"""
InstantEstimate - Streamlit Web Interface

Beautiful web interface for AI-powered structural cost estimation.
"""

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from main import generate_estimate_from_description, generate_reports


# Page configuration
st.set_page_config(
    page_title="InstantEstimate - AI Cost Estimator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f4788;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'estimate' not in st.session_state:
    st.session_state.estimate = None
if 'reports' not in st.session_state:
    st.session_state.reports = None


def get_example_data(example_name: str) -> dict:
    """Get pre-built example structural data"""
    examples = {
        "Small Workshop": {
            "description": "12m x 8m workshop, height 6m, HEA240 columns, IPE300 beams, S275 steel",
            "json": {
                "project": {"name": "Small Workshop"},
                "columns": [
                    {"profile": "HEA240", "material": "S275", "height": 6000, "quantity": 4},
                ],
                "beams": [
                    {"profile": "IPE300", "material": "S275", "length": 8000, "quantity": 4},
                ],
                "bracing": []
            }
        },
        "Medium Factory": {
            "description": "30m x 20m factory, height 8m, HEA300 columns @ 6m spacing, IPE400 beams, S355 steel",
            "json": {
                "project": {"name": "Medium Factory"},
                "columns": [
                    {"profile": "HEA300", "material": "S355", "height": 8000, "quantity": 15},
                ],
                "beams": [
                    {"profile": "IPE400", "material": "S355", "length": 10000, "quantity": 20},
                    {"profile": "IPE300", "material": "S355", "length": 6000, "quantity": 15},
                ],
                "bracing": [
                    {"profile": "L100x100x10", "material": "S275", "length": 8000, "quantity": 12},
                ]
            }
        },
        "Large Shed": {
            "description": "50m x 30m shed, height 12m, HEA400 columns @ 10m spacing, IPE500 roof beams, S355 steel with bracing",
            "json": {
                "project": {"name": "Large Industrial Shed"},
                "columns": [
                    {"profile": "HEA400", "material": "S355", "height": 12000, "quantity": 18},
                ],
                "beams": [
                    {"profile": "IPE500", "material": "S355", "length": 10000, "quantity": 30},
                    {"profile": "IPE400", "material": "S355", "length": 10000, "quantity": 24},
                ],
                "bracing": [
                    {"profile": "L120x120x12", "material": "S275", "length": 10000, "quantity": 24},
                ]
            }
        }
    }
    return examples.get(example_name, examples["Small Workshop"])


def display_summary_metrics(estimate: dict):
    """Display summary metrics in columns"""
    col1, col2, col3, col4 = st.columns(4)

    total_steel = estimate['project_summary']['total_steel_weight_tonnes']
    total_bolts = sum(estimate['quantities']['bolts'].values())
    total_cost = estimate['summary']['total_estimate']
    currency = estimate.get('currency_symbol', estimate['project_summary']['currency'])

    # Calculate estimated duration (based on steel weight)
    duration_weeks = max(2, int(total_steel * 0.5))  # Rough estimate

    with col1:
        st.metric(
            label="🏗️ Total Steel",
            value=f"{total_steel:.2f} tonnes",
            help="Total structural steel weight"
        )

    with col2:
        st.metric(
            label="🔩 Total Bolts",
            value=f"{total_bolts} nos",
            help="Total number of bolts required"
        )

    with col3:
        st.metric(
            label="💰 Total Estimate",
            value=f"{currency}{total_cost:,.0f}",
            help="Complete project cost estimate"
        )

    with col4:
        st.metric(
            label="⏱️ Est. Duration",
            value=f"{duration_weeks} weeks",
            help="Estimated project duration"
        )


def display_cost_chart(estimate: dict):
    """Display cost breakdown chart"""
    summary = estimate['summary']
    currency = estimate.get('currency_symbol', estimate['project_summary']['currency'])

    # Create data for chart
    categories = ['Materials', 'Labor', 'Overhead', 'Profit', 'Contingency']
    values = [
        summary['materials'],
        summary['labor'],
        summary['overhead_10%'],
        summary['profit_15%'],
        summary['contingency_5%']
    ]

    # Create bar chart using plotly
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            text=[f"{currency}{v:,.0f}" for v in values],
            textposition='outside',
            marker_color=['#1f4788', '#2563eb', '#60a5fa', '#93c5fd', '#dbeafe']
        )
    ])

    fig.update_layout(
        title="Cost Breakdown",
        xaxis_title="Category",
        yaxis_title=f"Amount ({currency})",
        height=400,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def display_material_details(estimate: dict):
    """Display detailed material breakdown"""
    material_costs = estimate['material_costs']
    currency = estimate.get('currency_symbol', estimate['project_summary']['currency'])

    # Create material DataFrame
    materials_data = []

    # Add steel
    for item in material_costs.get('steel', []):
        materials_data.append({
            'Category': 'Steel',
            'Item': item['item'],
            'Quantity': f"{item['quantity']:.3f}",
            'Unit': item['unit'],
            'Rate': f"{currency}{item['rate']:,.2f}",
            'Amount': f"{currency}{item['amount']:,.2f}"
        })

    # Add bolts
    for item in material_costs.get('bolts', []):
        materials_data.append({
            'Category': 'Bolts',
            'Item': item['item'],
            'Quantity': str(item['quantity']),
            'Unit': item['unit'],
            'Rate': f"{currency}{item['rate']:,.2f}",
            'Amount': f"{currency}{item['amount']:,.2f}"
        })

    # Add welding
    for item in material_costs.get('welding', []):
        materials_data.append({
            'Category': 'Welding',
            'Item': item['item'],
            'Quantity': f"{item['quantity']:.1f}",
            'Unit': item['unit'],
            'Rate': f"{currency}{item['rate']:,.2f}",
            'Amount': f"{currency}{item['amount']:,.2f}"
        })

    # Add concrete
    for item in material_costs.get('concrete', []):
        materials_data.append({
            'Category': 'Concrete',
            'Item': item['item'],
            'Quantity': f"{item['quantity']:.2f}",
            'Unit': item['unit'],
            'Rate': f"{currency}{item['rate']:,.2f}",
            'Amount': f"{currency}{item['amount']:,.2f}"
        })

    # Add paint
    for item in material_costs.get('paint', []):
        materials_data.append({
            'Category': 'Paint',
            'Item': item['item'],
            'Quantity': f"{item['quantity']:.2f}",
            'Unit': item['unit'],
            'Rate': f"{currency}{item['rate']:,.2f}",
            'Amount': f"{currency}{item['amount']:,.2f}"
        })

    df_materials = pd.DataFrame(materials_data)

    with st.expander("📊 Detailed Material Costs", expanded=False):
        st.dataframe(df_materials, use_container_width=True, hide_index=True)


def display_labor_details(estimate: dict):
    """Display labor cost details"""
    labor_costs = estimate['labor_costs']
    currency = estimate.get('currency_symbol', estimate['project_summary']['currency'])

    labor_data = []
    for item in labor_costs['items']:
        labor_data.append({
            'Item': item['item'],
            'Quantity': f"{item['quantity']:.3f}",
            'Unit': item['unit'],
            'Rate': f"{currency}{item['rate']:,.2f}",
            'Amount': f"{currency}{item['amount']:,.2f}"
        })

    df_labor = pd.DataFrame(labor_data)

    with st.expander("👷 Labor Costs", expanded=False):
        st.dataframe(df_labor, use_container_width=True, hide_index=True)
        st.info(f"**Total Labor Cost:** {currency}{labor_costs['total']:,.2f}")


# Main App
def main():
    # Header
    st.markdown('<div class="main-header">🏗️ InstantEstimate</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Structural Cost Estimation Tool</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        region = st.selectbox(
            "Region",
            ["India", "Middle East", "Europe", "USA"],
            help="Select region for pricing"
        )

        currency_map = {
            "India": "INR (₹)",
            "Middle East": "AED",
            "Europe": "EUR (€)",
            "USA": "USD ($)"
        }
        st.info(f"💱 Currency: {currency_map[region]}")

        st.markdown("---")

        st.header("ℹ️ About")
        st.markdown("""
        **InstantEstimate** generates professional cost estimates for structural steel buildings.

        **Features:**
        - Instant quantity takeoff
        - Regional pricing
        - PDF & Excel reports
        - Multi-modal input

        **Version:** 1.0.0
        """)

    # Main Content - Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Text Description", "📊 Upload JSON", "💾 Examples"])

    # TAB 1: Text Description
    with tab1:
        st.subheader("Enter Building Description")

        description = st.text_area(
            "Describe your structural steel building",
            value="30m x 20m warehouse, height 8m, HEA300 columns @ 6m spacing, IPE400 beams, S355 steel",
            height=100,
            help="Describe the building in natural language. Include: dimensions, height, column spacing, member sizes, steel grade."
        )

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🚀 Generate Estimate", type="primary", key="text_btn"):
                with st.spinner("Generating estimate..."):
                    try:
                        st.session_state.estimate = generate_estimate_from_description(
                            description=description,
                            region=region
                        )
                        st.session_state.reports = None  # Reset reports
                        st.success("✅ Estimate generated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    # TAB 2: Upload JSON
    with tab2:
        st.subheader("Upload Structural JSON")

        uploaded_file = st.file_uploader(
            "Choose a JSON file",
            type=['json'],
            help="Upload a JSON file with structural data (columns, beams, bracing)"
        )

        if uploaded_file is not None:
            try:
                structural_json = json.load(uploaded_file)
                st.success("✅ File uploaded successfully!")

                with st.expander("👀 Preview JSON", expanded=True):
                    st.json(structural_json)

                if st.button("🚀 Generate Estimate", type="primary", key="json_btn"):
                    with st.spinner("Generating estimate..."):
                        try:
                            st.session_state.estimate = generate_estimate_from_description(
                                description="Uploaded JSON",
                                region=region,
                                structural_json=structural_json
                            )
                            st.session_state.reports = None
                            st.success("✅ Estimate generated successfully!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

            except json.JSONDecodeError:
                st.error("❌ Invalid JSON file. Please check the format.")

    # TAB 3: Examples
    with tab3:
        st.subheader("Pre-Built Examples")
        st.markdown("Click on an example below to generate instant estimate:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("**🏪 Small Workshop**\n\n12m x 8m, 6m height\n\nEstimate: ₹4-6 Lakhs")
            if st.button("Load Example", key="ex1"):
                example_data = get_example_data("Small Workshop")
                with st.spinner("Generating estimate..."):
                    try:
                        st.session_state.estimate = generate_estimate_from_description(
                            description=example_data["description"],
                            region=region,
                            structural_json=example_data["json"]
                        )
                        st.session_state.reports = None
                        st.success("✅ Small Workshop estimate ready!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        with col2:
            st.info("**🏭 Medium Factory**\n\n30m x 20m, 8m height\n\nEstimate: ₹15-25 Lakhs")
            if st.button("Load Example", key="ex2"):
                example_data = get_example_data("Medium Factory")
                with st.spinner("Generating estimate..."):
                    try:
                        st.session_state.estimate = generate_estimate_from_description(
                            description=example_data["description"],
                            region=region,
                            structural_json=example_data["json"]
                        )
                        st.session_state.reports = None
                        st.success("✅ Medium Factory estimate ready!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        with col3:
            st.info("**🏗️ Large Shed**\n\n50m x 30m, 12m height\n\nEstimate: ₹40-60 Lakhs")
            if st.button("Load Example", key="ex3"):
                example_data = get_example_data("Large Shed")
                with st.spinner("Generating estimate..."):
                    try:
                        st.session_state.estimate = generate_estimate_from_description(
                            description=example_data["description"],
                            region=region,
                            structural_json=example_data["json"]
                        )
                        st.session_state.reports = None
                        st.success("✅ Large Shed estimate ready!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    # Display Results (if estimate exists)
    if st.session_state.estimate is not None:
        st.markdown("---")
        st.header("📊 Estimate Results")

        estimate = st.session_state.estimate

        # Summary Metrics
        display_summary_metrics(estimate)

        st.markdown("---")

        # Cost Breakdown Chart
        col1, col2 = st.columns([2, 1])

        with col1:
            display_cost_chart(estimate)

        with col2:
            st.subheader("📋 Summary")
            currency = estimate.get('currency_symbol', estimate['project_summary']['currency'])
            summary = estimate['summary']

            st.markdown(f"""
            **Materials:** {currency}{summary['materials']:,.2f}

            **Labor:** {currency}{summary['labor']:,.2f}

            **Subtotal:** {currency}{summary['subtotal']:,.2f}

            **Overhead (10%):** {currency}{summary['overhead_10%']:,.2f}

            **Profit (15%):** {currency}{summary['profit_15%']:,.2f}

            **Contingency (5%):** {currency}{summary['contingency_5%']:,.2f}

            ---

            **TOTAL:** {currency}{summary['total_estimate']:,.2f}
            """)

        st.markdown("---")

        # Detailed Breakdowns
        display_material_details(estimate)
        display_labor_details(estimate)

        st.markdown("---")

        # Generate Reports Section
        st.header("📄 Download Reports")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📑 Generate PDF Report", key="gen_pdf"):
                with st.spinner("Generating PDF..."):
                    try:
                        project_name = estimate.get('structural_data', {}).get('project', {}).get('name', 'Structural Steel Project')
                        reports = generate_reports(estimate, project_name)
                        st.session_state.reports = reports
                        st.success(f"✅ PDF generated: {reports['pdf']}")
                    except Exception as e:
                        st.error(f"❌ Error generating PDF: {str(e)}")

        with col2:
            if st.button("📊 Generate Excel BOQ", key="gen_excel"):
                with st.spinner("Generating Excel..."):
                    try:
                        project_name = estimate.get('structural_data', {}).get('project', {}).get('name', 'Structural Steel Project')
                        reports = generate_reports(estimate, project_name)
                        st.session_state.reports = reports
                        st.success(f"✅ Excel generated: {reports['excel']}")
                    except Exception as e:
                        st.error(f"❌ Error generating Excel: {str(e)}")

        with col3:
            # Download JSON
            json_str = json.dumps(estimate, indent=2)
            st.download_button(
                label="💾 Download JSON",
                data=json_str,
                file_name=f"estimate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        # Display download links if reports are generated
        if st.session_state.reports is not None:
            st.success("📁 Reports generated successfully!")

            col1, col2 = st.columns(2)

            with col1:
                with open(st.session_state.reports['pdf'], 'rb') as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name=st.session_state.reports['pdf'],
                        mime="application/pdf"
                    )

            with col2:
                with open(st.session_state.reports['excel'], 'rb') as f:
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=f,
                        file_name=st.session_state.reports['excel'],
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )


if __name__ == "__main__":
    main()
