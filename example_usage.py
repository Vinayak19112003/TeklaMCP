"""
Example Usage of AI Tekla Model Generator

This script demonstrates how to use the system to generate
Tekla models from different input types.
"""

from dotenv import load_dotenv
load_dotenv()

# Example 1: Generate from text description
def example_text_to_model():
    """
    Simple text description to Tekla model
    """
    print("=" * 60)
    print("EXAMPLE 1: Text to Tekla Model")
    print("=" * 60)

    # This would use the actual implementation:
    # from src.main import TeklaAIGenerator
    # generator = TeklaAIGenerator()

    description = """
    Create an industrial warehouse building:
    - Dimensions: 50m long x 30m wide x 12m high
    - Grid spacing: 10m in both directions
    - Columns: UC305x305x198, S355 steel
    - Roof beams: UB610x229x125, S355 steel
    - Base plates: Simple base plates with 6xM30 anchor bolts
    - Bracing: X-bracing on all perimeter bays
    - Design code: Eurocode 3
    - Loads:
      * Dead load: 0.5 kN/m²
      * Live load: 2.5 kN/m²
      * Wind load: 1.2 kN/m²
    """

    print("\nInput Description:")
    print(description)

    # Generate model
    # result = generator.from_text(description)

    # Save outputs
    # result.save("output/warehouse")

    print("\nExpected Output:")
    print("✓ Extracted JSON with building parameters")
    print("✓ Validated BuildingSchema")
    print("✓ Complete Tekla C# code")
    print("✓ Ready to execute in Tekla Structures")

    print("\nGenerated files:")
    print("  output/warehouse/extracted.json")
    print("  output/warehouse/schema.json")
    print("  output/warehouse/TeklaModel.cs")


# Example 2: Generate from PDF drawing
def example_pdf_to_model():
    """
    PDF structural drawing to Tekla model
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: PDF Drawing to Tekla Model")
    print("=" * 60)

    # This would use the actual implementation:
    # from src.main import TeklaAIGenerator
    # generator = TeklaAIGenerator()

    pdf_path = "drawings/structural_plan.pdf"

    print(f"\nInput: {pdf_path}")
    print("  - General arrangement plan")
    print("  - Column and beam schedules")
    print("  - Foundation details")
    print("  - Connection details")

    # Process PDF
    # result = generator.from_pdf(pdf_path)

    print("\nProcessing steps:")
    print("✓ Extract pages from PDF")
    print("✓ Classify page types (plan/schedule/detail)")
    print("✓ Vision AI analysis of drawings")
    print("✓ Table extraction from schedules")
    print("✓ Merge all extracted data")
    print("✓ Generate schema and code")

    # Save outputs
    # result.save("output/from_pdf")

    print("\nGenerated files:")
    print("  output/from_pdf/extracted.json")
    print("  output/from_pdf/schema.json")
    print("  output/from_pdf/TeklaModel.cs")


# Example 3: Iterative refinement
def example_iterative_refinement():
    """
    Make modifications to generated model
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Iterative Refinement")
    print("=" * 60)

    # Initial generation
    # from src.main import TeklaAIGenerator
    # generator = TeklaAIGenerator()

    initial_description = """
    40m x 30m building, 8m high,
    8m spacing, HEA300 columns,
    IPE400 beams, S355 steel
    """

    print("\nStep 1: Initial generation")
    print(f"Input: {initial_description}")

    # result = generator.from_text(initial_description)
    # schema_v1 = result.get_schema()

    print("✓ Initial model generated")
    print("  - 20 columns (HEA300)")
    print("  - 30 beams (IPE400)")

    # Modification 1
    print("\nStep 2: User feedback")
    feedback_1 = "Change all perimeter columns to UC356x406x287"

    print(f"Feedback: {feedback_1}")

    # from src.feedback.feedback_processor import FeedbackProcessor
    # processor = FeedbackProcessor()
    # schema_v2 = processor.apply_modifications(schema_v1, feedback_1)

    print("✓ Schema updated")
    print("  - 12 perimeter columns → UC356x406x287")
    print("  - 8 interior columns → HEA300 (unchanged)")

    # Modification 2
    print("\nStep 3: More modifications")
    feedback_2 = "Add moment connections at all beam-column joints"

    print(f"Feedback: {feedback_2}")

    # schema_v3 = processor.apply_modifications(schema_v2, feedback_2)

    print("✓ Connections added")
    print("  - 30 moment connections created")

    # Regenerate code
    print("\nStep 4: Regenerate code")
    # code = generator.code_gen.generate(schema_v3)

    print("✓ Updated C# code generated")
    print("✓ Ready to execute in Tekla")


