"""
Connection data models
Defines bolted and welded connections
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal, Dict, Any
from enum import Enum


class ConnectionType(str, Enum):
    """Type of connection"""
    BASE_PLATE = "base_plate"
    MOMENT = "moment"
    SIMPLE_SHEAR = "simple_shear"
    SPLICE = "splice"
    BRACING = "bracing"
    EAVE = "eave"
    APEX = "apex"
    PURLIN = "purlin"
    CUSTOM = "custom"


class BoltGrade(str, Enum):
    """Bolt grade"""
    GRADE_4_6 = "4.6"
    GRADE_4_8 = "4.8"
    GRADE_8_8 = "8.8"
    GRADE_10_9 = "10.9"


class WeldType(str, Enum):
    """Type of weld"""
    FILLET = "fillet"
    BUTT = "butt"
    PLUG = "plug"
    SLOT = "slot"


class BoltSpecification(BaseModel):
    """
    Bolt specification

    Attributes:
        size: Bolt diameter (e.g., "M24")
        grade: Bolt grade
        quantity: Number of bolts
        pattern: Bolt pattern description
    """
    size: str = Field(..., description="Bolt size (e.g., M24)")
    grade: BoltGrade = Field(default=BoltGrade.GRADE_8_8, description="Bolt grade")
    quantity: int = Field(..., description="Number of bolts")
    pattern: Optional[str] = Field(None, description="Bolt pattern (rectangular, circular, etc.)")
    spacing: Optional[float] = Field(None, description="Bolt spacing in mm")

    @validator('quantity')
    def validate_quantity(cls, v):
        """Ensure quantity is positive"""
        if v < 1:
            raise ValueError("Bolt quantity must be at least 1")
        return v

    @validator('size')
    def validate_size(cls, v):
        """Validate bolt size format"""
        if not v.startswith('M'):
            raise ValueError("Bolt size must start with 'M' (e.g., M24)")
        return v.upper()

    def get_diameter(self) -> int:
        """Extract bolt diameter in mm"""
        return int(self.size[1:])

    class Config:
        json_schema_extra = {
            "example": {
                "size": "M24",
                "grade": "8.8",
                "quantity": 4,
                "pattern": "rectangular",
                "spacing": 80
            }
        }


class WeldSpecification(BaseModel):
    """
    Weld specification

    Attributes:
        type: Weld type
        size: Weld size in mm
        length: Weld length in mm (if applicable)
        all_around: Whether weld goes all around
    """
    type: WeldType = Field(..., description="Weld type")
    size: float = Field(..., description="Weld size in mm")
    length: Optional[float] = Field(None, description="Weld length in mm")
    all_around: bool = Field(default=False, description="Weld all around")
    grade: Optional[str] = Field(None, description="Weld grade/specification")

    @validator('size')
    def validate_size(cls, v):
        """Ensure weld size is positive"""
        if v <= 0:
            raise ValueError("Weld size must be positive")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "type": "fillet",
                "size": 6,
                "all_around": True,
                "grade": "S355"
            }
        }


class Connection(BaseModel):
    """
    Structural connection definition

    Attributes:
        id: Unique connection ID
        type: Connection type
        primary_element: Primary element ID
        secondary_elements: List of secondary element IDs
        bolts: Bolt specification (if bolted)
        welds: Weld specifications (if welded)
        parameters: Additional parameters
        notes: Connection notes
    """
    id: str = Field(..., description="Unique connection ID")
    type: ConnectionType = Field(..., description="Connection type")
    primary_element: str = Field(..., description="Primary element ID")
    secondary_elements: List[str] = Field(default_factory=list, description="Secondary element IDs")
    bolts: Optional[BoltSpecification] = Field(None, description="Bolt specification")
    welds: List[WeldSpecification] = Field(default_factory=list, description="Weld specifications")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters")
    notes: Optional[str] = Field(None, description="Connection notes")

    def is_bolted(self) -> bool:
        """Check if connection is bolted"""
        return self.bolts is not None

    def is_welded(self) -> bool:
        """Check if connection is welded"""
        return len(self.welds) > 0

    def is_hybrid(self) -> bool:
        """Check if connection uses both bolts and welds"""
        return self.is_bolted() and self.is_welded()

    class Config:
        json_schema_extra = {
            "example": {
                "id": "CONN-BP-1",
                "type": "base_plate",
                "primary_element": "COL-A1",
                "secondary_elements": [],
                "bolts": {
                    "size": "M30",
                    "grade": "8.8",
                    "quantity": 4,
                    "pattern": "rectangular"
                },
                "parameters": {
                    "plate_thickness": 25,
                    "plate_grade": "S355"
                }
            }
        }


class ConnectionLibrary(BaseModel):
    """
    Library of standard connections

    Attributes:
        name: Library name
        connections: List of connection templates
    """
    name: str = Field(..., description="Library name")
    connections: List[Connection] = Field(default_factory=list, description="Connection templates")

    def get_connection(self, conn_id: str) -> Optional[Connection]:
        """Find connection by ID"""
        return next((c for c in self.connections if c.id == conn_id), None)

    def add_connection(self, connection: Connection):
        """Add connection to library"""
        self.connections.append(connection)


### TODO: USER MUST FILL THIS SECTION
# Add custom connection types here
# Examples:
# - Special moment connections
# - Proprietary connections
# - Non-standard details
# Create connection templates for common cases


if __name__ == "__main__":
    # Test connection models
    base_plate = Connection(
        id="BP-Standard-4M30",
        type=ConnectionType.BASE_PLATE,
        primary_element="COL-1",
        bolts=BoltSpecification(
            size="M30",
            grade=BoltGrade.GRADE_8_8,
            quantity=4,
            pattern="rectangular"
        ),
        parameters={
            "plate_thickness": 25,
            "plate_width": 450,
            "plate_length": 450,
            "plate_grade": "S355"
        }
    )

    print(f"Base Plate Connection:\n{base_plate.model_dump_json(indent=2)}")
    print(f"\nIs bolted: {base_plate.is_bolted()}")
    print(f"Is welded: {base_plate.is_welded()}")
