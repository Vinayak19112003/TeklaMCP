"""
OCR Extractor
Extract text from images using OCR
"""

import pytesseract
from PIL import Image
from typing import List, Dict
from ..utils import get_logger

logger = get_logger(__name__)


class OCRExtractor:
    """
    Extract text using Tesseract OCR
    """

    def __init__(self):
        self.logger = logger

    def extract_text(self, image_path: str) -> str:
        """
        Extract all text from image

        Args:
            image_path: Path to image

        Returns:
            Extracted text
        """
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            self.logger.error("OCR failed", error=str(e))
            return ""

    def extract_data(self, image_path: str) -> Dict:
        """
        Extract structured data using OCR

        Args:
            image_path: Path to image

        Returns:
            Dictionary with extracted data
        """
        text = self.extract_text(image_path)

        ### TODO: USER MUST FILL THIS SECTION
        # Parse extracted text to find:
        # - Dimensions
        # - Section sizes
        # - Materials
        # - Grid labels

        return {"text": text}


if __name__ == "__main__":
    print("OCR Extractor ready.")
