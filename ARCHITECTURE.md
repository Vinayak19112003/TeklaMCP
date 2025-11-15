# System Architecture - AI Tekla Model Generator

## 🏗️ Architectural Overview

This document describes the detailed architecture of the AI-powered Tekla Structures model generator.

---

## 1. Core Architecture Principles

### 1.1 Design Philosophy
- **Modularity**: Each component is independent and replaceable
- **Extensibility**: Easy to add new input types, extractors, or generators
- **Reliability**: Robust error handling and validation at each stage
- **Scalability**: Can handle from simple buildings to complex structures
- **Maintainability**: Clear separation of concerns, well-documented code

### 1.2 Architectural Patterns
- **Pipeline Architecture**: Data flows through distinct processing stages
- **Strategy Pattern**: Different extraction strategies for different input types
- **Template Method**: Code generation uses templates with customization
- **Factory Pattern**: Dynamic creation of extractors and generators
- **Observer Pattern**: Feedback and monitoring throughout pipeline

---

## 2. Component Architecture

### 2.1 Input Processing Layer

```
┌─────────────────────────────────────────────────────────┐
│              INPUT CLASSIFIER                           │
│  Determines input type and routes to processor         │
└────────┬────────────────────────────────────────────────┘
         │
         ├─► Text Input ──────► TextProcessor
         ├─► PDF Input ───────► PDFProcessor
         ├─► Image Input ─────► ImageProcessor
         ├─► Multi-modal ─────► MultiModalProcessor
         └─► Feedback ────────► FeedbackProcessor
```

#### Text Processor
**Purpose**: Process natural language descriptions

**Components**:
```python
class TextProcessor:
    def __init__(self):
        self.llm = ClaudeClient()  # or GPT-4
        self.validator = InputValidator()

    def process(self, text: str) -> Dict:
        """
        1. Validate input text
        2. Extract entities (dimensions, materials, loads)
        3. Structure into preliminary JSON
        4. Return structured data
        """
        validated = self.validator.validate(text)
        entities = self.llm.extract_entities(text)
        structured = self.structure_data(entities)
        return structured
```

**Key Features**:
- Entity recognition (NER) for structural elements
- Unit conversion and validation
- Ambiguity detection and clarification
- Context preservation across conversations

#### PDF Processor
**Purpose**: Extract information from structural drawings

**Architecture**:
```python
class PDFProcessor:
    def __init__(self):
        self.pdf_parser = PyMuPDFParser()
        self.vision_ai = ClaudeVision()
        self.ocr = TesseractOCR()
        self.table_extractor = TableExtractor()

    def process(self, pdf_path: str) -> Dict:
        """
        Multi-stage processing:
        1. PDF parsing (text + images)
        2. Page classification (plan/elevation/section/detail)
        3. Vision AI analysis for each page
        4. OCR for text extraction
        5. Table extraction for specs
        6. Combine all extracted data
        """
        pages = self.pdf_parser.extract_pages(pdf_path)
        results = []

        for page in pages:
            page_type = self.classify_page(page)

            if page_type == "drawing":
                data = self.vision_ai.analyze_drawing(page.image)
            elif page_type == "table":
                data = self.table_extractor.extract(page)
            else:
                data = self.ocr.extract_text(page)

            results.append(data)

        return self.merge_page_data(results)
```

**Technologies**:
- **PyMuPDF**: PDF parsing, image extraction
- **pdfplumber**: Table detection and extraction
- **Claude Vision/GPT-4V**: Drawing analysis
- **Tesseract**: OCR for text regions
- **OpenCV**: Image preprocessing

**Page Classification**:
```python
def classify_page(self, page) -> str:
    """
    Uses vision AI to determine page type:
    - general_arrangement: Overall plan view
    - foundation_plan: Foundation details
    - elevation: Building elevation
    - section: Cross-section view
    - connection_detail: Connection closeups
    - schedule: Member schedules, tables
    - specification: Text specifications
    """
    prompt = """
    Classify this structural drawing page as one of:
    general_arrangement, foundation_plan, elevation,
    section, connection_detail, schedule, specification
    """
    return self.vision_ai.classify(page.image, prompt)
```