# Example 4: Advanced usage with options
def example_advanced_usage():
    """
    Advanced usage with custom options
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Advanced Usage")
    print("=" * 60)

    # Custom configuration
    config = {
        "cache_enabled": True,
        "auto_execute": False,
        "save_intermediate": True,
        "validation_level": "strict",
        "code_template": "custom_template.cs",
        "connection_library": "eurocode_connections"
    }

    print("\nConfiguration:")
    for key, value in config.items():
        print(f"  {key}: {value}")

    # Complex building description
    description = """
    Design a multi-bay portal frame structure:

    GEOMETRY:
    - Length: 80m (10 bays @ 8m spacing)
    - Width: 30m (single span)
    - Eave height: 10m
    - Ridge height: 12m
    - Portal frame spacing: 8m

    STRUCTURAL ELEMENTS:
    - Columns: UB533x210x101, S355J2
    - Rafters: UB457x191x74, S355J2
    - Purlins: Z200 @ 1.5m spacing
    - Side rails: Z150 @ 1.5m spacing
    - Bracing: Angle 100x100x10

    FOUNDATIONS:
    - Pad foundations with holding down bolts
    - 4xM30 bolts per base plate
    - Foundation depth: 1500mm

    CONNECTIONS:
    - Eave: Moment connection (bolted)
    - Apex: Moment connection (bolted)
    - Base: Fixed base plate connection
    - Purlin to rafter: Cleat connection

    LOADS:
    - Dead load: 0.6 kN/m² (including self-weight)
    - Live load (roof): 0.75 kN/m²
    - Snow load: 0.8 kN/m²
    - Wind pressure: 1.2 kN/m²

    DESIGN CRITERIA:
    - Design code: EN 1993-1-1 (Eurocode 3)
    - National annex: UK
    - Deflection limit: Span/200
    - Fire resistance: R30
    """

    print("\nInput description:")
    print("  ✓ Complete geometry specification")
    print("  ✓ All structural elements defined")
    print("  ✓ Foundation details")
    print("  ✓ Connection specifications")
    print("  ✓ Load cases")
    print("  ✓ Design criteria")

    # This would generate a comprehensive model
    # result = generator.from_text(description, config=config)

    print("\nExpected model complexity:")
    print("  - 22 portal frames")
    print("  - 44 columns with base plates")
    print("  - 44 rafters (22 left + 22 right)")
    print("  - ~200 purlins")
    print("  - ~150 side rails")
    print("  - 20+ bracing bays")
    print("  - 300+ connections")

    print("\nProcessing time estimate: ~2-3 minutes")
    print("Generated C# code size: ~1000 lines")


# Example 5: Batch processing
def example_batch_processing():
    """
    Process multiple buildings in batch
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Batch Processing")
    print("=" * 60)

    buildings = [
        {
            "name": "Warehouse A",
            "description": "50m x 30m warehouse, 12m high, 10m spacing",
            "output": "output/warehouse_a"
        },
        {
            "name": "Warehouse B",
            "description": "60m x 40m warehouse, 15m high, 12m spacing",
            "output": "output/warehouse_b"
        },
        {
            "name": "Office Building",
            "description": "30m x 20m office, 4 floors @ 3.5m, 6m spacing",
            "output": "output/office"
        }
    ]

    print(f"\nProcessing {len(buildings)} buildings...")

    # from src.main import TeklaAIGenerator
    # generator = TeklaAIGenerator()

    for i, building in enumerate(buildings, 1):
        print(f"\n[{i}/{len(buildings)}] {building['name']}")
        print(f"  Description: {building['description']}")

        # result = generator.from_text(building['description'])
        # result.save(building['output'])

        print(f"  ✓ Generated and saved to {building['output']}")

    print("\n✓ Batch processing complete!")
    print(f"  Total buildings: {len(buildings)}")
    print(f"  Output directory: output/")


# Main execution
if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║         AI-Powered Tekla Model Generator                   ║")
    print("║              Usage Examples                                ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n")

    # Run all examples
    example_text_to_model()
    example_pdf_to_model()
    example_iterative_refinement()
    example_advanced_usage()
    example_batch_processing()

    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("\n1. Set up API keys in .env file")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Implement the core modules following IMPLEMENTATION_GUIDE.md")
    print("4. Test with simple examples first")
    print("5. Gradually add more complex features")
    print("\nFor detailed implementation:")
    print("  - See ARCHITECTURE.md for system design")
    print("  - See PIPELINE.md for data flow")
    print("  - See IMPLEMENTATION_GUIDE.md for step-by-step setup")
    print("\n" + "=" * 60)
    print("\n")
