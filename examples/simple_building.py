"""
Example: Simple Building Generation
Generate a simple warehouse from text description
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from input_processing import TextProcessor
from schema import SchemaGenerator, SchemaValidator
from code_generation import TeklaCodeGenerator
from utils import ensure_dir

def main():
    """Generate simple warehouse"""

    print("=" * 60)
    print("Simple Building Example")
    print("=" * 60)

    # Text description
    description = """
    Create an industrial warehouse:
    - 40 meters long x 30 meters wide
    - 10 meter eave height
    - 8 meter column spacing in both directions
    - UC305x305x198 columns, S355 steel
    - UB457x191x74 roof beams
    - Simple base plates with 4xM24 bolts
    """

    print("\nStep 1: Processing text description...")
    text_proc = TextProcessor()
    extracted = text_proc.process(description)
    print(f"✓ Extracted {len(extracted)} data fields")

    print("\nStep 2: Generating schema...")
    schema_gen = SchemaGenerator()
    schema = schema_gen.generate(extracted)
    print(f"✓ Schema created with {len(schema.elements)} elements")

    print("\nStep 3: Validating schema...")
    validator = SchemaValidator()
    is_valid, warnings = validator.validate(schema)
    print(f"✓ Validation: {'PASSED' if is_valid else 'FAILED'}")
    for warning in warnings:
        print(f"  [{warning.severity}] {warning.message}")

    print("\nStep 4: Generating Tekla code...")
    code_gen = TeklaCodeGenerator()
    code = code_gen.generate(schema)
    print(f"✓ Generated {len(code.split(chr(10)))} lines of C# code")

    # Save outputs
    output_dir = Path(__file__).parent.parent / "output" / "simple_building"
    ensure_dir(output_dir)

    with open(output_dir / "schema.json", 'w') as f:
        f.write(schema.model_dump_json(indent=2))

    with open(output_dir / "TeklaModel.cs", 'w') as f:
        f.write(code)

    print(f"\n✓ Files saved to: {output_dir}")
    print("\nTo compile and run:")
    print(f"  cd {output_dir}")
    print("  dotnet build TeklaModel.cs")
    print("  dotnet run")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