#### Image Processor
**Purpose**: Process hand sketches, photos, screenshots

```python
class ImageProcessor:
    def __init__(self):
        self.vision_ai = ClaudeVision()
        self.preprocessor = ImagePreprocessor()

    def process(self, image_path: str) -> Dict:
        """
        1. Preprocess image (enhance, deskew, denoise)
        2. Vision AI analysis
        3. Extract grid, dimensions, annotations
        4. Return structured data
        """
        img = self.preprocessor.load_and_enhance(image_path)
        analysis = self.vision_ai.analyze_structural_drawing(img)
        return self.structure_extracted_data(analysis)
```

**Image Enhancement Pipeline**:
```python
class ImagePreprocessor:
    def load_and_enhance(self, path: str):
        img = cv2.imread(path)

        # 1. Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2. Deskew (correct rotation)
        deskewed = self.deskew(gray)

        # 3. Denoise
        denoised = cv2.fastNlMeansDenoising(deskewed)

        # 4. Enhance contrast
        enhanced = cv2.equalizeHist(denoised)

        # 5. Binarization (for OCR)
        binary = cv2.adaptiveThreshold(
            enhanced, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return binary
```

---

### 2.2 Information Extraction Layer

```
┌─────────────────────────────────────────────────────────┐
│          EXTRACTION ORCHESTRATOR                        │
│  Coordinates multiple extractors                       │
└────────┬────────────────────────────────────────────────┘
         │
         ├─► GridExtractor ────► Grid system data
         ├─► ElementExtractor ─► Beams, columns, bracing
         ├─► LoadExtractor ────► Loads and load cases
         ├─► MaterialExtractor ► Materials and grades
         ├─► ConnectionExtractor ► Connection details
         └─► SpecExtractor ────► Specifications, codes
```

#### Vision-Based Extraction

**Grid Extractor**:
```python
class GridExtractor:
    def extract_from_drawing(self, drawing_image, llm_analysis) -> GridData:
        """
        Extract grid information using combination of:
        1. Vision AI detection
        2. OCR for labels
        3. Geometric analysis
        """
        prompt = """
        Analyze this structural drawing and extract:

        1. All gridline labels (numbers and letters)
        2. Spacing between gridlines in millimeters
        3. Total building dimensions
        4. Grid orientation (true north if shown)

        Return as JSON:
        {
          "x_grid": {
            "labels": ["1", "2", "3", ...],
            "coordinates": [0, 6000, 12000, ...],
            "spacing_type": "uniform" | "variable"
          },
          "y_grid": {
            "labels": ["A", "B", "C", ...],
            "coordinates": [0, 8000, 16000, ...],
            "spacing_type": "uniform" | "variable"
          },
          "z_levels": {
            "labels": ["Ground", "First Floor", ...],
            "elevations": [0, 4000, 8000, ...]
          }
        }
        """

        result = self.llm.extract(drawing_image, prompt)
        validated = self.validate_grid(result)
        return GridData(**validated)
```

**Element Extractor**:
```python
class ElementExtractor:
    def extract_elements(self, drawing_image) -> List[StructuralElement]:
        """
        Extract all structural elements with:
        - Type (column, beam, brace, etc.)
        - Location (grid references)
        - Size/profile
        - Material
        - Orientation
        """
        prompt = """
        Identify all structural elements in this drawing.

        For each element, extract:
        1. Type: column, beam, rafter, purlin, bracing, etc.
        2. Location: grid references (e.g., "column at A-1")
        3. Profile/size: section designation (e.g., "HEA300", "IPE400")
        4. Material: steel grade or concrete class
        5. Length or height
        6. Any special notes

        Return as JSON array:
        [
          {
            "type": "column",
            "location": {"grid_x": "A", "grid_y": "1"},
            "profile": "HEA300",
            "material": "S355",
            "height": 8000,
            "notes": "Base plate with 4xM24 bolts"
          },
          ...
        ]
        """

        elements = self.llm.extract(drawing_image, prompt)
        return [StructuralElement(**e) for e in elements]
```

