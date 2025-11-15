"""
Document Classifier
Classifies input documents to route to appropriate processor
"""

from pathlib import Path
from typing import Literal
import mimetypes

from ..utils import get_logger

logger = get_logger(__name__)

DocumentType = Literal["text", "pdf", "image", "unknown"]


class DocumentClassifier:
    """
    Classify input documents by type
    """

    def __init__(self):
        self.logger = logger

        # Supported file extensions
        self.pdf_extensions = {".pdf"}
        self.image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
        self.text_extensions = {".txt", ".md"}

    def classify(self, input_data: str) -> DocumentType:
        """
        Classify input data

        Args:
            input_data: File path or text string

        Returns:
            Document type
        """
        # Check if it's a file path
        path = Path(input_data)

        if path.exists() and path.is_file():
            return self._classify_file(path)
        else:
            # Assume it's text if not a file
            return "text"

    def _classify_file(self, file_path: Path) -> DocumentType:
        """
        Classify file by extension and MIME type

        Args:
            file_path: Path to file

        Returns:
            Document type
        """
        extension = file_path.suffix.lower()

        # Check by extension first
        if extension in self.pdf_extensions:
            return "pdf"
        elif extension in self.image_extensions:
            return "image"
        elif extension in self.text_extensions:
            return "text"

        # Check by MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))

        if mime_type:
            if mime_type.startswith("image/"):
                return "image"
            elif mime_type == "application/pdf":
                return "pdf"
            elif mime_type.startswith("text/"):
                return "text"

        self.logger.warning("Unknown file type", path=str(file_path), extension=extension)

        return "unknown"

    def can_process(self, input_data: str) -> bool:
        """
        Check if input can be processed

        Args:
            input_data: File path or text

        Returns:
            True if processable
        """
        doc_type = self.classify(input_data)
        return doc_type != "unknown"

    ### TODO: USER MUST FILL THIS SECTION
    # Add custom classification logic:
    # - Support for CAD files (DWG, DXF)
    # - Support for IFC files
    # - Support for Excel/CSV schedules
    # - Content-based classification (not just extension)


if __name__ == "__main__":
    classifier = DocumentClassifier()

    # Test classification
    test_cases = [
        "This is a text description",
        "drawing.pdf",
        "sketch.jpg",
        "plan.png",
        "notes.txt"
    ]

    for test in test_cases:
        doc_type = classifier.classify(test)
        print(f"{test:30} → {doc_type}")
