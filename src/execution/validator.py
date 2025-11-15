"""
Model Validator
Validates created Tekla model
"""

from ..utils import get_logger

logger = get_logger(__name__)


class ModelValidator:
    """
    Validate Tekla model after creation
    """

    def __init__(self):
        self.logger = logger

    def validate(self) -> bool:
        """
        Validate model

        Returns:
            True if valid
        """
        ### TODO: USER MUST FILL THIS SECTION
        # Add model validation:
        # - Check element count
        # - Check for clashes
        # - Verify connections

        return True


if __name__ == "__main__":
    print("Model Validator ready.")