**Load Extractor**:
```python
class LoadExtractor:
    def extract_loads(self, spec_text: str) -> List[Load]:
        """
        Extract load cases from specifications
        """
        prompt = """
        Extract all load information:

        1. Dead loads (DL)
        2. Live loads (LL)
        3. Wind loads (WL)
        4. Snow loads (SL)
        5. Seismic loads (EQ)
        6. Load combinations

        Include:
        - Magnitude and units
        - Application location
        - Load case number
        - Design code reference

        Return as JSON.
        """

        loads = self.llm.extract(spec_text, prompt)
        return [Load(**l) for l in loads]
```

#### Validation & Inference

```python
class ExtractionValidator:
    """
    Validates extracted data and infers missing information
    """

    def validate_and_infer(self, extracted_data: Dict) -> Dict:
        """
        1. Check for completeness
        2. Validate engineering constraints
        3. Infer missing data
        4. Flag uncertainties
        """
        validated = self.validate_constraints(extracted_data)
        inferred = self.infer_missing_data(validated)
        flagged = self.flag_uncertainties(inferred)
        return flagged

    def validate_constraints(self, data: Dict) -> Dict:
        """
        Engineering validation:
        - Beam spans within reasonable limits
        - Column heights make sense
        - Material grades are valid
        - Profile sizes exist in standards
        """
        # Example: validate beam span
        for beam in data.get('beams', []):
            span = beam['length']
            if span > 25000:  # 25m
                beam['warnings'] = beam.get('warnings', [])
                beam['warnings'].append(
                    "Long span detected - verify design"
                )

        return data

    def infer_missing_data(self, data: Dict) -> Dict:
        """
        Intelligent inference:
        - If no material specified, use common default (S275/S355)
        - If base connections not shown, infer standard base plate
        - If loads not specified, use typical values with warning
        """
        if 'materials' not in data:
            data['materials'] = {
                'default_steel': 'S275',
                'inferred': True,
                'warning': 'Material not specified - using default'
            }

        return data
```

---

### 2.3 Schema Generation Layer

```python
class SchemaGenerator:
    """
    Converts extracted data into validated JSON schema
    """

    def __init__(self):
        self.schema_validator = SchemaValidator()
        self.template_engine = Jinja2TemplateEngine()

    def generate_schema(self, extracted_data: Dict) -> BuildingSchema:
        """
        Create comprehensive building schema
        """
        schema = {
            "metadata": self.generate_metadata(extracted_data),
            "grid": self.generate_grid_schema(extracted_data['grid']),
            "elements": self.generate_elements_schema(extracted_data['elements']),
            "loads": self.generate_loads_schema(extracted_data['loads']),
            "connections": self.generate_connections_schema(extracted_data),
            "materials": self.generate_materials_schema(extracted_data['materials'])
        }

        # Validate against JSON schema
        validated = self.schema_validator.validate(schema)

        return BuildingSchema(**validated)
```

