# Implementation Guide

Step-by-step guide to implementing the AI Tekla Model Generator.

---

## Phase 1: Setup & Prerequisites

### 1.1 Install Dependencies

```bash
# Clone repository
git clone https://github.com/yourrepo/TeklaMCP.git
cd TeklaMCP

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Install .NET SDK (for Tekla code compilation)
# Download from: https://dotnet.microsoft.com/download
# Verify installation:
dotnet --version
```

### 1.2 Configure API Keys

Create `.env` file:

```bash
# AI APIs
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Cloud OCR (if using)
AZURE_VISION_KEY=your_azure_key
AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/

# Vector Database (if using cloud)
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_environment

# Application Settings
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=50
CACHE_ENABLED=true
AUTO_EXECUTE=false
```

### 1.3 Install Tekla Structures

- Install Tekla Structures (2021 or later recommended)
- Ensure Tekla OpenAPI is accessible
- Test connection: Open Tekla → File → New Model

---

## Phase 2: Core Implementation

### 2.1 Project Structure Setup

```bash
mkdir -p src/{input_processing,extraction,schema,code_generation,execution,feedback,utils}
mkdir -p prompts schemas examples tests
```

### 2.2 Implement Input Processing

**File: `src/input_processing/text_processor.py`**

```python
from anthropic import Anthropic
from typing import Dict
import os

class TextProcessor:
    """
    Process natural language building descriptions
    """

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def process(self, text: str) -> Dict:
        """
        Extract structured building information from text
        """
        prompt = self._build_extraction_prompt(text)

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20250929",
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Parse JSON response
        import json
        result = json.loads(response.content[0].text)

        return result

    def _build_extraction_prompt(self, text: str) -> str:
        return f"""
You are a structural engineering AI analyzing building descriptions.

Extract the following information from this description:

TEXT: {text}

Return a JSON object with this structure:
{{
  "building_type": "industrial_building | warehouse | office | etc.",
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
    "bolts": "<bolt specification>"
  }},
  "beams": {{
    "profile": "<section designation>",
    "material": "<material grade>",
    "type": "simple | continuous | rigid"
  }},
  "bracing": {{
    "present": true/false,
    "type": "X | K | V",
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
  "design_code": "EC3 | AISC360 | BS5950 | AS4100"
}}

Important:
- All dimensions in millimeters
- Extract exact values mentioned
- Use "unknown" for missing data
- Infer reasonable defaults if appropriate (note this in output)
"""


# Example usage
if __name__ == "__main__":
    processor = TextProcessor()

    description = """
    Create a 40m x 30m industrial warehouse with:
    - 10m column spacing
    - 12m eave height
    - HEB400 columns
    - IPE500 roof beams
    - S355 steel grade
    - Simple base plates
    """

    result = processor.process(description)
    print(json.dumps(result, indent=2))
```

**File: `src/input_processing/pdf_processor.py`**

