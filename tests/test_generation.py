"""
Tests for code generation
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from schema import SchemaGenerator, BuildingSchema
from code_generation import TeklaCodeGenerator


def test_schema_generation():
    """Test schema generation"""

    test_data = {
        "dimensions": {"length": 30000, "width": 20000, "height": 8000},
        "grid": {"x_spacing": 10000, "y_spacing": 10000, "x_count": 3, "y_count": 2},
        "columns": {"profile": "HEA300", "material": "S355"}
    }

    gen = SchemaGenerator()
    schema = gen.generate(test_data)

    assert isinstance(schema, BuildingSchema)
    assert len(schema.elements) > 0


def test_code_generation():
    """Test Tekla code generation"""

    # Create simple schema
    from schema.models import GridSystem, GridLine, Point3D

    grid = GridSystem(
        x_lines=[GridLine(label="1", coordinate=0), GridLine(label="2", coordinate=8000)],
        y_lines=[GridLine(label="A", coordinate=0), GridLine(label="B", coordinate=6000)]
    )

    from schema import BuildingMetadata

    schema = BuildingSchema(
        metadata=BuildingMetadata(),
        grid=grid,
        elements=[]
    )

    gen = TeklaCodeGenerator()
    code = gen.generate(schema)

    assert "using Tekla.Structures" in code
    assert "CreateGrid" in code


### TODO: USER MUST FILL THIS SECTION
# Add more tests


if __name__ == "__main__":
    pytest.main([__file__])
