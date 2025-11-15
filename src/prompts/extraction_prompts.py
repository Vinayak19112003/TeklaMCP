"""
Extraction Prompts
LLM prompts for data extraction
"""

TEXT_EXTRACTION_PROMPT = """
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
- Return ONLY valid JSON
"""

PDF_EXTRACTION_PROMPT = """
Analyze this structural drawing page.

Classify the page type:
- general_arrangement: Overall plan view
- elevation: Building elevation
- section: Cross-section
- foundation_plan: Foundation layout
- connection_detail: Connection details
- schedule: Member schedule/table
- specification: Text specifications

Then extract all relevant information.

Return as JSON with all extracted data.
Return ONLY valid JSON.
"""

### TODO: USER MUST FILL THIS SECTION
# Add custom prompts for:
# - Specific drawing types
# - Different design codes
# - Special extraction needs