```python
import fitz  # PyMuPDF
from anthropic import Anthropic
import os
from PIL import Image
import io
import base64

class PDFProcessor:
    """
    Process structural PDF drawings
    """

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def process(self, pdf_path: str) -> Dict:
        """
        Extract information from PDF drawings
        """
        # Open PDF
        doc = fitz.open(pdf_path)

        all_results = []

        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Convert page to image
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")

            # Analyze with Vision AI
            result = self._analyze_page(img_bytes, page_num)

            all_results.append(result)

        # Merge results from all pages
        merged = self._merge_page_results(all_results)

        return merged

    def _analyze_page(self, image_bytes: bytes, page_num: int) -> Dict:
        """
        Analyze single page with Claude Vision
        """
        # Encode image to base64
        img_b64 = base64.b64encode(image_bytes).decode()

        prompt = """
Analyze this structural drawing page.

Classify the page type:
- general_arrangement: Overall plan view
- elevation: Building elevation view
- section: Cross-section view
- foundation_plan: Foundation layout
- connection_detail: Connection details
- schedule: Member schedule/table
- specification: Text specifications

Then extract all relevant information:
1. For plan/elevation/section:
   - Grid lines and labels
   - Dimensions
   - Member sizes and locations
   - Materials
   - Notes

2. For schedules:
   - Extract table data
   - Member marks, sizes, quantities

3. For details:
   - Connection type
   - Components
   - Bolt/weld specifications

Return as structured JSON.
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

        import json
        result = json.loads(response.content[0].text)
        result["page_number"] = page_num

        return result

    def _merge_page_results(self, results: List[Dict]) -> Dict:
        """
        Combine data from multiple pages
        """
        # Find plan view (main page)
        plan_view = next(
            (r for r in results if r.get("page_type") == "general_arrangement"),
            results[0]
        )

        # Enhance with schedule data
        schedules = [r for r in results if r.get("page_type") == "schedule"]
        for schedule in schedules:
            if "column_schedule" in schedule:
                plan_view["column_details"] = schedule["column_schedule"]
            if "beam_schedule" in schedule:
                plan_view["beam_details"] = schedule["beam_schedule"]

        # Add connection details
        details = [r for r in results if r.get("page_type") == "connection_detail"]
        plan_view["connections"] = details

        return plan_view


# Example usage
if __name__ == "__main__":
    processor = PDFProcessor()
    result = processor.process("structural_plan.pdf")

    import json
    print(json.dumps(result, indent=2))
```

### 2.3 Implement Schema Generator

**File: `src/schema/models.py`**

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from enum import Enum

class Point3D(BaseModel):
    x: float
    y: float
    z: float = 0.0

class GridLine(BaseModel):
    label: str
    coordinate: float  # millimeters

class GridSystem(BaseModel):
    x_lines: List[GridLine]
    y_lines: List[GridLine]
    z_levels: List[GridLine] = Field(default_factory=list)

    @validator('x_lines', 'y_lines')
    def validate_sorted(cls, v):
        coords = [line.coordinate for line in v]
        if coords != sorted(coords):
            raise ValueError("Grid lines must be sorted")
        return v

class ElementType(str, Enum):
    COLUMN = "column"
    BEAM = "beam"
    RAFTER = "rafter"
    BRACE = "brace"

class StructuralElement(BaseModel):
    id: str
    type: ElementType
    profile: str
    material: str
    start_point: Point3D
    end_point: Point3D
    rotation: float = 0.0
    class_: str = Field(default="1", alias="class")

class Connection(BaseModel):
    type: Literal["base_plate", "moment", "simple", "splice"]
    primary_element: str
    secondary_elements: List[str] = Field(default_factory=list)
    bolts: Optional[str] = None
    parameters: dict = Field(default_factory=dict)

class BuildingSchema(BaseModel):
    metadata: dict
    grid: GridSystem
    elements: List[StructuralElement]
    connections: List[Connection] = Field(default_factory=list)
    materials: dict = Field(default_factory=dict)
```

**File: `src/schema/schema_generator.py`**

```python
from .models import *
from typing import Dict, List

