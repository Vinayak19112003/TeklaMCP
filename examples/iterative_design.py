"""
Example: Iterative Design
Generate model and apply modifications
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from input_processing import TextProcessor
from schema import SchemaGenerator
from code_generation import TeklaCodeGenerator
from feedback import ModificationParser, SchemaUpdater
from utils import ensure_dir


def main():
    """Iterative design example"""

    print("=" * 60)
    print("Iterative Design Example")
    print("=" * 60)

    # Initial design
    description = """
    30m x 20m warehouse, 8m high,
    6m spacing, HEA300 columns,
    IPE400 beams, S355 steel
    """

    print("\nStep 1: Initial generation...")
    text_proc = TextProcessor()
    extracted = text_proc.process(description)

    schema_gen = SchemaGenerator()
    schema_v1 = schema_gen.generate(extracted)
    print(f"✓ V1: {len(schema_v1.elements)} elements")

    # Modification 1
    print("\nStep 2: Apply modification...")
    feedback_1 = "Change all columns to UC356x406x287"

    mod_parser = ModificationParser()
    modifications = mod_parser.parse(feedback_1, {})

    schema_updater = SchemaUpdater()
    schema_v2 = schema_updater.apply_modifications(schema_v1, modifications)
    print(f"✓ V2: Modified columns")

    # Generate final code
    print("\nStep 3: Generate updated code...")
    code_gen = TeklaCodeGenerator()
    code = code_gen.generate(schema_v2)
    print(f"✓ Code generated")

    # Save
    output_dir = Path(__file__).parent.parent / "output" / "iterative"
    ensure_dir(output_dir)

    with open(output_dir / "TeklaModel.cs", 'w') as f:
        f.write(code)

    print(f"\n✓ Saved to: {output_dir}")


if __name__ == "__main__":
    main()
