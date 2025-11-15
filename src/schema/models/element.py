"""
Structural element data models
Defines beams, columns, bracing, and other structural members
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from enum import Enum


class ElementType(str, Enum):
    """Type of structural element"""
    COLUMN = "column"
    BEAM = "beam"
    RAFTER = "rafter"
    PURLIN = "purlin"
    BRACE = "brace"
    FOUNDATION = "foundation"
    PLATE = "plate"
    GUSSET = "gusset"


class Point3D(BaseModel):
    """
    3D point in space

    Attributes:
        x, y, z: Coordinates in millimeters
    """
    x: float = Field(..., description="X coordinate in mm")
    y: float = Field(..., description="Y coordinate in mm")
    z: float = Field(default=0.0, description="Z coordinate in mm")

    def to_list(self) -> List[float]:
        """Convert to list [x, y, z]"""
        return [self.x, self.y, self.z]

    def distance_to(self, other: 'Point3D') -> float:
        """Calculate distance to another point"""
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5

    class Config:
        json_schema_extra = {
            "example": {"x": 0, "y": 0, "z": 8000}
        }


class SectionProfile(BaseModel):
    """
    Section profile definition

    Attributes:
        profile_string: Profile designation (e.g., "HEA300", "UC305x305x198")
        profile_type: Type of profile
    """
    profile_string: str = Field(..., description="Profile designation")
    profile_type: Optional[str] = Field(None, description="Profile type (I, H, UC, UB, etc.)")

    @validator('profile_string')
    def validate_profile(cls, v):
        """Basic validation of profile string"""
        if not v or len(v) < 2:
            raise ValueError("Profile string must be valid")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {"profile_string": "HEA300", "profile_type": "H"}
        }


class Material(BaseModel):
    """
    Material definition

    Attributes:
        material_string: Material designation (e.g., "S355", "C30/37")
        material_type: Type of material
        grade: Material grade
    """
    material_string: str = Field(..., description="Material designation")
    material_type: Literal["steel", "concrete", "timber", "other"] = Field(default="steel")
    grade: Optional[str] = Field(None, description="Material grade")
    fy: Optional[float] = Field(None, description="Yield strength in MPa")
    fu: Optional[float] = Field(None, description="Ultimate strength in MPa")

    class Config:
        json_schema_extra = {
            "example": {
                "material_string": "S355",
                "material_type": "steel",
                "grade": "J2",
                "fy": 355,
                "fu": 510
            }
        }


class StructuralElement(BaseModel):
    """
    Complete structural element definition

    Attributes:
        id: Unique element identifier
        type: Type of element
        profile: Section profile
        material: Material specification
        start_point: Starting point coordinates
        end_point: Ending point coordinates
        rotation: Rotation angle in degrees
        class_: Tekla class number
        notes: Additional notes
    """
    id: str = Field(..., description="Unique element ID")
    type: ElementType = Field(..., description="Element type")
    profile: SectionProfile = Field(..., description="Section profile")
    material: Material = Field(..., description="Material")
    start_point: Point3D = Field(..., description="Start point")
    end_point: Point3D = Field(..., description="End point")
    rotation: float = Field(default=0.0, description="Rotation angle in degrees")
    class_: str = Field(default="1", alias="class", description="Tekla class")
    grid_reference: Optional[str] = Field(None, description="Grid reference (e.g., A-1)")
    notes: Optional[str] = Field(None, description="Additional notes")

    @validator('rotation')
    def validate_rotation(cls, v):
        """Ensure rotation is between 0 and 360"""
        return v % 360

    def get_length(self) -> float:
        """
        Calculate element length

        Returns:
            Length in millimeters
        """
        return self.start_point.distance_to(self.end_point)

    def get_midpoint(self) -> Point3D:
        """
        Calculate element midpoint

        Returns:
            Midpoint coordinates
        """
        return Point3D(
            x=(self.start_point.x + self.end_point.x) / 2,
            y=(self.start_point.y + self.end_point.y) / 2,
            z=(self.start_point.z + self.end_point.z) / 2
        )

    def is_vertical(self, tolerance: float = 1.0) -> bool:
        """
        Check if element is vertical

        Args:
            tolerance: Tolerance in mm

        Returns:
            True if vertical
        """
        horizontal_dist = ((self.end_point.x - self.start_point.x)**2 +
                          (self.end_point.y - self.start_point.y)**2)**0.5
        return horizontal_dist < tolerance

    def is_horizontal(self, tolerance: float = 1.0) -> bool:
        """
        Check if element is horizontal

        Args:
            tolerance: Tolerance in mm

        Returns:
            True if horizontal
        """
        vertical_dist = abs(self.end_point.z - self.start_point.z)
        return vertical_dist < tolerance

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "COL-1",
                "type": "column",
                "profile": {"profile_string": "UC305x305x198"},
                "material": {"material_string": "S355", "material_type": "steel"},
                "start_point": {"x": 0, "y": 0, "z": 0},
                "end_point": {"x": 0, "y": 0, "z": 8000},
                "rotation": 0,
                "class": "1",
                "grid_reference": "A-1"
            }
        }


class ElementGroup(BaseModel):
    """
    Group of related elements

    Attributes:
        name: Group name
        elements: List of element IDs
        description: Group description
    """
    name: str = Field(..., description="Group name")
    elements: List[str] = Field(default_factory=list, description="Element IDs in group")
    description: Optional[str] = Field(None, description="Group description")


### TODO: USER MUST FILL THIS SECTION
# Add custom element types or specialized element classes here
# Examples:
# - Composite beams
# - Castellated beams
# - Pre-stressed elements
# - Special foundations


if __name__ == "__main__":
    # Test element models
    column = StructuralElement(
        id="COL-A1",
        type=ElementType.COLUMN,
        profile=SectionProfile(profile_string="UC305x305x198"),
        material=Material(material_string="S355", material_type="steel"),
        start_point=Point3D(x=0, y=0, z=0),
        end_point=Point3D(x=0, y=0, z=8000),
        grid_reference="A-1"
    )

    print(f"Column length: {column.get_length()}mm")
    print(f"Is vertical: {column.is_vertical()}")
    print(f"Midpoint: {column.get_midpoint()}")
    print(f"\nColumn JSON:\n{column.model_dump_json(indent=2)}")