class SchemaGenerator:
    """
    Generate validated building schema from extracted data
    """

    def generate(self, extracted_data: Dict) -> BuildingSchema:
        """
        Create BuildingSchema from extracted data
        """
        # Generate grid
        grid = self._generate_grid(extracted_data)

        # Generate elements
        elements = self._generate_elements(extracted_data, grid)

        # Generate connections
        connections = self._generate_connections(extracted_data, elements)

        # Build schema
        schema = BuildingSchema(
            metadata=self._generate_metadata(extracted_data),
            grid=grid,
            elements=elements,
            connections=connections,
            materials=extracted_data.get("materials", {})
        )

        return schema

    def _generate_grid(self, data: Dict) -> GridSystem:
        """
        Generate grid system from extracted data
        """
        grid_data = data.get("grid", {})

        # Generate X-axis gridlines
        x_lines = []
        x_spacing = grid_data.get("x_spacing")
        x_count = grid_data.get("x_count", 1)

        if isinstance(x_spacing, list):
            # Variable spacing
            coord = 0
            for i, spacing in enumerate(x_spacing):
                x_lines.append(GridLine(label=str(i + 1), coordinate=coord))
                coord += spacing
            x_lines.append(GridLine(label=str(len(x_spacing) + 1), coordinate=coord))
        else:
            # Uniform spacing
            for i in range(x_count + 1):
                x_lines.append(
                    GridLine(label=str(i + 1), coordinate=i * x_spacing)
                )

        # Generate Y-axis gridlines
        y_lines = []
        y_spacing = grid_data.get("y_spacing")
        y_count = grid_data.get("y_count", 1)

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if isinstance(y_spacing, list):
            coord = 0
            for i, spacing in enumerate(y_spacing):
                y_lines.append(GridLine(label=letters[i], coordinate=coord))
                coord += spacing
            y_lines.append(GridLine(label=letters[len(y_spacing)], coordinate=coord))
        else:
            for i in range(y_count + 1):
                y_lines.append(
                    GridLine(label=letters[i], coordinate=i * y_spacing)
                )

        # Z-levels
        z_levels = [
            GridLine(label="Ground", elevation=0),
            GridLine(label="Roof", elevation=data["dimensions"]["height"])
        ]

        return GridSystem(x_lines=x_lines, y_lines=y_lines, z_levels=z_levels)

    def _generate_elements(self, data: Dict, grid: GridSystem) -> List[StructuralElement]:
        """
        Generate all structural elements
        """
        elements = []

        # Create columns at all grid intersections
        column_data = data.get("columns", {})
        column_height = data["dimensions"]["height"]

        element_id = 1
        for x_line in grid.x_lines:
            for y_line in grid.y_lines:
                col = StructuralElement(
                    id=f"COL-{element_id}",
                    type=ElementType.COLUMN,
                    profile=column_data.get("profile", "UC305x305x198"),
                    material=column_data.get("material", "S355"),
                    start_point=Point3D(x=x_line.coordinate, y=y_line.coordinate, z=0),
                    end_point=Point3D(x=x_line.coordinate, y=y_line.coordinate, z=column_height)
                )
                elements.append(col)
                element_id += 1

        # Create beams between columns (roof level)
        beam_data = data.get("beams", {})
        roof_level = column_height

        # X-direction beams
        for y_line in grid.y_lines:
            for i in range(len(grid.x_lines) - 1):
                beam = StructuralElement(
                    id=f"BEAM-X-{element_id}",
                    type=ElementType.BEAM,
                    profile=beam_data.get("profile", "IPE400"),
                    material=beam_data.get("material", "S355"),
                    start_point=Point3D(
                        x=grid.x_lines[i].coordinate,
                        y=y_line.coordinate,
                        z=roof_level
                    ),
                    end_point=Point3D(
                        x=grid.x_lines[i + 1].coordinate,
                        y=y_line.coordinate,
                        z=roof_level
                    )
                )
                elements.append(beam)
                element_id += 1

        # Y-direction beams
        for x_line in grid.x_lines:
            for i in range(len(grid.y_lines) - 1):
                beam = StructuralElement(
                    id=f"BEAM-Y-{element_id}",
                    type=ElementType.BEAM,
                    profile=beam_data.get("profile", "IPE400"),
                    material=beam_data.get("material", "S355"),
                    start_point=Point3D(
                        x=x_line.coordinate,
                        y=grid.y_lines[i].coordinate,
                        z=roof_level
                    ),
                    end_point=Point3D(
                        x=x_line.coordinate,
                        y=grid.y_lines[i + 1].coordinate,
                        z=roof_level
                    )
                )
                elements.append(beam)
                element_id += 1

        return elements

    def _generate_connections(self, data: Dict, elements: List[StructuralElement]) -> List[Connection]:
        """
        Generate connection specifications
        """
        connections = []

        column_data = data.get("columns", {})
        bolts = column_data.get("bolts", "4xM24")

        # Base plate for each column
        for elem in elements:
            if elem.type == ElementType.COLUMN:
                conn = Connection(
                    type="base_plate",
                    primary_element=elem.id,
                    bolts=bolts,
                    parameters={
                        "plate_thickness": 25,
                        "bolt_grade": "8.8"
                    }
                )
                connections.append(conn)

        return connections

    def _generate_metadata(self, data: Dict) -> dict:
        from datetime import datetime

        return {
            "name": data.get("building_type", "Generated Building"),
            "design_code": data.get("design_code", "EC3"),
            "units": "mm",
            "created": datetime.now().isoformat(),
            "ai_generated": True
        }
