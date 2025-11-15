"""
Example: Generate from PDF Drawing
Process a PDF structural drawing
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from input_processing import PDFProcessor
from schema import SchemaGenerator
from code_generation import TeklaCodeGenerator
from utils import ensure_dir


def main(pdf_path: str):
    """Generate from PDF"""

    print("=" * 60)
    print("PDF to Model Example")
    print("=" * 60)

    print(f"\nProcessing PDF: {pdf_path}")

    # Process PDF
    pdf_proc = PDFProcessor()
    extracted = pdf_proc.process(pdf_path)
    print(f"✓ Extracted data from {extracted.get('pages', 1)} pages")

    # Generate schema
    schema_gen = SchemaGenerator()
    schema = schema_gen.generate(extracted)
    print(f"✓ Schema with {len(schema.elements)} elements")

    # Generate code
    code_gen = TeklaCodeGenerator()
    code = code_gen.generate(schema)
    print(f"✓ Generated code")

    # Save
    output_dir = Path(__file__).parent.parent / "output" / "from_pdf"
    ensure_dir(output_dir)

    with open(output_dir / "TeklaModel.cs", 'w') as f:
        f.write(code)

    print(f"\n✓ Saved to: {output_dir}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python from_pdf.py <path_to_pdf>")
