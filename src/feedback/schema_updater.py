"""
Schema Updater
Updates building schema based on modifications
"""

from typing import List, Dict
from ..schema import BuildingSchema
from ..utils import get_logger

logger = get_logger(__name__)


class SchemaUpdater:
    """
    Update building schema with modifications
    """

    def __init__(self):
        self.logger = logger

    def apply_modifications(self, schema: BuildingSchema, modifications: List[Dict]) -> BuildingSchema:
        """
        Apply modifications to schema

        Args:
            schema: Current schema
            modifications: List of modifications

        Returns:
            Updated schema
        """
        self.logger.info("Applying modifications", count=len(modifications))

        updated_schema = schema.model_copy(deep=True)

        for mod in modifications:
            self._apply_single_modification(updated_schema, mod)

        return updated_schema

    def _apply_single_modification(self, schema: BuildingSchema, mod: Dict):
        """Apply single modification"""

        target = mod.get("target")
        filter_criteria = mod.get("filter")
        property_name = mod.get("property")
        new_value = mod.get("new_value")

        if target == "columns":
            self._modify_columns(schema, filter_criteria, property_name, new_value)
        elif target == "beams":
            self._modify_beams(schema, filter_criteria, property_name, new_value)

        ### TODO: USER MUST FILL THIS SECTION
        # Add more modification types:
        # - Grid modifications
        # - Connection modifications
        # - Add/remove elements

    def _modify_columns(self, schema, filter_criteria, property_name, new_value):
        """Modify columns"""
        columns = schema.get_elements_by_type("column")

        for col in columns:
            if self._matches_filter(col, filter_criteria):
                if property_name == "profile":
                    col.profile.profile_string = new_value
                elif property_name == "material":
                    col.material.material_string = new_value

    def _modify_beams(self, schema, filter_criteria, property_name, new_value):
        """Modify beams"""
        pass  # Similar to columns

    def _matches_filter(self, element, filter_criteria) -> bool:
        """Check if element matches filter"""
        if filter_criteria == "all":
            return True

        ### TODO: USER MUST FILL THIS SECTION
        # Implement filter matching:
        # - "perimeter" - check if on edge
        # - "interior" - check if not on edge
        # - Grid locations

        return True


if __name__ == "__main__":
    print("Schema Updater ready.")
