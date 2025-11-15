"""
Refinement Prompts
LLM prompts for modification parsing
"""

MODIFICATION_PARSING_PROMPT = """
Parse this modification request into structured changes:

FEEDBACK: {feedback}

CURRENT MODEL:
{model_summary}

Extract:
1. What to modify
2. Which elements
3. What property
4. New value

Return as JSON array of modifications.
Return ONLY valid JSON.
"""

### TODO: USER MUST FILL THIS SECTION
# Add modification prompts
