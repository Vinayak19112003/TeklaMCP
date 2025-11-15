"""
Text Processor
Processes natural language building descriptions using LLM
"""

import os
import json
from typing import Dict
from anthropic import Anthropic
from openai import OpenAI

from ..utils import get_logger, Config

logger = get_logger(__name__)


class TextProcessor:
    """
    Process natural language text descriptions
    Extract structured building data using LLM
    """

    def __init__(self, provider: str = "anthropic"):
        """
        Initialize text processor

        Args:
            provider: "anthropic" or "openai"
        """
        self.logger = logger
        self.provider = provider

        if provider == "anthropic":
            self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
            self.model = Config.DEFAULT_LLM_MODEL
        elif provider == "openai":
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.model = "gpt-4-turbo-preview"
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def process(self, text: str) -> Dict:
        """
        Process text description and extract structural data

        Args:
            text: Natural language building description

        Returns:
            Dictionary with extracted structural data
        """
        self.logger.info("Processing text description", length=len(text))

        try:
            prompt = self._build_extraction_prompt(text)

            if self.provider == "anthropic":
                result = self._process_with_claude(prompt)
            else:
                result = self._process_with_openai(prompt)

            self.logger.info("Text processing complete", keys=list(result.keys()))

            return result

        except Exception as e:
            self.logger.error("Text processing failed", error=str(e))
            raise

    def _build_extraction_prompt(self, text: str) -> str:
        """Build extraction prompt"""
        return f"""
You are a structural engineering AI analyzing building descriptions.

Extract the following information from this description:

TEXT: {text}

Return a JSON object with this structure:
{{
  "building_type": "industrial_building | warehouse | office | portal_frame | etc.",
  "dimensions": {{
    "length": <millimeters>,
    "width": <millimeters>,
    "height": <millimeters>
  }},
  "grid": {{
    "x_spacing": <millimeters or array of spacings>,
    "y_spacing": <millimeters or array of spacings>,
    "x_count": <number of bays>,
    "y_count": <number of bays>
  }},
  "columns": {{
    "profile": "<section designation>",
    "material": "<material grade>",
    "base_connection": "<connection type>",
    "bolts": "<bolt specification like 4xM24>"
  }},
  "beams": {{
    "profile": "<section designation>",
    "material": "<material grade>",
    "type": "simple | continuous | rigid"
  }},
  "bracing": {{
    "present": true/false,
    "type": "X | K | V | diagonal",
    "location": "description"
  }},
  "loads": {{
    "dead": <kN/m²>,
    "live": <kN/m²>,
    "wind": <kN/m²>,
    "snow": <kN/m²>
  }},
  "materials": {{
    "steel_grade": "<grade>",
    "concrete_class": "<class if applicable>"
  }},
  "design_code": "EC3 | AISC360 | BS5950 | AS4100",
  "confidence": <0.0-1.0>
}}

Important:
- All dimensions in millimeters
- Extract exact values mentioned
- Use null for missing data
- Infer reasonable defaults if appropriate (note in confidence)
- Return ONLY valid JSON, no other text
"""

    def _process_with_claude(self, prompt: str) -> Dict:
        """Process using Claude API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract JSON from response
        text = response.content[0].text

        # Try to parse JSON
        try:
            # Look for JSON in response
            if "```json" in text:
                json_text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                json_text = text.split("```")[1].split("```")[0]
            else:
                json_text = text

            result = json.loads(json_text.strip())
            return result

        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse JSON response", error=str(e), text=text[:500])
            raise

    def _process_with_openai(self, prompt: str) -> Dict:
        """Process using OpenAI API"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a structural engineering assistant. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=Config.TEMPERATURE,
            response_format={"type": "json_object"}
        )

        text = response.choices[0].message.content
        return json.loads(text)

    ### TODO: USER MUST FILL THIS SECTION
    # Add custom text processing logic:
    # - Pre-processing steps (cleaning, normalization)
    # - Post-processing validation
    # - Custom extraction rules
    # - Multi-language support


if __name__ == "__main__":
    processor = TextProcessor()

    description = """
    Create an industrial warehouse:
    - 40 meters long x 30 meters wide
    - 10 meter eave height
    - 8 meter column spacing in both directions
    - UC305x305x198 columns, S355 steel
    - UB457x191x74 roof beams
    - Simple base plates with 4xM24 bolts
    """

    result = processor.process(description)
    print(json.dumps(result, indent=2))
