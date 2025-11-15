"""
Schema Generator
Converts extracted data into validated BuildingSchema
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

from .models import (
    GridSystem, GridLine,
    StructuralElement, ElementType, Point3D, SectionProfile, Material,
    LoadCase, LoadingSchedule,
    Connection, BoltSpecification
)
from ..utils import get_logger

logger = get_logger(__name__)


class BuildingMetadata(BaseModel):
    """Building metadata"""
    name: str = Field(default="Generated Building", description="Project name")
    project_number: Optional[str] = Field(None, description="Project number")
    design_code: str = Field(default="EC3", description="Design code")
    units: str = Field(default="mm", description="Units")
    created: str = Field(default_factory=lambda: datetime.now().isoformat())
    ai_generated: bool = Field(default=True)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class BuildingSchema(BaseModel):
    """
    Complete building schema
    Main data structure for entire building model
    """
    metadata: BuildingMetadata
    grid: GridSystem
    elements: List[StructuralElement] = Field(default_factory=list)
    connections: List[Connection] = Field(default_factory=list)
    loads: LoadingSchedule = Field(default_factory=LoadingSchedule)
    materials: Dict = Field(default_factory=dict)

    def get_elements_by_type(self, element_type: ElementType) -> List[StructuralElement]:
        """Get all elements of specific type"""
        return [e for e in self.elements if e.type == element_type]

    def get_element_count(self) -> Dict[str, int]:
        """Get count of each element type"""
        counts = {}
        for elem in self.elements:
            counts[elem.type.value] = counts.get(elem.type.value, 0) + 1
        return counts

    class Config:
        json_schema_extra = {
            "example": {
                "metadata": {"name": "Test Building", "design_code": "EC3"},
                "grid": {"x_lines": [], "y_lines": []},
                "elements": [],
                "connections": []
            }
        }


class SchemaGenerator:
    """
    Generate BuildingSchema from extracted data
    """

    def __init__(self):
        self.logger = logger

    def generate(self, extracted_data: Dict) -> BuildingSchema:
        """
        Main method to generate complete schema

        Args:
            extracted_data: Dictionary from extraction layer

        Returns:
            Validated BuildingSchema
        """
        self.logger.info("Generating building schema", data_keys=list(extracted_data.keys()))

        try:
            # Generate each component
            metadata = self._generate_metadata(extracted_data)
            grid = self._generate_grid(extracted_data)
            elements = self._generate_elements(extracted_data, grid)
            connections = self._generate_connections(extracted_data, elements)
            loads = self._generate_loads(extracted_data)
            materials = self._generate_materials(extracted_data)

            schema = BuildingSchema(
                metadata=metadata,
                grid=grid,
                elements=elements,
                connections=connections,
                loads=loads,
                materials=materials
            )

            self.logger.info("Schema generated successfully",
                           element_count=len(elements),
                           connection_count=len(connections))

            return schema

        except Exception as e:
            self.logger.error("Schema generation failed", error=str(e))
            raise

    def _generate_metadata(self, data: Dict) -> BuildingMetadata:
        """Generate metadata from extracted data"""
        return BuildingMetadata(
            name=data.get("building_type", "Generated Building"),
            design_code=data.get("design_code", "EC3"),
            confidence=data.get("confidence", 0.85)
        )

    def _generate_grid(self, data: Dict) -> GridSystem:
        """
        Generate grid system

        Args:
            data: Extracted data

        Returns:
            GridSystem object
        """
        grid_data = data.get("grid", {})
        dimensions = data.get("dimensions", {})

        # Generate X-axis gridlines
        x_lines = self._generate_grid_lines(
            grid_data.get("x_spacing"),
            grid_data.get("x_count", 1),
            dimensions.get("length", 0),
            axis="x"
        )

        # Generate Y-axis gridlines
        y_lines = self._generate_grid_lines(
            grid_data.get("y_spacing"),
            grid_data.get("y_count", 1),
            dimensions.get("width", 0),
            axis="y"
        )

        # Generate Z-levels
        z_levels = []
        if "height" in dimensions:
            z_levels.append(GridLine(label="Ground", coordinate=0))
            z_levels.append(GridLine(label="Roof", coordinate=dimensions["height"]))

        return GridSystem(
            name="MainGrid",
            x_lines=x_lines,
            y_lines=y_lines,
            z_levels=z_levels
        )

    def _generate_grid_lines(self, spacing, count, total_length, axis="x") -> List[GridLine]:
        """
        Generate grid lines for one axis

        Args:
            spacing: Spacing value(s)
            count: Number of bays
            total_length: Total length
            axis: "x" or "y"

        Returns:
            List of GridLine objects
        """
        lines = []

        if spacing is None and total_length > 0 and count > 0:
            # Calculate uniform spacing from total length
            spacing = total_length / count

        if isinstance(spacing, (int, float)):
            # Uniform spacing
            for i in range(count + 1):
                label = str(i + 1) if axis == "x" else chr(65 + i)  # Numbers or letters
                lines.append(GridLine(label=label, coordinate=i * spacing))

        elif isinstance(spacing, list):
            # Variable spacing
            coord = 0
            for i, space in enumerate(spacing):
                label = str(i + 1) if axis == "x" else chr(65 + i)
                lines.append(GridLine(label=label, coordinate=coord))
                coord += space
            # Add final line
            label = str(len(spacing) + 1) if axis == "x" else chr(65 + len(spacing))
            lines.append(GridLine(label=label, coordinate=coord))

        return lines

    def _generate_elements(self, data: Dict, grid: GridSystem) -> List[StructuralElement]:
        """
        Generate all structural elements

        Args:
            data: Extracted data
            grid: Grid system

        Returns:
            List of StructuralElement objects
        """
        elements = []

        # Generate columns
        columns = self._generate_columns(data, grid)
        elements.extend(columns)

        # Generate beams
        beams = self._generate_beams(data, grid)
        elements.extend(beams)

        ### TODO: USER MUST FILL THIS SECTION
        # Add custom element generation logic:
        # - Bracing members
        # - Purlins
        # - Special elements
        # Use data from extracted_data and grid system

        return elements

    def _generate_columns(self, data: Dict, grid: GridSystem) -> List[StructuralElement]:
        """Generate columns at grid intersections"""
        columns = []
        column_data = data.get("columns", {})

        profile = column_data.get("profile", "UC305x305x198")
        material = column_data.get("material", "S355")
        height = data.get("dimensions", {}).get("height", 8000)

        element_id = 1

        for x_line in grid.x_lines:
            for y_line in grid.y_lines:
                col = StructuralElement(
                    id=f"COL-{element_id}",
                    type=ElementType.COLUMN,
                    profile=SectionProfile(profile_string=profile),
                    material=Material(material_string=material, material_type="steel"),
                    start_point=Point3D(x=x_line.coordinate, y=y_line.coordinate, z=0),
                    end_point=Point3D(x=x_line.coordinate, y=y_line.coordinate, z=height),
                    grid_reference=f"{y_line.label}-{x_line.label}"
                )
                columns.append(col)
                element_id += 1

        return columns

    def _generate_beams(self, data: Dict, grid: GridSystem) -> List[StructuralElement]:
        """Generate beams between columns"""
        beams = []
        beam_data = data.get("beams", {})

        profile = beam_data.get("profile", "IPE400")
        material = beam_data.get("material", "S355")
        roof_level = data.get("dimensions", {}).get("height", 8000)

        element_id = 1

        # X-direction beams
        for y_line in grid.y_lines:
            for i in range(len(grid.x_lines) - 1):
                beam = StructuralElement(
                    id=f"BEAM-X-{element_id}",
                    type=ElementType.BEAM,
                    profile=SectionProfile(profile_string=profile),
                    material=Material(material_string=material, material_type="steel"),
                    start_point=Point3D(
                        x=grid.x_lines[i].coordinate,
                        y=y_line.coordinate,
                        z=roof_level
                    ),
                    end_point=Point3D(
                        x=grid.x_lines[i + 1].coordinate,
                        y=y_line.coordinate,
                        z=roof_level
                    )
                )
                beams.append(beam)
                element_id += 1

        # Y-direction beams
        for x_line in grid.x_lines:
            for i in range(len(grid.y_lines) - 1):
                beam = StructuralElement(
                    id=f"BEAM-Y-{element_id}",
                    type=ElementType.BEAM,
                    profile=SectionProfile(profile_string=profile),
                    material=Material(material_string=material, material_type="steel"),
                    start_point=Point3D(
                        x=x_line.coordinate,
                        y=grid.y_lines[i].coordinate,
                        z=roof_level
                    ),
                    end_point=Point3D(
                        x=x_line.coordinate,
                        y=grid.y_lines[i + 1].coordinate,
                        z=roof_level
                    )
                )
                beams.append(beam)
                element_id += 1

        return beams

    def _generate_connections(self, data: Dict, elements: List[StructuralElement]) -> List[Connection]:
        """Generate connections"""
        connections = []
        column_data = data.get("columns", {})

        # Generate base plates for all columns
        columns = [e for e in elements if e.type == ElementType.COLUMN]

        for col in columns:
            conn = Connection(
                id=f"BP-{col.id}",
                type="base_plate",
                primary_element=col.id,
                bolts=BoltSpecification(
                    size=column_data.get("bolts", "M24").replace("x", ""),
                    quantity=int(column_data.get("bolts", "4xM24").split("x")[0]) if "x" in column_data.get("bolts", "4xM24") else 4
                ),
                parameters={
                    "plate_thickness": 25,
                    "bolt_grade": "8.8"
                }
            )
            connections.append(conn)

        return connections

    def _generate_loads(self, data: Dict) -> LoadingSchedule:
        """Generate loading schedule"""
        loads_data = data.get("loads", {})

        schedule = LoadingSchedule(design_code=data.get("design_code", "EC1"))

        ### TODO: USER MUST FILL THIS SECTION
        # Parse and add load cases from extracted data
        # Example:
        # if "dead" in loads_data:
        #     schedule.add_load_case(LoadCase(...))

        return schedule

    def _generate_materials(self, data: Dict) -> Dict:
        """Generate materials dictionary"""
        materials = {}

        if "materials" in data:
            materials = data["materials"]
        else:
            # Default materials
            materials["steel"] = {
                "grade": data.get("columns", {}).get("material", "S355"),
                "type": "steel"
            }

        return materials


if __name__ == "__main__":
    # Test schema generator
    test_data = {
        "building_type": "warehouse",
        "dimensions": {
            "length": 40000,
            "width": 30000,
            "height": 10000
        },
        "grid": {
            "x_spacing": 8000,
            "y_spacing": 10000,
            "x_count": 5,
            "y_count": 3
        },
        "columns": {
            "profile": "HEA300",
            "material": "S355",
            "bolts": "4xM24"
        },
        "beams": {
            "profile": "IPE400",
            "material": "S355"
        }
    }

    generator = SchemaGenerator()
    schema = generator.generate(test_data)

    print(f"Generated schema with {len(schema.elements)} elements")
    print(f"Element counts: {schema.get_element_count()}")