**JSON Schema Structure**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "grid", "elements"],
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "project_name": {"type": "string"},
        "project_number": {"type": "string"},
        "design_code": {"type": "string", "enum": ["EC3", "AISC360", "BS5950"]},
        "units": {"type": "string", "default": "mm"},
        "created_date": {"type": "string", "format": "date-time"},
        "ai_confidence": {"type": "number", "minimum": 0, "maximum": 1}
      }
    },
    "grid": {
      "type": "object",
      "required": ["x_lines", "y_lines"],
      "properties": {
        "x_lines": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "label": {"type": "string"},
              "coordinate": {"type": "number"}
            }
          }
        },
        "y_lines": {"type": "array"},
        "z_levels": {"type": "array"}
      }
    },
    "elements": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "profile", "material"],
        "properties": {
          "id": {"type": "string"},
          "type": {"type": "string", "enum": ["column", "beam", "brace", "rafter"]},
          "profile": {"type": "string"},
          "material": {"type": "string"},
          "start_point": {"$ref": "#/definitions/point3d"},
          "end_point": {"$ref": "#/definitions/point3d"},
          "rotation": {"type": "number"},
          "class": {"type": "string"}
        }
      }
    }
  },
  "definitions": {
    "point3d": {
      "type": "object",
      "properties": {
        "x": {"type": "number"},
        "y": {"type": "number"},
        "z": {"type": "number"}
      },
      "required": ["x", "y", "z"]
    }
  }
}
```

---

### 2.4 Code Generation Layer

#### Generator Architecture

```python
class TeklaCodeGenerator:
    """
    Generates Tekla OpenAPI C# code from building schema
    """

    def __init__(self):
        self.llm = ClaudeClient(model="claude-3-5-sonnet-20250929")
        self.template_engine = Jinja2TemplateEngine()
        self.rag_system = TeklaRAGSystem()  # For API documentation
        self.validator = CSharpValidator()

    def generate_code(self, schema: BuildingSchema) -> str:
        """
        Multi-stage code generation:
        1. RAG lookup for relevant Tekla API patterns
        2. Template selection
        3. LLM-based code generation
        4. Validation and compilation check
        """

        # Get relevant API documentation
        api_docs = self.rag_system.get_relevant_docs(schema)

        # Select appropriate templates
        templates = self.select_templates(schema)

        # Generate code using LLM
        code = self.llm_generate(schema, api_docs, templates)

        # Validate
        validated = self.validator.validate(code)

        return validated

    def llm_generate(self, schema, api_docs, templates) -> str:
        """
        LLM-based code generation with few-shot examples
        """
        prompt = f"""
        You are an expert Tekla Structures OpenAPI developer.

        Generate complete C# code to create this building model:

        BUILDING SCHEMA:
        {json.dumps(schema.dict(), indent=2)}

        RELEVANT API DOCUMENTATION:
        {api_docs}

        EXAMPLE TEMPLATES:
        {templates}

        REQUIREMENTS:
        1. Use Tekla.Structures.Model namespace
        2. Create complete, compilable C# code
        3. Structure:
           - Namespace and imports
           - Main class with CreateModel() method
           - Helper methods for each component type
           - Error handling
        4. Order of operations:
           a) Connect to model
           b) Create grid system
           c) Create columns (with base plates)
           d) Create beams/rafters
           e) Create bracing
           f) Create connections
           g) Commit changes
        5. Use proper Tekla conventions:
           - All coordinates in millimeters
           - Position enums for alignment
           - Material and profile strings
        6. Add comments explaining each major section
        7. Include error handling and logging
        8. Make code readable and maintainable

        Generate the complete C# code now.
        """

        return self.llm.generate(prompt, max_tokens=8000)
```

#### RAG System for Tekla API

```python
class TeklaRAGSystem:
    """
    Retrieval-Augmented Generation for Tekla API documentation
    """

    def __init__(self):
        self.vector_db = ChromaDB()
        self.embedder = OpenAIEmbeddings()

        # Index Tekla documentation
        self.index_documentation()

    def index_documentation(self):
        """
        Index Tekla OpenAPI documentation into vector DB
        """
        docs = [
            "Creating grids in Tekla...",
            "Beam creation with Tekla.Structures.Model.Beam...",
            "Connection components usage...",
            "Position and rotation enums...",
            # ... all Tekla API docs
        ]

        for doc in docs:
            embedding = self.embedder.embed(doc)
            self.vector_db.add(doc, embedding)

    def get_relevant_docs(self, schema: BuildingSchema, top_k=5) -> str:
        """
        Retrieve relevant API documentation based on schema
        """
        # Create query from schema
        query = f"""
        How to create:
        - Grid with {len(schema.grid.x_lines)} x {len(schema.grid.y_lines)} lines
        - {len([e for e in schema.elements if e.type == 'column'])} columns
        - {len([e for e in schema.elements if e.type == 'beam'])} beams
        - Base plate connections
        """

        # Retrieve relevant docs
        docs = self.vector_db.similarity_search(query, k=top_k)

        return "\n\n".join(docs)
