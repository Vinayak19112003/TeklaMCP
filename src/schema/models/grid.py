"""
Grid system data models
Defines grid lines, levels, and grid system structure
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class GridLineType(str, Enum):
    """Type of grid line"""
    X_AXIS = "x_axis"
    Y_AXIS = "y_axis"
    Z_LEVEL = "z_level"


class GridLine(BaseModel):
    """
    Single grid line definition

    Attributes:
        label: Grid line label (e.g., "1", "A", "Ground")
        coordinate: Position in millimeters
        line_type: X, Y, or Z axis
    """
    label: str = Field(..., description="Grid line label")
    coordinate: float = Field(..., description="Position in millimeters")
    line_type: Optional[GridLineType] = Field(None, description="Type of grid line")

    @validator('coordinate')
    def validate_coordinate(cls, v):
        """Ensure coordinate is non-negative"""
        if v < 0:
            raise ValueError("Coordinate must be non-negative")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "label": "A",
                "coordinate": 0,
                "line_type": "y_axis"
            }
        }


class GridSpacing(BaseModel):
    """
    Grid spacing definition

    Attributes:
        uniform: Whether spacing is uniform
        spacing: Spacing value(s) in mm
    """
    uniform: bool = Field(True, description="Whether spacing is uniform")
    spacing: List[float] = Field(..., description="Spacing values in mm")

    @validator('spacing')
    def validate_spacing(cls, v):
        """Ensure all spacing values are positive"""
        if any(s <= 0 for s in v):
            raise ValueError("All spacing values must be positive")
        return v


class GridSystem(BaseModel):
    """
    Complete grid system definition

    Attributes:
        name: Grid system name
        x_lines: X-axis grid lines
        y_lines: Y-axis grid lines
        z_levels: Z-axis levels (elevations)
        origin: Grid origin point (x, y, z) in mm
    """
    name: str = Field(default="MainGrid", description="Grid system name")
    x_lines: List[GridLine] = Field(..., description="X-axis grid lines")
    y_lines: List[GridLine] = Field(..., description="Y-axis grid lines")
    z_levels: List[GridLine] = Field(default_factory=list, description="Z-axis levels")
    origin: List[float] = Field(default=[0, 0, 0], description="Grid origin (x,y,z) in mm")

    @validator('x_lines', 'y_lines', 'z_levels')
    def validate_sorted(cls, v):
        """Ensure grid lines are sorted by coordinate"""
        if not v:
            return v

        coords = [line.coordinate for line in v]
        if coords != sorted(coords):
            raise ValueError("Grid lines must be sorted by coordinate")

        return v

    @validator('x_lines', 'y_lines')
    def validate_not_empty(cls, v):
        """Ensure at least 2 grid lines"""
        if len(v) < 2:
            raise ValueError("Grid must have at least 2 lines in each direction")
        return v

    def get_dimensions(self) -> dict:
        """
        Calculate grid dimensions

        Returns:
            Dict with length, width, height in mm
        """
        length = max(line.coordinate for line in self.x_lines) if self.x_lines else 0
        width = max(line.coordinate for line in self.y_lines) if self.y_lines else 0
        height = max(line.coordinate for line in self.z_levels) if self.z_levels else 0

        return {
            "length": length,
            "width": width,
            "height": height
        }

    def get_grid_count(self) -> dict:
        """
        Get number of bays in each direction

        Returns:
            Dict with x_bays, y_bays count
        """
        return {
            "x_bays": len(self.x_lines) - 1 if self.x_lines else 0,
            "y_bays": len(self.y_lines) - 1 if self.y_lines else 0,
            "levels": len(self.z_levels) if self.z_levels else 0
        }

    def get_grid_intersection(self, x_label: str, y_label: str, z_label: str = None) -> Optional[List[float]]:
        """
        Get coordinates of grid intersection

        Args:
            x_label: X grid line label
            y_label: Y grid line label
            z_label: Z level label (optional)

        Returns:
            [x, y, z] coordinates or None if not found
        """
        x_coord = next((line.coordinate for line in self.x_lines if line.label == x_label), None)
        y_coord = next((line.coordinate for line in self.y_lines if line.label == y_label), None)

        if x_coord is None or y_coord is None:
            return None

        if z_label:
            z_coord = next((line.coordinate for line in self.z_levels if line.label == z_label), 0)
        else:
            z_coord = 0

        return [x_coord, y_coord, z_coord]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "MainGrid",
                "x_lines": [
                    {"label": "1", "coordinate": 0},
                    {"label": "2", "coordinate": 8000},
                    {"label": "3", "coordinate": 16000}
                ],
                "y_lines": [
                    {"label": "A", "coordinate": 0},
                    {"label": "B", "coordinate": 6000}
                ],
                "z_levels": [
                    {"label": "Ground", "coordinate": 0},
                    {"label": "Roof", "coordinate": 8000}
                ]
            }
        }


### TODO: USER MUST FILL THIS SECTION
# If you need custom grid types or special grid configurations:
# - Radial grids
# - Curved grids
# - Non-orthogonal grids
# Define them as additional classes here


if __name__ == "__main__":
    # Test grid models
    grid = GridSystem(
        x_lines=[
            GridLine(label="1", coordinate=0),
            GridLine(label="2", coordinate=8000),
            GridLine(label="3", coordinate=16000),
        ],
        y_lines=[
            GridLine(label="A", coordinate=0),
            GridLine(label="B", coordinate=6000),
        ],
        z_levels=[
            GridLine(label="Ground", coordinate=0),
            GridLine(label="Roof", coordinate=8000),
        ]
    )

    print(f"Grid dimensions: {grid.get_dimensions()}")
    print(f"Grid count: {grid.get_grid_count()}")
    print(f"Intersection A-1: {grid.get_grid_intersection('1', 'A')}")
    print(f"\nGrid JSON:\n{grid.model_dump_json(indent=2)}")
