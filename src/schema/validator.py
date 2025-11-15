"""
Schema Validator
Validates building schemas for correctness and engineering constraints
"""

from typing import List, Dict, Tuple
from .schema_generator import BuildingSchema
from .models import StructuralElement, ElementType
from ..utils import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class ValidationWarning:
    """Validation warning"""
    def __init__(self, severity: str, message: str, element_id: str = None):
        self.severity = severity  # "info", "warning", "critical"
        self.message = message
        self.element_id = element_id


class SchemaValidator:
    """
    Validates BuildingSchema for correctness
    """

    def __init__(self):
        self.logger = logger
        self.warnings: List[ValidationWarning] = []

    def validate(self, schema: BuildingSchema) -> Tuple[bool, List[ValidationWarning]]:
        """
        Main validation method

        Args:
            schema: BuildingSchema to validate

        Returns:
            (is_valid, warnings)
        """
        self.warnings = []

        self.logger.info("Starting schema validation")

        try:
            # Run all validations
            self._validate_grid(schema)
            self._validate_elements(schema)
            self._validate_connections(schema)
            self._validate_engineering_constraints(schema)

            # Check for critical warnings
            critical = [w for w in self.warnings if w.severity == "critical"]

            if critical:
                self.logger.error("Validation failed", critical_count=len(critical))
                return False, self.warnings
            else:
                self.logger.info("Validation passed", warning_count=len(self.warnings))
                return True, self.warnings

        except Exception as e:
            self.logger.error("Validation error", error=str(e))
            raise ValidationError(f"Validation failed: {str(e)}")

    def _validate_grid(self, schema: BuildingSchema):
        """Validate grid system"""
        grid = schema.grid

        # Check minimum grid lines
        if len(grid.x_lines) < 2:
            self.warnings.append(
                ValidationWarning("critical", "Grid must have at least 2 X lines")
            )

        if len(grid.y_lines) < 2:
            self.warnings.append(
                ValidationWarning("critical", "Grid must have at least 2 Y lines")
            )

        # Check grid spacing
        for i in range(len(grid.x_lines) - 1):
            spacing = grid.x_lines[i + 1].coordinate - grid.x_lines[i].coordinate
            if spacing < 1000:  # Less than 1m
                self.warnings.append(
                    ValidationWarning("warning", f"Very small X spacing: {spacing}mm")
                )
            elif spacing > 50000:  # More than 50m
                self.warnings.append(
                    ValidationWarning("warning", f"Very large X spacing: {spacing}mm")
                )

    def _validate_elements(self, schema: BuildingSchema):
        """Validate structural elements"""

        # Check for elements
        if len(schema.elements) == 0:
            self.warnings.append(
                ValidationWarning("critical", "No structural elements defined")
            )
            return

        # Validate each element
        for elem in schema.elements:
            self._validate_element(elem)

        # Check for overlapping elements
        self._check_overlapping_elements(schema.elements)

    def _validate_element(self, elem: StructuralElement):
        """Validate single element"""

        # Check length
        length = elem.get_length()

        if length < 100:  # Less than 10cm
            self.warnings.append(
                ValidationWarning("warning", f"Very short element: {length}mm", elem.id)
            )

        # Check beam spans
        if elem.type == ElementType.BEAM:
            if length > 25000:  # More than 25m
                self.warnings.append(
                    ValidationWarning(
                        "warning",
                        f"Long beam span: {length}mm - verify design",
                        elem.id
                    )
                )

        # Check column heights
        if elem.type == ElementType.COLUMN:
            if length > 20000:  # More than 20m
                self.warnings.append(
                    ValidationWarning(
                        "warning",
                        f"Tall column: {length}mm - check buckling",
                        elem.id
                    )
                )

        ### TODO: USER MUST FILL THIS SECTION
        # Add custom element validation rules:
        # - Profile size checks
        # - Material compatibility
        # - Connection requirements
        # - Design code specific rules

    def _check_overlapping_elements(self, elements: List[StructuralElement]):
        """Check for overlapping/coincident elements"""
        # Simple check - compare start and end points
        positions = {}

        for elem in elements:
            key = (
                round(elem.start_point.x),
                round(elem.start_point.y),
                round(elem.start_point.z),
                round(elem.end_point.x),
                round(elem.end_point.y),
                round(elem.end_point.z)
            )

            if key in positions:
                self.warnings.append(
                    ValidationWarning(
                        "warning",
                        f"Potential overlap: {elem.id} and {positions[key]}",
                        elem.id
                    )
                )
            else:
                positions[key] = elem.id

    def _validate_connections(self, schema: BuildingSchema):
        """Validate connections"""

        # Check that referenced elements exist
        element_ids = {e.id for e in schema.elements}

        for conn in schema.connections:
            if conn.primary_element not in element_ids:
                self.warnings.append(
                    ValidationWarning(
                        "critical",
                        f"Connection {conn.id} references non-existent element {conn.primary_element}",
                        conn.id
                    )
                )

            for sec_elem in conn.secondary_elements:
                if sec_elem not in element_ids:
                    self.warnings.append(
                        ValidationWarning(
                            "critical",
                            f"Connection {conn.id} references non-existent element {sec_elem}",
                            conn.id
                        )
                    )

    def _validate_engineering_constraints(self, schema: BuildingSchema):
        """Validate engineering constraints"""

        ### TODO: USER MUST FILL THIS SECTION
        # Add engineering validation rules:
        # - Structural stability checks
        # - Load path validation
        # - Design code compliance
        # - Material strength checks
        # Example:
        # if not self._check_lateral_stability(schema):
        #     self.warnings.append(ValidationWarning("critical", "No lateral bracing"))

        pass

    def get_validation_summary(self) -> Dict:
        """
        Get validation summary

        Returns:
            Dictionary with counts by severity
        """
        summary = {
            "total": len(self.warnings),
            "critical": len([w for w in self.warnings if w.severity == "critical"]),
            "warning": len([w for w in self.warnings if w.severity == "warning"]),
            "info": len([w for w in self.warnings if w.severity == "info"])
        }

        return summary


if __name__ == "__main__":
    # Test validator
    from .schema_generator import SchemaGenerator

    test_data = {
        "building_type": "test",
        "dimensions": {"length": 30000, "width": 20000, "height": 8000},
        "grid": {"x_spacing": 10000, "y_spacing": 10000, "x_count": 3, "y_count": 2},
        "columns": {"profile": "HEA300", "material": "S355"},
        "beams": {"profile": "IPE400", "material": "S355"}
    }

    generator = SchemaGenerator()
    schema = generator.generate(test_data)

    validator = SchemaValidator()
    is_valid, warnings = validator.validate(schema)

    print(f"Validation: {'✓ PASSED' if is_valid else '✗ FAILED'}")
    print(f"Summary: {validator.get_validation_summary()}")

    for warning in warnings:
        print(f"  [{warning.severity.upper()}] {warning.message}")
