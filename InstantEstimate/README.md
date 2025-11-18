# InstantEstimate 🏗️

**AI-Powered Cost Estimation for Structural Steel Buildings**

InstantEstimate is an intelligent cost estimation tool that generates detailed Bill of Quantities (BOQ) and cost estimates for structural steel buildings from simple text descriptions or structural JSON data.

## 🎯 Features

- **Multi-Input Support**: Text descriptions, structural JSON, or pre-built examples
- **Comprehensive Quantity Takeoff**: Automatically extracts steel, bolts, welds, concrete quantities
- **Regional Pricing**: Support for India, Middle East, Europe, and USA markets
- **Professional Reports**: Generate PDF and Excel BOQ reports
- **Interactive Web Interface**: Beautiful Streamlit-based UI
- **Instant Results**: Get cost estimates in seconds

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to the project directory
cd instant-estimate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### 1. Command Line Interface

```python
from main import generate_estimate_from_description

# Simple text description
description = "30m x 20m warehouse, HEA300 columns, IPE400 beams, S355 steel"
estimate = generate_estimate_from_description(description)
```

#### 2. Web Interface (Recommended)

```bash
# Launch the Streamlit app
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## 📊 Example Estimates

### Small Workshop
```
Description: "12m x 8m workshop, height 6m, HEA240 columns, IPE300 beams, S275 steel"
Estimated Cost: ₹4.5 - 6.5 Lakhs
Steel Weight: ~2.5 tonnes
Duration: 2-3 weeks
```

### Medium Industrial Warehouse
```
Description: "40m x 25m warehouse, height 10m, HEA400 columns @ 8m spacing, IPE500 beams, S355 steel"
Estimated Cost: ₹25 - 35 Lakhs
Steel Weight: ~15 tonnes
Duration: 6-8 weeks
```

### Large Aircraft Hangar
```
Description: "60m x 80m hangar, height 15m, UC356 portal columns, UB914 rafters, S355 steel"
Estimated Cost: ₹1.2 - 1.8 Crores
Steel Weight: ~80 tonnes
Duration: 4-6 months
```

## 🏗️ How It Works

```
Text/JSON Input
      ↓
Quantity Extraction (Steel, Bolts, Welds, Concrete)
      ↓
Pricing Engine (Regional rates, Labor costs)
      ↓
Cost Calculation (Materials + Labor + Overheads)
      ↓
Report Generation (PDF + Excel BOQ)
```

## 📁 Project Structure

```
instant-estimate/
├── main.py                 # Main pipeline orchestrator
├── quantity_extractor.py   # Material quantity extraction
├── pricing_engine.py       # Cost calculation with regional pricing
├── report_generator.py     # PDF and Excel report generation
├── app.py                  # Streamlit web interface
├── requirements.txt        # Python dependencies
├── test_example.py         # Testing suite
├── demo.sh                 # Demo launcher script
└── README.md              # This file
```

## 🔧 Core Modules

### 1. Quantity Extractor (`quantity_extractor.py`)

Extracts material quantities from structural JSON:
- Steel sections (HEA, IPE, UC, UB) with weight and paint area
- Bolts (M20, M24, M30) based on connection count
- Welds (fillet 6mm, 8mm) for connections
- Concrete foundations and reinforcement

### 2. Pricing Engine (`pricing_engine.py`)

Calculates costs with regional pricing:
- Material costs (steel, bolts, welding, concrete, paint)
- Labor costs (fabrication, erection)
- Overheads (10%), Profit (15%), Contingency (5%)
- Multi-currency support (INR, USD, EUR, AED)

### 3. Report Generator (`report_generator.py`)

Generates professional documents:
- **PDF Report**: Professional A4 format with company branding
- **Excel BOQ**: Detailed Bill of Quantities with line items
- Includes project summary, cost breakdown, and material details

### 4. Web Interface (`app.py`)

Interactive Streamlit application:
- Text description input
- JSON file upload
- Pre-built examples
- Real-time cost visualization
- Downloadable reports (PDF, Excel, JSON)

## 💡 API Usage

### Python API

```python
from quantity_extractor import QuantityExtractor
from pricing_engine import PricingEngine
from report_generator import ReportGenerator

# Step 1: Extract quantities
extractor = QuantityExtractor()
quantities = extractor.get_all_quantities(structural_json)

# Step 2: Calculate costs
pricing = PricingEngine(region="India")
estimate = pricing.calculate_total_estimate(quantities)

# Step 3: Generate reports
reporter = ReportGenerator()
pdf_file = reporter.generate_pdf(estimate)
excel_file = reporter.generate_excel(estimate)

print(f"Reports generated: {pdf_file}, {excel_file}")
```

## 🌍 Regional Pricing

Supported regions with local pricing:

- **India** (INR): Based on current Indian market rates
- **Middle East** (AED): UAE/GCC market rates
- **Europe** (EUR): European market averages
- **USA** (USD): North American market rates

## 📈 Cost Breakdown

Typical estimate includes:

1. **Materials**
   - Structural steel (by grade)
   - Bolts and fasteners
   - Welding consumables
   - Paint and coating
   - Concrete and reinforcement

2. **Labor**
   - Fabrication
   - Surface treatment
   - Erection and installation

3. **Indirect Costs**
   - Overhead (10%)
   - Profit margin (15%)
   - Contingency (5%)

## 🎓 Integration with TeklaMCP

InstantEstimate is designed to work seamlessly with TeklaMCP:

1. Generate Tekla model using TeklaMCP
2. Export structural JSON from TeklaMCP schema
3. Upload to InstantEstimate for cost estimation
4. Get instant BOQ and pricing

## 🧪 Testing

```bash
# Run all tests
python test_example.py

# Test specific module
python -c "from quantity_extractor import QuantityExtractor; print('✅ Quantity extractor OK')"
```

## 🏆 Hackathon Project

**Built for**: [Your Hackathon Name]
**Category**: AI/ML, Construction Tech, FinTech
**Team**: [Your Team Name]

### Innovation Highlights

1. **AI-Powered**: Intelligent quantity extraction and cost estimation
2. **Multi-Modal**: Text, JSON, or example-based input
3. **Professional Output**: Client-ready PDF and Excel reports
4. **Real-World Ready**: Based on actual market pricing and engineering practices
5. **User-Friendly**: Beautiful web interface for non-technical users

## 📸 Screenshots

### Web Interface
- Clean, modern Streamlit UI with tabs for different input methods
- Real-time cost visualization with charts and metrics
- One-click report generation and download

### PDF Report
- Professional A4 format with company branding
- Comprehensive cost breakdown tables
- Summary metrics and project information

### Excel BOQ
- Detailed line items with quantities and rates
- Separate sheets for summary and detailed breakdown
- Ready for contractor submission

## 🤝 Contributing

This is a hackathon project, but improvements are welcome!

## 📄 License

MIT License - Free for educational and commercial use

## 📞 Support

For questions or issues:
- Check the documentation in each module
- Review example usage in `main.py` and `test_example.py`
- Open an issue on GitHub

---

**Built with ❤️ for construction professionals worldwide**

*Making cost estimation instant, accurate, and accessible.*