```

#### Template System

```python
# Example: Column template (Jinja2)
COLUMN_TEMPLATE = """
private void CreateColumn(double x, double y, double height,
                         string profile, string material)
{
    Beam column = new Beam();
    column.StartPoint = new Point(x, y, 0);
    column.EndPoint = new Point(x, y, height);
    column.Profile.ProfileString = "{{ profile }}";
    column.Material.MaterialString = "{{ material }}";
    column.Class = "{{ class }}";
    column.Position.Depth = Position.DepthEnum.MIDDLE;
    column.Position.Plane = Position.PlaneEnum.MIDDLE;
    column.Position.Rotation = Position.RotationEnum.FRONT;

    if (!column.Insert())
    {
        Console.WriteLine($"Failed to create column at ({x}, {y})");
        return;
    }

    // Create base plate
    CreateBasePlate(column);
}
"""

# Grid template
GRID_TEMPLATE = """
private void CreateGrid()
{
    Grid grid = new Grid();
    grid.Name = "{{ grid_name }}";

    // X-axis gridlines
    GridPlane gridPlaneX = new GridPlane();
    gridPlaneX.Label = "X";

    {% for line in x_lines %}
    {
        GridLine gridLine = new GridLine();
        gridLine.Point = new Point({{ line.coordinate }}, 0, 0);
        gridLine.Direction = new Vector(0, 1, 0);
        gridLine.Label = "{{ line.label }}";
        gridPlaneX.GridLines.Add(gridLine);
    }
    {% endfor %}

    // Y-axis gridlines
    GridPlane gridPlaneY = new GridPlane();
    gridPlaneY.Label = "Y";

    {% for line in y_lines %}
    {
        GridLine gridLine = new GridLine();
        gridLine.Point = new Point(0, {{ line.coordinate }}, 0);
        gridLine.Direction = new Vector(1, 0, 0);
        gridLine.Label = "{{ line.label }}";
        gridPlaneY.GridLines.Add(gridLine);
    }
    {% endfor %}

    grid.GridPlanes.Add(gridPlaneX);
    grid.GridPlanes.Add(gridPlaneY);
    grid.Insert();
}
"""
```

#### Code Validation

```python
class CSharpValidator:
    """
    Validates generated C# code
    """

    def validate(self, code: str) -> str:
        """
        1. Syntax check using Roslyn
        2. Compile check
        3. Static analysis
        4. Return validated code or raise errors
        """

        # Save to temp file
        temp_file = self.save_temp(code)

        # Try to compile
        result = subprocess.run(
            ["dotnet", "build", temp_file],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # Compilation failed
            errors = self.parse_errors(result.stderr)
            raise CodeGenerationError(f"Compilation failed: {errors}")

        return code

    def parse_errors(self, stderr: str) -> str:
        """
        Parse compiler errors and return human-readable format
        """
        # Extract error messages
        errors = re.findall(r"error CS\d+: (.+)", stderr)
        return "\n".join(errors)
```

---

### 2.5 Execution Layer

```python
class TeklaExecutor:
    """
    Executes generated C# code in Tekla Structures
    """

    def __init__(self):
        self.compiler = CSharpCompiler()
        self.tekla_connector = TeklaConnector()

    def execute(self, code: str) -> ExecutionResult:
        """
        1. Compile C# code
        2. Check Tekla connection
        3. Execute in Tekla
        4. Validate model
        5. Return result
        """

        # Compile
        assembly = self.compiler.compile(code)

        # Check Tekla is running
        if not self.tekla_connector.is_connected():
            raise TeklaNotRunningError("Tekla Structures is not running")

        # Execute
        try:
            result = self.tekla_connector.execute(assembly)

            # Validate model was created
            validation = self.validate_model()

            return ExecutionResult(
                success=True,
                validation=validation,
                message="Model created successfully"
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e),
                message="Execution failed"
            )

    def validate_model(self) -> ModelValidation:
        """
        Validate created model:
        - All elements created
        - Correct profiles and materials
        - No overlapping elements
        - Connections applied
        """
        # Query Tekla model
        model_stats = self.tekla_connector.get_model_stats()

        return ModelValidation(
            element_count=model_stats['total_parts'],
            column_count=model_stats['columns'],
            beam_count=model_stats['beams'],
            connection_count=model_stats['connections'],
            errors=model_stats.get('errors', [])
        )