```

### 2.4 Implement Code Generator

**File: `src/code_generation/tekla_generator.py`**

```python
from anthropic import Anthropic
from ..schema.models import BuildingSchema
import os
import json

class TeklaCodeGenerator:
    """
    Generate Tekla OpenAPI C# code from building schema
    """

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate(self, schema: BuildingSchema) -> str:
        """
        Generate complete Tekla C# code
        """
        prompt = self._build_generation_prompt(schema)

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20250929",
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        code = response.content[0].text

        # Extract code from markdown if present
        if "```csharp" in code:
            code = code.split("```csharp")[1].split("```")[0]

        return code.strip()

    def _build_generation_prompt(self, schema: BuildingSchema) -> str:
        schema_json = schema.model_dump_json(indent=2)

        return f"""
You are an expert Tekla Structures OpenAPI developer.

Generate complete, production-ready C# code to create this building model:

BUILDING SCHEMA:
{schema_json}

REQUIREMENTS:

1. Structure:
   - Use namespace matching the project
   - Import required Tekla namespaces
   - Main class with CreateModel() method
   - Helper methods for each component type
   - Main() entry point

2. Implementation order:
   a) Connect to Tekla model
   b) Create grid system
   c) Create all columns with base plates
   d) Create all beams
   e) Commit changes

3. Tekla API conventions:
   - Use Tekla.Structures.Model namespace
   - All coordinates in millimeters
   - Grid: Use Grid, GridPlane, GridLine classes
   - Elements: Use Beam class for columns and beams
   - Connections: Use Connection class
   - Position enums: Position.DepthEnum, Position.PlaneEnum, Position.RotationEnum

4. Code quality:
   - Add error handling (try-catch, null checks)
   - Add Console.WriteLine for progress tracking
   - Add comments explaining major sections
   - Use descriptive variable names
   - Format code properly

5. Example patterns:

Creating a column:
```csharp
Beam column = new Beam();
column.StartPoint = new Point(x, y, 0);
column.EndPoint = new Point(x, y, height);
column.Profile.ProfileString = "UC305*305*198";  // Note: * not x
column.Material.MaterialString = "S355";
column.Class = "1";
column.Position.Depth = Position.DepthEnum.MIDDLE;
column.Position.Plane = Position.PlaneEnum.MIDDLE;
column.Insert();
```

Creating grid:
```csharp
Grid grid = new Grid();
GridPlane gridPlaneX = new GridPlane();
GridLine line = new GridLine();
line.Point = new Point(x, 0, 0);
line.Direction = new Vector(0, 1, 0);
line.Label = "1";
gridPlaneX.GridLines.Add(line);
grid.GridPlanes.Add(gridPlaneX);
grid.Insert();
```

Now generate the complete C# code. Return ONLY the code, no explanations.
"""


# Example usage
if __name__ == "__main__":
    # Assume we have a schema
    from ..schema.models import *

    # Simple example schema
    grid = GridSystem(
        x_lines=[GridLine(label=str(i), coordinate=i*8000) for i in range(5)],
        y_lines=[GridLine(label=c, coordinate=i*6000) for i, c in enumerate("ABCD")]
    )

    elements = [
        StructuralElement(
            id="COL-1",
            type=ElementType.COLUMN,
            profile="UC305x305x198",
            material="S355",
            start_point=Point3D(x=0, y=0, z=0),
            end_point=Point3D(x=0, y=0, z=8000)
        )
    ]

    schema = BuildingSchema(
        metadata={"name": "Test Building"},
        grid=grid,
        elements=elements
    )

    generator = TeklaCodeGenerator()
    code = generator.generate(schema)

    print(code)

    # Save to file
    with open("generated_model.cs", "w") as f:
        f.write(code)
