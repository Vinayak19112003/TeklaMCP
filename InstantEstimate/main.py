"""
Main Pipeline - InstantEstimate

This module orchestrates the complete cost estimation pipeline:
Text/JSON → Quantities → Pricing → Reports
"""

import json
from typing import Dict
from quantity_extractor import QuantityExtractor
from pricing_engine import PricingEngine
from report_generator import ReportGenerator


def generate_estimate_from_description(
    description: str,
    region: str = "India",
    structural_json: Dict = None
) -> Dict:
    """
    Generate complete cost estimate from building description or structural JSON

    Args:
        description: Text description of the building
        region: Region for pricing ("India", "Middle East", "Europe", "USA")
        structural_json: Optional pre-formatted structural JSON (if provided, description is ignored)

    Returns:
        Complete estimate dictionary with all quantities, costs, and report filenames
    """

    print("🏗️  InstantEstimate - AI-Powered Cost Estimation")
    print("=" * 60)
    print()

    # Step 1: Parse structural data
    print("📋 Step 1: Parsing structural data...")

    if structural_json is None:
        # For now, use sample data (in production, this would call an AI parser)
        print(f"   Input: {description[:50]}...")
        structural_data = _parse_description_to_json(description)
    else:
        structural_data = structural_json

    print(f"   ✅ Structural data prepared")
    print()

    # Step 2: Extract quantities
    print("📊 Step 2: Extracting material quantities...")
    extractor = QuantityExtractor()
    quantities = extractor.get_all_quantities(structural_data)

    # Print quantity summary
    total_steel_kg = sum(data.get("weight_kg", 0) for data in quantities["steel"].values())
    total_bolts = sum(quantities["bolts"].values())
    total_weld_length = sum(quantities["welds"].values())

    print(f"   Steel: {total_steel_kg/1000:.2f} tonnes")
    print(f"   Bolts: {total_bolts} nos")
    print(f"   Welds: {total_weld_length:.1f} m")
    print(f"   ✅ Quantities extracted")
    print()

    # Step 3: Calculate costs
    print(f"💰 Step 3: Calculating costs ({region})...")
    pricing = PricingEngine(region=region)
    estimate = pricing.calculate_total_estimate(quantities)

    print(f"   Materials: {pricing.format_amount(estimate['summary']['materials'])}")
    print(f"   Labor: {pricing.format_amount(estimate['summary']['labor'])}")
    print(f"   Total: {pricing.format_amount(estimate['summary']['total_estimate'])}")
    print(f"   ✅ Costs calculated")
    print()

    # Step 4: Print cost breakdown table
    print("💵 COST BREAKDOWN:")
    print("─" * 60)
    print(f"  {'Description':<30} {'Amount':>20}")
    print("─" * 60)
    print(f"  {'Materials':<30} {pricing.format_amount(estimate['summary']['materials']):>20}")
    print(f"  {'Labor':<30} {pricing.format_amount(estimate['summary']['labor']):>20}")
    print(f"  {'Subtotal':<30} {pricing.format_amount(estimate['summary']['subtotal']):>20}")
    print(f"  {'Overhead (10%)':<30} {pricing.format_amount(estimate['summary']['overhead_10%']):>20}")
    print(f"  {'Profit (15%)':<30} {pricing.format_amount(estimate['summary']['profit_15%']):>20}")
    print(f"  {'Contingency (5%)':<30} {pricing.format_amount(estimate['summary']['contingency_5%']):>20}")
    print("═" * 60)
    print(f"  {'TOTAL ESTIMATE':<30} {pricing.format_amount(estimate['summary']['total_estimate']):>20}")
    print("═" * 60)
    print()

    # Step 5: Save to JSON
    print("💾 Step 4: Saving estimate to JSON...")
    with open("estimate.json", "w") as f:
        json.dump(estimate, f, indent=2)
    print(f"   ✅ Saved to estimate.json")
    print()

    # Add structural data and quantities to estimate
    estimate["structural_data"] = structural_data
    estimate["quantities"] = quantities

    # Return complete estimate
    print("✅ Estimate generation completed!")
    print("=" * 60)
    print()

    return estimate


def generate_reports(estimate: Dict, project_name: str = "Structural Steel Project") -> Dict[str, str]:
    """
    Generate PDF and Excel reports from estimate

    Args:
        estimate: Complete estimate dictionary
        project_name: Name of the project

    Returns:
        Dict with report filenames {"pdf": "...", "excel": "..."}
    """
    print("📄 Generating reports...")
    print()

    reporter = ReportGenerator()

    # Generate PDF
    print("   Generating PDF report...")
    pdf_file = reporter.generate_pdf(estimate, project_name)
    print(f"   ✅ PDF: {pdf_file}")

    # Generate Excel
    print("   Generating Excel BOQ...")
    excel_file = reporter.generate_excel(estimate, project_name)
    print(f"   ✅ Excel: {excel_file}")

    print()
    print("✅ All reports generated successfully!")
    print()

    return {"pdf": pdf_file, "excel": excel_file}


