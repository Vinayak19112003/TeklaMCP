"""
Modification Parser
Parses natural language modification requests
"""

import json
from typing import List, Dict
from anthropic import Anthropic

from ..utils import get_logger, Config

logger = get_logger(__name__)


class ModificationParser:
    """
    Parse natural language modification requests
    """

    def __init__(self):
        self.logger = logger
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def parse(self, feedback: str, current_schema: Dict) -> List[Dict]:
        """
        Parse modification request

        Args:
            feedback: Natural language modification
            current_schema: Current building schema

        Returns:
            List of modification dictionaries
        """
        self.logger.info("Parsing modification", feedback=feedback)

        prompt = f"""
Parse this modification request into structured changes:

FEEDBACK: {feedback}

CURRENT MODEL SUMMARY:
- Elements: {current_schema.get('element_count', 'unknown')}
- Grid: {current_schema.get('grid_summary', 'unknown')}

Extract:
1. What to modify (columns, beams, grid, connections, etc.)
2. Which elements (all, specific locations, range, perimeter, interior)
3. What property to change (profile, material, spacing, etc.)
4. New value

Return as JSON array:
[
  {{
    "target": "columns",
    "filter": "all" | "perimeter" | "interior" | {{"grid_locations": [...]}},
    "property": "profile",
    "new_value": "UC356x406x287"
  }}
]

Return ONLY valid JSON array.
"""

        response = self.client.messages.create(
            model=Config.DEFAULT_LLM_MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text

        # Extract JSON
        if "```json" in text:
            json_text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            json_text = text.split("```")[1].split("```")[0]
        else:
            json_text = text

        modifications = json.loads(json_text.strip())

        return modifications


if __name__ == "__main__":
    print("Modification Parser ready.")
