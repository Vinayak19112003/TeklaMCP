"""
PDF Processor
Processes PDF structural drawings using Vision AI
"""

import fitz  # PyMuPDF
import base64
from pathlib import Path
from typing import Dict, List
from anthropic import Anthropic

from ..utils import get_logger, Config, validate_file_size

logger = get_logger(__name__)


class PDFProcessor:
    """
    Process PDF structural drawings
    Extract information using Vision AI
    """

    def __init__(self):
        self.logger = logger
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def process(self, pdf_path: str) -> Dict:
        """
        Process PDF drawing

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with extracted data
        """
        self.logger.info("Processing PDF", path=pdf_path)

        try:
            # Validate file size
            validate_file_size(pdf_path, Config.MAX_FILE_SIZE_MB)

            # Open PDF
            doc = fitz.open(pdf_path)
            self.logger.info("PDF opened", pages=len(doc))

            all_results = []

            # Process each page
            for page_num in range(len(doc)):
                self.logger.info("Processing page", page=page_num + 1)

                page_result = self._process_page(doc, page_num)
                all_results.append(page_result)

            doc.close()

            # Merge results from all pages
            merged = self._merge_page_results(all_results)

            self.logger.info("PDF processing complete", pages=len(all_results))

            return merged

        except Exception as e:
            self.logger.error("PDF processing failed", error=str(e))
            raise

    def _process_page(self, doc, page_num: int) -> Dict:
        """Process single PDF page"""

        page = doc[page_num]

        # Convert page to image
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")

        # Analyze with Vision AI
        result = self._analyze_with_vision(img_bytes, page_num)

        return result

    def _analyze_with_vision(self, image_bytes: bytes, page_num: int) -> Dict:
        """
        Analyze page using Claude Vision

        Args:
            image_bytes: PNG image bytes
            page_num: Page number

        Returns:
            Extracted data dictionary
        """
        # Encode image to base64
        img_b64 = base64.b64encode(image_bytes).decode()

        prompt = """
Analyze this structural drawing page.

First, classify the page type:
- general_arrangement: Overall plan view with grid
- elevation: Building elevation view
- section: Cross-section view
- foundation_plan: Foundation layout
- connection_detail: Connection details
- schedule: Member schedule/table
- specification: Text specifications

Then extract all relevant information:

1. For plan/elevation/section:
   - Grid lines and labels
   - Dimensions between grid lines
   - Member sizes and locations
   - Materials noted
   - Connection details
   - All annotations and notes

2. For schedules:
   - Extract table data
   - Member marks, sizes, quantities, materials

3. For details:
   - Connection type
   - Components (plates, bolts, welds)
   - Bolt/weld specifications
   - Dimensions

Return as JSON:
{{
  "page_type": "<type>",
  "grid": {{
    "x_lines": [{{"label": "1", "coordinate": 0}}, ...],
    "y_lines": [{{"label": "A", "coordinate": 0}}, ...],
    "spacings": [...]
  }},
  "elements": [
    {{"type": "column", "location": "A-1", "profile": "UC305x305x198", ...}},
    ...
  ],
  "dimensions": {{
    "length": <mm>,
    "width": <mm>,
    "height": <mm>
  }},
  "notes": ["note1", "note2"],
  "confidence": 0.85
}}

Return ONLY valid JSON.
"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20250929",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": img_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )

        # Parse response
        import json
        text = response.content[0].text

        # Extract JSON
        if "```json" in text:
            json_text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            json_text = text.split("```")[1].split("```")[0]
        else:
            json_text = text

        result = json.loads(json_text.strip())
        result["page_number"] = page_num

        return result

    def _merge_page_results(self, results: List[Dict]) -> Dict:
        """
        Merge results from multiple pages

        Args:
            results: List of page results

        Returns:
            Merged dictionary
        """
        # Find plan view (main page)
        plan_view = next(
            (r for r in results if r.get("page_type") == "general_arrangement"),
            results[0] if results else {}
        )

        # Enhance with schedule data
        schedules = [r for r in results if r.get("page_type") == "schedule"]
        for schedule in schedules:
            if "elements" in schedule:
                plan_view.setdefault("element_details", []).extend(schedule["elements"])

        # Add connection details
        details = [r for r in results if r.get("page_type") == "connection_detail"]
        plan_view.setdefault("connection_details", []).extend(details)

        # Collect all notes
        all_notes = []
        for result in results:
            all_notes.extend(result.get("notes", []))
        plan_view["notes"] = all_notes

        return plan_view

    ### TODO: USER MUST FILL THIS SECTION
    # Add custom PDF processing logic:
    # - OCR for text extraction
    # - Table detection and parsing
    # - Symbol recognition
    # - CAD layer parsing (if DWG converted to PDF)


if __name__ == "__main__":
    processor = PDFProcessor()

    # Test with a PDF file
    # result = processor.process("test_drawing.pdf")
    # print(json.dumps(result, indent=2))

    print("PDF Processor ready. Provide a PDF path to process.")