```

---

### 2.6 Feedback Loop

```python
class FeedbackProcessor:
    """
    Handles user modifications and iterative refinement
    """

    def __init__(self):
        self.llm = ClaudeClient()
        self.schema_updater = SchemaUpdater()
        self.code_generator = TeklaCodeGenerator()

    def process_feedback(self,
                        current_schema: BuildingSchema,
                        feedback: str) -> BuildingSchema:
        """
        Process user feedback and update schema

        Examples:
        - "Change all columns to UC305x305x198"
        - "Add X-bracing between gridlines 2-3"
        - "Increase bay spacing to 10m"
        """

        # Parse feedback using LLM
        modifications = self.parse_modifications(feedback)

        # Apply to schema
        updated_schema = self.schema_updater.apply(
            current_schema,
            modifications
        )

        return updated_schema

    def parse_modifications(self, feedback: str) -> List[Modification]:
        """
        Extract structured modifications from natural language
        """
        prompt = f"""
        Parse this modification request into structured changes:

        FEEDBACK: {feedback}

        Extract:
        1. What to modify (columns, beams, grid, etc.)
        2. Which elements (all, specific locations, range)
        3. What property to change (profile, material, spacing, etc.)
        4. New value

        Return as JSON:
        [
          {{
            "target": "columns",
            "filter": "all",
            "property": "profile",
            "new_value": "UC305x305x198"
          }}
        ]
        """

        result = self.llm.extract(prompt)
        return [Modification(**m) for m in result]
```

---

## 3. Data Models

### 3.1 Core Data Structures

```python
from pydantic import BaseModel, validator
from typing import List, Optional, Literal
from enum import Enum

class Point3D(BaseModel):
    x: float
    y: float
    z: float = 0.0

class GridLine(BaseModel):
    label: str
    coordinate: float

class GridSystem(BaseModel):
    x_lines: List[GridLine]
    y_lines: List[GridLine]
    z_levels: List[GridLine] = []

    @validator('x_lines', 'y_lines')
    def validate_sorted(cls, v):
        coords = [line.coordinate for line in v]
        if coords != sorted(coords):
            raise ValueError("Grid lines must be sorted by coordinate")
        return v

class ElementType(str, Enum):
    COLUMN = "column"
    BEAM = "beam"
    RAFTER = "rafter"
    PURLIN = "purlin"
    BRACE = "brace"
    FOUNDATION = "foundation"

class StructuralElement(BaseModel):
    id: str
    type: ElementType
    profile: str
    material: str
    start_point: Point3D
    end_point: Point3D
    rotation: float = 0.0
    class_: str = "1"
    notes: Optional[str] = None

class Connection(BaseModel):
    type: Literal["base_plate", "moment", "simple", "splice"]
    primary_element: str  # element ID
    secondary_elements: List[str] = []
    bolts: Optional[str] = None
    weld: Optional[str] = None
    parameters: dict = {}

class LoadCase(BaseModel):
    name: str
    type: Literal["dead", "live", "wind", "snow", "seismic"]
    magnitude: float
    unit: str
    application: str

class BuildingSchema(BaseModel):
    metadata: dict
    grid: GridSystem
    elements: List[StructuralElement]
    connections: List[Connection] = []
    loads: List[LoadCase] = []
    materials: dict = {}
```

---

## 4. Technology Stack Details

### 4.1 AI/ML Stack

```yaml
Primary LLMs:
  - Claude 3.5 Sonnet: Vision + Code Generation
  - GPT-4 Turbo: Backup for complex reasoning

