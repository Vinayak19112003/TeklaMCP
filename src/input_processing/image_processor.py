"""
Image Processor
Processes images and hand sketches using Vision AI
"""

import base64
from pathlib import Path
from typing import Dict
from anthropic import Anthropic
import cv2
import numpy as np

from ..utils import get_logger, Config, validate_file_size

logger = get_logger(__name__)


class ImageProcessor:
    """
    Process structural drawing images
    Handle photos, scans, hand sketches
    """

    def __init__(self):
        self.logger = logger
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def process(self, image_path: str) -> Dict:
        """
        Process image

        Args:
            image_path: Path to image file

        Returns:
            Extracted structural data
        """
        self.logger.info("Processing image", path=image_path)

        try:
            # Validate file
            validate_file_size(image_path, Config.MAX_FILE_SIZE_MB)

            # Preprocess image
            processed_img = self._preprocess_image(image_path)

            # Convert to base64
            img_b64 = self._image_to_base64(processed_img)

            # Analyze with Vision AI
            result = self._analyze_with_vision(img_b64)

            self.logger.info("Image processing complete")

            return result

        except Exception as e:
            self.logger.error("Image processing failed", error=str(e))
            raise

    def _preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for better extraction

        Args:
            image_path: Path to image

        Returns:
            Processed image as numpy array
        """
        # Read image
        img = cv2.imread(str(image_path))

        if img is None:
            raise ValueError(f"Failed to read image: {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray)

        # Enhance contrast
        enhanced = cv2.equalizeHist(denoised)

        # Convert back to BGR for encoding
        result = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

        return result

    def _image_to_base64(self, img: np.ndarray) -> str:
        """Convert numpy image to base64"""
        # Encode as PNG
        success, buffer = cv2.imencode('.png', img)

        if not success:
            raise ValueError("Failed to encode image")

        # Convert to base64
        img_b64 = base64.b64encode(buffer).decode()

        return img_b64

    def _analyze_with_vision(self, img_b64: str) -> Dict:
        """
        Analyze image with Claude Vision

        Args:
            img_b64: Base64 encoded image

        Returns:
            Extracted data dictionary
        """
        prompt = """
Analyze this structural drawing or sketch.

Extract all visible information:

1. Grid system (if visible):
   - Grid line labels
   - Spacing dimensions

2. Structural elements:
   - Columns, beams, bracing
   - Locations and sizes
   - Any annotations

3. Dimensions:
   - Overall building size
   - Member lengths
   - Spacing

4. Materials and specifications:
   - Steel sections
   - Materials noted
   - Connection types

5. Any text annotations or notes

Return as JSON:
{{
  "drawing_type": "plan | elevation | section | sketch",
  "grid": {{
    "x_lines": [...],
    "y_lines": [...],
    "spacings": {{...}}
  }},
  "dimensions": {{
    "length": <mm>,
    "width": <mm>,
    "height": <mm>
  }},
  "elements": [
    {{"type": "column", "profile": "...", "location": "..."}},
    ...
  ],
  "notes": ["..."],
  "quality": "good | fair | poor",
  "confidence": 0.0-1.0
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

        # Parse JSON response
        import json
        text = response.content[0].text

        if "```json" in text:
            json_text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            json_text = text.split("```")[1].split("```")[0]
        else:
            json_text = text

        result = json.loads(json_text.strip())

        return result

    ### TODO: USER MUST FILL THIS SECTION
    # Add custom image processing:
    # - Perspective correction for phone photos
    # - Line detection for grid extraction
    # - Symbol recognition
    # - Handwriting recognition (OCR)
    # - Image quality assessment


if __name__ == "__main__":
    processor = ImageProcessor()

    # Test with an image
    # result = processor.process("test_sketch.jpg")
    # print(json.dumps(result, indent=2))

    print("Image Processor ready. Provide an image path to process.")