```

### 2.5 Main Application

**File: `src/main.py`**

```python
from input_processing.text_processor import TextProcessor
from input_processing.pdf_processor import PDFProcessor
from schema.schema_generator import SchemaGenerator
from code_generation.tekla_generator import TeklaCodeGenerator
import json
import os

class TeklaAIGenerator:
    """
    Main application class
    """

    def __init__(self):
        self.text_processor = TextProcessor()
        self.pdf_processor = PDFProcessor()
        self.schema_gen = SchemaGenerator()
        self.code_gen = TeklaCodeGenerator()

    def from_text(self, description: str):
        """
        Generate from text description
        """
        print("Processing text description...")
        extracted = self.text_processor.process(description)

        print("Generating schema...")
        schema = self.schema_gen.generate(extracted)

        print("Generating Tekla code...")
        code = self.code_gen.generate(schema)

        return GenerationResult(
            extracted=extracted,
            schema=schema,
            code=code
        )

    def from_pdf(self, pdf_path: str):
        """
        Generate from PDF drawing
        """
        print(f"Processing PDF: {pdf_path}...")
        extracted = self.pdf_processor.process(pdf_path)

        print("Generating schema...")
        schema = self.schema_gen.generate(extracted)

        print("Generating Tekla code...")
        code = self.code_gen.generate(schema)

        return GenerationResult(
            extracted=extracted,
            schema=schema,
            code=code
        )


class GenerationResult:
    def __init__(self, extracted, schema, code):
        self.extracted = extracted
        self.schema = schema
        self.code = code

    def save(self, output_dir="output"):
        """
        Save all outputs to files
        """
        os.makedirs(output_dir, exist_ok=True)

        # Save extracted data
        with open(f"{output_dir}/extracted.json", "w") as f:
            json.dump(self.extracted, f, indent=2)

        # Save schema
        with open(f"{output_dir}/schema.json", "w") as f:
            f.write(self.schema.model_dump_json(indent=2))

        # Save code
        with open(f"{output_dir}/TeklaModel.cs", "w") as f:
            f.write(self.code)

        print(f"\nFiles saved to {output_dir}/")
        print(f"  - extracted.json")
        print(f"  - schema.json")
        print(f"  - TeklaModel.cs")

    def get_code(self):
        return self.code

    def get_schema(self):
        return self.schema


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Tekla Model Generator")
    parser.add_argument("--text", help="Text description of building")
    parser.add_argument("--pdf", help="Path to PDF drawing")
    parser.add_argument("--output", default="output", help="Output directory")

    args = parser.parse_args()

    generator = TeklaAIGenerator()

    if args.text:
        result = generator.from_text(args.text)
    elif args.pdf:
        result = generator.from_pdf(args.pdf)
    else:
        print("Error: Provide --text or --pdf")
        exit(1)

    result.save(args.output)

    print("\nGeneration complete!")
    print(f"\nTo compile and run:")
    print(f"  cd {args.output}")
    print(f"  dotnet build TeklaModel.cs")
    print(f"  dotnet run")
```

---

## Phase 3: Testing

### 3.1 Create Test Cases

**File: `tests/test_text_processor.py`**

```python
import pytest
from src.input_processing.text_processor import TextProcessor

def test_simple_building():
    processor = TextProcessor()

    description = """
    30m x 20m building, 8m high,
    HEA300 columns, IPE400 beams, S355 steel
    """

    result = processor.process(description)

    assert result["dimensions"]["length"] == 30000
    assert result["dimensions"]["width"] == 20000
    assert result["dimensions"]["height"] == 8000
    assert result["columns"]["profile"] == "HEA300"
    assert result["beams"]["profile"] == "IPE400"

def test_complex_building():
    processor = TextProcessor()

    description = """
    Industrial warehouse:
    - 60m long x 40m wide
    - 12m eave height
    - 10m bay spacing
    - UC305x305x198 columns
    - UB610x229x125 roof beams
    - S355 steel
    - Perimeter bracing
    - Design to Eurocode 3
    """

    result = processor.process(description)

    assert result["building_type"] == "industrial_warehouse"
    assert result["grid"]["x_spacing"] == 10000
    assert result["bracing"]["present"] == True
    assert result["design_code"] == "EC3"
