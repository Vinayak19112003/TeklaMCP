"""
Load case data models
Defines structural loads and load combinations
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from enum import Enum


class LoadType(str, Enum):
    """Type of load"""
    DEAD = "dead"
    LIVE = "live"
    WIND = "wind"
    SNOW = "snow"
    SEISMIC = "seismic"
    TEMPERATURE = "temperature"
    IMPOSED = "imposed"


class LoadApplication(str, Enum):
    """How load is applied"""
    POINT = "point"
    LINE = "line"
    AREA = "area"
    VOLUME = "volume"


class LoadCase(BaseModel):
    """
    Single load case definition

    Attributes:
        name: Load case name
        type: Type of load
        magnitude: Load magnitude
        unit: Load unit
        application: How load is applied
        location: Where load is applied
    """
    name: str = Field(..., description="Load case name")
    type: LoadType = Field(..., description="Load type")
    magnitude: float = Field(..., description="Load magnitude")
    unit: str = Field(..., description="Load unit (kN, kN/m, kN/m²)")
    application: LoadApplication = Field(..., description="Load application type")
    location: Optional[str] = Field(None, description="Load location description")
    direction: Optional[List[float]] = Field(None, description="Load direction vector")

    @validator('magnitude')
    def validate_magnitude(cls, v):
        """Ensure magnitude is positive"""
        if v < 0:
            raise ValueError("Load magnitude must be positive")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dead Load",
                "type": "dead",
                "magnitude": 0.5,
                "unit": "kN/m²",
                "application": "area",
                "location": "Roof",
                "direction": [0, 0, -1]
            }
        }


class LoadCombination(BaseModel):
    """
    Load combination definition

    Attributes:
        name: Combination name
        load_cases: List of load case names
        factors: Load factors for each case
        combination_type: ULS or SLS
    """
    name: str = Field(..., description="Combination name")
    load_cases: List[str] = Field(..., description="Load case names")
    factors: List[float] = Field(..., description="Load factors")
    combination_type: Literal["ULS", "SLS"] = Field(..., description="Ultimate or Serviceability")

    @validator('factors')
    def validate_factors(cls, v, values):
        """Ensure factors match load cases"""
        if 'load_cases' in values and len(v) != len(values['load_cases']):
            raise ValueError("Number of factors must match number of load cases")
        return v

    def get_total_factor(self) -> float:
        """Calculate total load factor"""
        return sum(self.factors)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "1.35DL + 1.5LL",
                "load_cases": ["Dead Load", "Live Load"],
                "factors": [1.35, 1.5],
                "combination_type": "ULS"
            }
        }


class LoadingSchedule(BaseModel):
    """
    Complete loading schedule

    Attributes:
        design_code: Design code used
        load_cases: List of load cases
        combinations: List of load combinations
    """
    design_code: str = Field(default="EC1", description="Design code (EC1, ASCE, etc.)")
    load_cases: List[LoadCase] = Field(default_factory=list, description="Load cases")
    combinations: List[LoadCombination] = Field(default_factory=list, description="Load combinations")

    def get_load_case(self, name: str) -> Optional[LoadCase]:
        """
        Find load case by name

        Args:
            name: Load case name

        Returns:
            LoadCase or None
        """
        return next((lc for lc in self.load_cases if lc.name == name), None)

    def add_load_case(self, load_case: LoadCase):
        """Add load case to schedule"""
        self.load_cases.append(load_case)

    def add_combination(self, combination: LoadCombination):
        """Add load combination to schedule"""
        self.combinations.append(combination)


### TODO: USER MUST FILL THIS SECTION
# Add custom load types or special loading conditions here
# Examples:
# - Dynamic loads
# - Fatigue loads
# - Construction loads
# - Special seismic loads


if __name__ == "__main__":
    # Test load models
    schedule = LoadingSchedule(design_code="EC1")

    dead_load = LoadCase(
        name="Dead Load",
        type=LoadType.DEAD,
        magnitude=0.5,
        unit="kN/m²",
        application=LoadApplication.AREA,
        location="Roof"
    )

    live_load = LoadCase(
        name="Live Load",
        type=LoadType.LIVE,
        magnitude=2.5,
        unit="kN/m²",
        application=LoadApplication.AREA,
        location="Roof"
    )

    schedule.add_load_case(dead_load)
    schedule.add_load_case(live_load)

    combination = LoadCombination(
        name="1.35DL + 1.5LL",
        load_cases=["Dead Load", "Live Load"],
        factors=[1.35, 1.5],
        combination_type="ULS"
    )

    schedule.add_combination(combination)

    print(f"Loading Schedule:\n{schedule.model_dump_json(indent=2)}")