def _parse_description_to_json(description: str) -> Dict:
    """
    Parse text description to structural JSON

    In production, this would use AI (Claude/GPT-4) to extract structural details.
    For now, returns sample data based on keywords in description.

    Args:
        description: Text description of building

    Returns:
        Structural JSON
    """
    # Simple keyword-based parsing for demo
    # In production, this would be replaced with AI parsing

    description_lower = description.lower()

    # Determine building size and profiles
    if "small" in description_lower or "workshop" in description_lower:
        # Small workshop
        return {
            "project": {"name": "Small Workshop"},
            "columns": [
                {"profile": "HEA240", "material": "S275", "height": 6000, "quantity": 4},
            ],
            "beams": [
                {"profile": "IPE300", "material": "S275", "length": 8000, "quantity": 4},
            ],
            "bracing": []
        }

    elif "large" in description_lower or "hangar" in description_lower:
        # Large hangar
        return {
            "project": {"name": "Large Aircraft Hangar"},
            "columns": [
                {"profile": "UC356x406x634", "material": "S355", "height": 15000, "quantity": 20},
            ],
            "beams": [
                {"profile": "UB914x419x388", "material": "S355", "length": 60000, "quantity": 10},
                {"profile": "UB914x419x388", "material": "S355", "length": 80000, "quantity": 10},
            ],
            "bracing": [
                {"profile": "L150x150x15", "material": "S355", "length": 10000, "quantity": 40},
            ]
        }

    else:
        # Default: medium warehouse
        return {
            "project": {"name": "Industrial Warehouse"},
            "columns": [
                {"profile": "HEA300", "material": "S355", "height": 8000, "quantity": 12},
            ],
            "beams": [
                {"profile": "IPE400", "material": "S355", "length": 10000, "quantity": 18},
                {"profile": "IPE300", "material": "S355", "length": 8000, "quantity": 12},
            ],
            "bracing": [
                {"profile": "L100x100x10", "material": "S275", "length": 8000, "quantity": 8},
            ]
        }


# Example usage
if __name__ == "__main__":
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "INSTANTESTIMATE - DEMO" + " " * 26 + "║")
    print("║" + " " * 8 + "AI-Powered Cost Estimation Tool" + " " * 19 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    # Example 1: Medium warehouse
    print("\n📌 EXAMPLE 1: Medium Industrial Warehouse")
    print("-" * 60)

    description1 = "40m x 25m industrial warehouse, height 10m, HEA400 columns @ 8m spacing, IPE500 roof beams, S355 steel"

    estimate1 = generate_estimate_from_description(
        description=description1,
        region="India"
    )

    # Generate reports
    reports1 = generate_reports(estimate1, "Industrial Warehouse - Example 1")

    print(f"📁 Files generated:")
    print(f"   - PDF: {reports1['pdf']}")
    print(f"   - Excel: {reports1['excel']}")
    print(f"   - JSON: estimate.json")
    print()

    # Example 2: Small workshop
    print("\n📌 EXAMPLE 2: Small Workshop")
    print("-" * 60)

    description2 = "Small workshop - 12m x 8m, height 6m, HEA240 columns, IPE300 beams, S275 steel"

    estimate2 = generate_estimate_from_description(
        description=description2,
        region="India"
    )

    # Generate reports
    reports2 = generate_reports(estimate2, "Small Workshop - Example 2")

    print(f"📁 Files generated:")
    print(f"   - PDF: {reports2['pdf']}")
    print(f"   - Excel: {reports2['excel']}")
    print()

    # Example 3: Using custom structural JSON
    print("\n📌 EXAMPLE 3: Custom Structural JSON")
    print("-" * 60)

    custom_json = {
        "project": {"name": "Custom Building"},
        "columns": [
            {"profile": "UC305x305x158", "material": "S355", "height": 12000, "quantity": 8},
        ],
        "beams": [
            {"profile": "UB533x210x101", "material": "S355", "length": 15000, "quantity": 12},
        ],
        "bracing": [
            {"profile": "L120x120x12", "material": "S275", "length": 9000, "quantity": 16},
        ]
    }

    estimate3 = generate_estimate_from_description(
        description="Custom building",
        region="Middle East",  # Using different region
        structural_json=custom_json
    )

    # Generate reports
    reports3 = generate_reports(estimate3, "Custom Building - Middle East")

    print(f"📁 Files generated:")
    print(f"   - PDF: {reports3['pdf']}")
    print(f"   - Excel: {reports3['excel']}")
    print()

    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "ALL EXAMPLES COMPLETED!" + " " * 21 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    print("✨ InstantEstimate is ready for use!")
    print("   Run 'streamlit run app.py' to launch the web interface")
    print()
