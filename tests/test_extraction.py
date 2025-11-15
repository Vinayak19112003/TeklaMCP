"""
Tests for extraction modules
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from input_processing import TextProcessor


def test_text_processing():
    """Test text description processing"""

    description = "40m x 30m warehouse, 10m high, HEA300 columns"

    processor = TextProcessor()
    result = processor.process(description)

    assert "dimensions" in result
    assert result["dimensions"]["length"] == 40000
    assert result["dimensions"]["width"] == 30000


### TODO: USER MUST FILL THIS SECTION
# Add more tests:
# - PDF processing
# - Image processing
# - Schema generation
# - Code generation
# - Validation


if __name__ == "__main__":
    pytest.main([__file__])