```

### 3.2 Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_text_processor.py
```

---

## Phase 4: Deployment

### 4.1 Local Usage

```bash
# From text
python src/main.py --text "40m x 30m warehouse, 10m spacing, HEB400 columns, S355"

# From PDF
python src/main.py --pdf drawings/plan.pdf --output output/my_building
```

### 4.2 As Python Module

```python
from src.main import TeklaAIGenerator

generator = TeklaAIGenerator()

result = generator.from_text("""
    Create a 50m x 25m portal frame building:
    - 6m bay spacing
    - 8m eave, 10m ridge
    - UB533x210x101 columns
    - UB457x191x74 rafters
    - S355 steel
""")

# Get generated code
code = result.get_code()

# Save outputs
result.save("output/portal_frame")

# Execute in Tekla (requires Tekla running)
# result.execute_in_tekla()  # Future implementation
```

### 4.3 Web API (Optional)

**File: `api/server.py`**

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from src.main import TeklaAIGenerator
import shutil

app = FastAPI(title="Tekla AI Generator API")
generator = TeklaAIGenerator()

@app.post("/generate/text")
async def generate_from_text(description: str):
    """
    Generate from text description
    """
    try:
        result = generator.from_text(description)

        return {
            "success": True,
            "schema": result.schema.model_dump(),
            "code": result.code
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/generate/pdf")
async def generate_from_pdf(file: UploadFile = File(...)):
    """
    Generate from PDF upload
    """
    try:
        # Save uploaded file
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process
        result = generator.from_pdf(temp_path)

        return {
            "success": True,
            "schema": result.schema.model_dump(),
            "code": result.code
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

# Run: uvicorn api.server:app --reload
```

---

## Phase 5: Advanced Features

### 5.1 Caching Implementation

```python
import hashlib
import json
from functools import wraps

class CacheManager:
    def __init__(self):
        self.cache = {}

    def cache_extraction(self, func):
        @wraps(func)
        def wrapper(self, input_data):
            # Generate cache key
            cache_key = hashlib.md5(
                str(input_data).encode()
            ).hexdigest()

            # Check cache
            if cache_key in self.cache:
                print("Cache hit!")
                return self.cache[cache_key]

            # Execute function
            result = func(self, input_data)

            # Store in cache
            self.cache[cache_key] = result

            return result

        return wrapper
```

### 5.2 Feedback Loop

```python
from anthropic import Anthropic

class FeedbackProcessor:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def apply_modifications(self, schema: BuildingSchema, feedback: str):
        """
        Apply user modifications to existing schema
        """
        prompt = f"""
You are modifying an existing building model.

CURRENT SCHEMA:
{schema.model_dump_json(indent=2)}

USER MODIFICATION:
{feedback}

Return the COMPLETE updated schema as JSON, incorporating the requested changes.
Only modify what was requested, keep everything else the same.
"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20250929",
            max_tokens=6000,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        updated = json.loads(response.content[0].text)

        return BuildingSchema(**updated)
```

---

## Next Steps

1. **Implement RAG system** for Tekla API documentation
2. **Add connection library** with pre-built connection types
3. **Implement load calculation** integration
4. **Add 3D preview** using Three.js
5. **Create web interface** for easier usage
6. **Add model validation** after execution
7. **Implement cost estimation** based on generated model

---

## Troubleshooting

### Common Issues

**Issue: API key errors**
```
Solution: Check .env file has correct API keys
```

**Issue: Tekla connection failed**
```
Solution: Ensure Tekla Structures is running and has an open model
```

**Issue: Code compilation errors**
```
Solution: Check .NET SDK is installed and Tekla OpenAPI references are correct
```

**Issue: Low extraction quality**
```
Solution: Improve prompts, use higher quality input images, or try different AI model
```

---

This implementation guide provides a complete pathway from setup to deployment!