Vision Models:
  - Claude Vision API: Drawing analysis
  - GPT-4 Vision: Alternative vision processing

OCR:
  - Tesseract: Open-source OCR
  - Azure Computer Vision: Cloud OCR
  - Google Cloud Vision: High-accuracy OCR

Embeddings:
  - OpenAI text-embedding-3-large: For RAG
  - Voyage AI: Alternative embeddings
```

### 4.2 Document Processing

```yaml
PDF Processing:
  - PyMuPDF (fitz): Fast PDF parsing
  - pdfplumber: Table extraction
  - pdf2image: PDF to image conversion

Image Processing:
  - Pillow: Basic image operations
  - OpenCV: Advanced processing
  - scikit-image: Scientific image processing

Document Understanding:
  - Docling: Document layout analysis
  - Unstructured.io: Multi-format parsing
```

### 4.3 Vector Database & RAG

```yaml
Vector Databases:
  - ChromaDB: Local development
  - Pinecone: Production scalability
  - Weaviate: Alternative vector DB

RAG Framework:
  - LangChain: Orchestration
  - LlamaIndex: Data connectors
```

### 4.4 Code Generation & Execution

```yaml
.NET Stack:
  - .NET 6/7/8 SDK
  - Roslyn: C# compilation and analysis
  - Tekla OpenAPI: Model creation

Validation:
  - Roslyn Analyzers: Static analysis
  - FxCop: Code quality
```

---

## 5. Deployment Architecture

### 5.1 Development Setup
```
Developer Machine
├── Python 3.10+ (Processing pipeline)
├── .NET SDK (Code compilation)
├── Tekla Structures (Model execution)
└── Vector DB (Local ChromaDB)
```

### 5.2 Production Setup (Optional Web Service)

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND                             │
│  React/Next.js Web App                                 │
│  - File upload                                         │
│  - Text input                                          │
│  - 3D preview (Three.js)                               │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼────────────────────────────────────┐
│                API GATEWAY                              │
│  FastAPI/Flask                                         │
│  - Authentication                                      │
│  - Rate limiting                                       │
│  - Request routing                                     │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼────────┐   ┌─────────▼────────┐
│ Processing      │   │  Code Generation │
│ Workers         │   │  Workers         │
│ (Celery)        │   │  (Celery)        │
└────────┬────────┘   └─────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              SHARED SERVICES                            │
│  - Redis (caching, queue)                              │
│  - PostgreSQL (metadata, history)                      │
│  - S3/MinIO (file storage)                             │
│  - Pinecone (vector search)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Performance Optimization

### 6.1 Caching Strategy

```python
class CachingLayer:
    """
    Multi-level caching for performance
    """

    def __init__(self):
        self.redis = Redis()
        self.memory_cache = {}

    def get_cached_extraction(self, file_hash: str):
        """
        Cache extracted data to avoid re-processing
        """
        # Check memory cache
        if file_hash in self.memory_cache:
            return self.memory_cache[file_hash]

        # Check Redis
        cached = self.redis.get(f"extraction:{file_hash}")
        if cached:
            return json.loads(cached)

        return None

    def cache_extraction(self, file_hash: str, data: dict, ttl=3600):
        """
        Store extraction result
        """
        # Memory cache
        self.memory_cache[file_hash] = data

        # Redis cache
        self.redis.setex(
            f"extraction:{file_hash}",
            ttl,
            json.dumps(data)
        )
```

### 6.2 Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelProcessor:
    """
    Process multiple pages/documents in parallel
    """

    def process_multi_page_pdf(self, pdf_path: str):
        """
        Process PDF pages in parallel
        """
        pages = self.extract_pages(pdf_path)

        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.process_page, page): page
                for page in pages
            }

            for future in as_completed(futures):
                page = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Page {page.number} failed: {e}")

        return self.merge_results(results)
```

---

## 7. Error Handling & Resilience

