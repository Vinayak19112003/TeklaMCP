"""
Test Suite for InstantEstimate

This script tests all modules independently and runs end-to-end validation.
"""

import json
from quantity_extractor import QuantityExtractor, SectionDatabase
from pricing_engine import PricingEngine
from report_generator import ReportGenerator
from main import generate_estimate_from_description, generate_reports


def test_section_database():
    """Test SectionDatabase module"""
    print("🔍 Testing SectionDatabase...")

    db = SectionDatabase()

    # Test known sections
    test_sections = ["HEA300", "IPE400", "UC305x305x158", "UB533x210x101"]

    for profile in test_sections:
        section = db.get_section(profile)
        assert section.profile == profile, f"Profile mismatch for {profile}"
        assert section.weight_per_meter > 0, f"Invalid weight for {profile}"
        assert section.paint_area_per_meter > 0, f"Invalid paint area for {profile}"
        print(f"   ✓ {profile}: {section.weight_per_meter} kg/m, {section.paint_area_per_meter} m²/m")

    print("   ✅ SectionDatabase tests passed!\n")


def test_quantity_extractor():
    """Test QuantityExtractor module"""
    print("🔍 Testing QuantityExtractor...")

    extractor = QuantityExtractor()

    # Test data
    test_data = {
        "project": {"name": "Test Building"},
        "columns": [
            {"profile": "HEA300", "material": "S355", "height": 8000, "quantity": 4},
        ],
        "beams": [
            {"profile": "IPE400", "material": "S355", "length": 10000, "quantity": 6},
        ],
        "bracing": [
            {"profile": "L100x100x10", "material": "S275", "length": 8000, "quantity": 4},
        ]
    }

    quantities = extractor.get_all_quantities(test_data)

    # Validate steel quantities
    assert "steel" in quantities, "Missing steel quantities"
    assert "S355" in quantities["steel"], "Missing S355 steel"
    assert quantities["steel"]["S355"]["weight_kg"] > 0, "Invalid steel weight"
    print(f"   ✓ Steel S355: {quantities['steel']['S355']['weight_kg']:.2f} kg")

    # Validate bolts
    assert "bolts" in quantities, "Missing bolt quantities"
    assert quantities["bolts"]["M24"] > 0, "Missing M24 bolts"
    print(f"   ✓ Bolts M24: {quantities['bolts']['M24']} nos")

    # Validate welds
    assert "welds" in quantities, "Missing weld quantities"
    total_welds = sum(quantities["welds"].values())
    assert total_welds > 0, "Invalid weld quantities"
    print(f"   ✓ Total welds: {total_welds:.1f} m")

    # Validate concrete
    assert "concrete" in quantities, "Missing concrete quantities"
    assert quantities["concrete"]["M30"] > 0, "Invalid concrete volume"
    print(f"   ✓ Concrete M30: {quantities['concrete']['M30']:.2f} m³")

    print("   ✅ QuantityExtractor tests passed!\n")


def test_pricing_engine():
    """Test PricingEngine module"""
    print("🔍 Testing PricingEngine...")

    # Test quantities
    test_quantities = {
        "steel": {
            "S355": {
                "weight_kg": 2500.5,
                "paint_area_m2": 150.2,
                "members": []
            }
        },
        "bolts": {
            "M20": 96,
            "M24": 16,
            "M30": 0
        },
        "welds": {
            "fillet_6mm": 18.4,
            "fillet_8mm": 8.0
        },
        "concrete": {
            "M30": 4.0,
            "reinforcement_kg": 400.0
        }
    }

    # Test all regions
    regions = ["India", "Middle East", "Europe", "USA"]

    for region in regions:
        pricing = PricingEngine(region=region)
        estimate = pricing.calculate_total_estimate(test_quantities)

        # Validate estimate structure
        assert "project_summary" in estimate, f"Missing project_summary for {region}"
        assert "material_costs" in estimate, f"Missing material_costs for {region}"
        assert "labor_costs" in estimate, f"Missing labor_costs for {region}"
        assert "summary" in estimate, f"Missing summary for {region}"

        # Validate costs are positive
        assert estimate["summary"]["materials"] > 0, f"Invalid materials cost for {region}"
        assert estimate["summary"]["labor"] > 0, f"Invalid labor cost for {region}"
        assert estimate["summary"]["total_estimate"] > 0, f"Invalid total for {region}"

        print(f"   ✓ {region}: {pricing.format_amount(estimate['summary']['total_estimate'])}")

    print("   ✅ PricingEngine tests passed!\n")


