"""
NLP Extractor
Extract entities from text using NLP
"""

from typing import Dict, List
from ..utils import get_logger

logger = get_logger(__name__)


class NLPExtractor:
    """
    Extract named entities from text
    """

    def __init__(self):
        self.logger = logger

    def extract_dimensions(self, text: str) -> Dict:
        """Extract dimensions from text"""

        ### TODO: USER MUST FILL THIS SECTION
        # Use regex or NLP to extract:
        # - "40m" → 40000mm
        # - "30 meters" → 30000mm
        # - Fractions and decimals

        return {}

    def extract_sections(self, text: str) -> List[str]:
        """Extract steel section designations"""

        ### TODO: USER MUST FILL THIS SECTION
        # Extract patterns like:
        # - HEA300, IPE400
        # - UC305x305x198
        # - UB457x191x74

        return []


if __name__ == "__main__":
    print("NLP Extractor ready.")