```python
class RobustPipeline:
    """
    Pipeline with comprehensive error handling
    """

    def process_with_fallback(self, input_data):
        """
        Try multiple strategies with fallbacks
        """
        strategies = [
            self.primary_strategy,
            self.secondary_strategy,
            self.fallback_strategy
        ]

        errors = []

        for strategy in strategies:
            try:
                result = strategy(input_data)
                if self.validate_result(result):
                    return result
            except Exception as e:
                errors.append(f"{strategy.__name__}: {e}")
                continue

        # All strategies failed
        raise ProcessingError(
            f"All strategies failed: {'; '.join(errors)}"
        )

    def validate_result(self, result) -> bool:
        """
        Check if result meets quality threshold
        """
        # Check completeness
        if not result.get('grid') or not result.get('elements'):
            return False

        # Check confidence
        if result.get('confidence', 0) < 0.7:
            return False

        return True
```

---

## 8. Monitoring & Logging

```python
import structlog
from opentelemetry import trace

logger = structlog.get_logger()
tracer = trace.get_tracer(__name__)

class MonitoredPipeline:
    """
    Pipeline with comprehensive monitoring
    """

    def process(self, input_data):
        with tracer.start_as_current_span("pipeline.process") as span:
            span.set_attribute("input_type", input_data.type)

            try:
                # Log start
                logger.info("pipeline.started",
                           input_type=input_data.type,
                           size=input_data.size)

                # Process
                result = self._do_process(input_data)

                # Log success
                logger.info("pipeline.completed",
                           duration=span.duration,
                           elements_created=len(result.elements))

                span.set_attribute("success", True)
                return result

            except Exception as e:
                # Log error
                logger.error("pipeline.failed",
                            error=str(e),
                            traceback=traceback.format_exc())

                span.set_attribute("success", False)
                span.record_exception(e)
                raise
```

---

## 9. Security Considerations

### 9.1 Input Validation

```python
class SecurityValidator:
    """
    Validate and sanitize inputs
    """

    def validate_pdf(self, file_path: str):
        """
        Check PDF file for:
        - Max file size (50MB)
        - Valid PDF format
        - No embedded executables
        - No scripts
        """
        # Size check
        size = os.path.getsize(file_path)
        if size > 50 * 1024 * 1024:
            raise ValidationError("PDF exceeds 50MB limit")

        # Format validation
        if not self.is_valid_pdf(file_path):
            raise ValidationError("Invalid PDF format")

        # Security scan
        if self.has_embedded_executables(file_path):
            raise SecurityError("PDF contains embedded executables")

    def sanitize_code(self, generated_code: str) -> str:
        """
        Sanitize generated code:
        - Remove dangerous system calls
        - Limit file I/O
        - No network access
        """
        dangerous_patterns = [
            r'System\.IO\.File\.Delete',
            r'Process\.Start',
            r'Registry\.',
            r'HttpClient',
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, generated_code):
                raise SecurityError(
                    f"Generated code contains dangerous pattern: {pattern}"
                )

        return generated_code
```

---

## 10. Testing Strategy

### 10.1 Unit Tests

```python
import pytest

class TestGridExtractor:
    def test_extract_uniform_grid(self):
        """Test extraction of uniform grid"""
        drawing = load_test_image("uniform_grid_6x4.png")
        extractor = GridExtractor()

        result = extractor.extract(drawing)

        assert len(result.x_lines) == 6
        assert len(result.y_lines) == 4
        assert result.x_lines[0].coordinate == 0
        assert result.x_lines[1].coordinate == 6000
```

### 10.2 Integration Tests

```python
class TestEndToEnd:
    def test_text_to_model(self):
        """Test complete pipeline from text to model"""
        generator = TeklaGenerator()

        result = generator.from_text("""
            30m x 20m building, 8m height,
            HEA300 columns, IPE400 beams, S355 steel
        """)

        assert result.schema.grid is not None
        assert len(result.schema.elements) > 0
        assert result.code is not None
        assert "HEA300" in result.code
```

---

This architecture provides a robust, scalable, and maintainable foundation for the AI Tekla model generator system.