def test_report_generator():
    """Test ReportGenerator module"""
    print("🔍 Testing ReportGenerator...")

    # Sample estimate data
    sample_estimate = {
        "project_summary": {
            "date": "2024-01-15 14:30:00",
            "region": "India",
            "currency": "INR",
            "total_steel_weight_tonnes": 2.501,
        },
        "material_costs": {
            "steel": [
                {"item": "Structural Steel - S355", "quantity": 2.501, "unit": "tonne", "rate": 65000, "amount": 162565.0}
            ],
            "bolts": [
                {"item": "Bolts - M20", "quantity": 96, "unit": "nos", "rate": 15, "amount": 1440.0}
            ],
            "welding": [
                {"item": "Welding - Fillet 6mm", "quantity": 18.4, "unit": "m", "rate": 120, "amount": 2208.0}
            ],
            "concrete": [
                {"item": "Concrete - M30", "quantity": 4.0, "unit": "m³", "rate": 7000, "amount": 28000.0}
            ],
            "paint": [
                {"item": "Steel Painting (2 coats)", "quantity": 150.2, "unit": "m²", "rate": 250, "amount": 37550.0}
            ],
            "total": 259603.0
        },
        "labor_costs": {
            "items": [
                {"item": "Steel Fabrication", "quantity": 2.501, "unit": "tonne", "rate": 8000, "amount": 20008.0},
                {"item": "Steel Erection & Installation", "quantity": 2.501, "unit": "tonne", "rate": 12000, "amount": 30012.0}
            ],
            "total": 50020.0
        },
        "summary": {
            "materials": 259603.0,
            "labor": 50020.0,
            "subtotal": 309623.0,
            "overhead_10%": 30962.3,
            "profit_15%": 46443.45,
            "contingency_5%": 15481.15,
            "total_estimate": 402509.9
        },
        "currency_symbol": "₹"
    }

    reporter = ReportGenerator()

    # Test PDF generation
    pdf_file = reporter.generate_pdf(sample_estimate, "Test Project - PDF")
    assert pdf_file.endswith(".pdf"), "Invalid PDF filename"
    print(f"   ✓ PDF generated: {pdf_file}")

    # Test Excel generation
    excel_file = reporter.generate_excel(sample_estimate, "Test Project - Excel")
    assert excel_file.endswith(".xlsx"), "Invalid Excel filename"
    print(f"   ✓ Excel generated: {excel_file}")

    print("   ✅ ReportGenerator tests passed!\n")


def test_end_to_end():
    """Test complete end-to-end pipeline"""
    print("🔍 Testing End-to-End Pipeline...")

    description = "Test warehouse - 20m x 15m, height 8m, HEA300 columns, IPE400 beams, S355 steel"

    # Generate estimate
    estimate = generate_estimate_from_description(
        description=description,
        region="India"
    )

    # Validate estimate
    assert estimate is not None, "Estimate generation failed"
    assert "project_summary" in estimate, "Missing project_summary"
    assert "summary" in estimate, "Missing summary"
    assert estimate["summary"]["total_estimate"] > 0, "Invalid total estimate"

    print(f"   ✓ Estimate generated: ₹{estimate['summary']['total_estimate']:,.2f}")

    # Generate reports
    reports = generate_reports(estimate, "Test Project - E2E")

    assert "pdf" in reports, "PDF report not generated"
    assert "excel" in reports, "Excel report not generated"

    print(f"   ✓ PDF: {reports['pdf']}")
    print(f"   ✓ Excel: {reports['excel']}")

    print("   ✅ End-to-End tests passed!\n")


def run_all_tests():
    """Run all tests"""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "INSTANTESTIMATE TEST SUITE" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    tests = [
        ("Section Database", test_section_database),
        ("Quantity Extractor", test_quantity_extractor),
        ("Pricing Engine", test_pricing_engine),
        ("Report Generator", test_report_generator),
        ("End-to-End Pipeline", test_end_to_end),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"   ❌ Test failed: {str(e)}\n")
            failed += 1
        except Exception as e:
            print(f"   ❌ Unexpected error: {str(e)}\n")
            failed += 1

    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 20 + "TEST RESULTS" + " " * 26 + "║")
    print("╠" + "═" * 58 + "╣")
    print(f"║  Total Tests: {len(tests):<44} ║")
    print(f"║  Passed: {passed:<49} ║")
    print(f"║  Failed: {failed:<49} ║")
    print("╚" + "═" * 58 + "╝")
    print()

    if failed == 0:
        print("✅ ALL TESTS PASSED! 🎉")
        print("   InstantEstimate is ready for deployment!")
    else:
        print(f"❌ {failed} test(s) failed. Please review the errors above.")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
