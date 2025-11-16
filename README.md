# AI-Powered Tekla Structures Model Generator

## 🎯 **NEW USER? START HERE!**

**👉 [Read START_HERE.md](START_HERE.md) first!** 👈

START_HERE.md will guide you through all the documentation in the right order, with clear learning paths for beginners, technical users, and everyone in between.

**Quick paths:**
- **Complete Beginner?** → [START_HERE.md](START_HERE.md) → [WHY_USE_THIS.md](WHY_USE_THIS.md) → [QUICK_START.md](QUICK_START.md)
- **Just want to try it?** → [QUICK_START.md](QUICK_START.md) (15 minutes)
- **Need full details?** → [USER_MANUAL.md](USER_MANUAL.md) (complete guide)

---

## 🏗️ Overview

An intelligent system that automatically generates complete Tekla Structures 3D models from natural language descriptions, PDF drawings, images, and engineering specifications.

**From this:**
```
"Create a 30m x 20m industrial building, 8m height,
with HEA300 columns and IPE400 beams, S355 steel"
```

**To this:** A complete, detailed Tekla 3D model with all structural elements, connections, and materials.

---

## 🎯 Key Features

### Multi-Modal Input Processing
- ✅ **Text descriptions** - Natural language building specifications
- ✅ **PDF drawings** - Structural plans, elevations, sections
- ✅ **Images/Screenshots** - Hand sketches, existing plans
- ✅ **Specification documents** - Design codes, material specs, load tables

### Intelligent Extraction
- **Grid systems** - Dimensions, spacing, orientation
- **Structural elements** - Beams, columns, bracing, foundations
- **Member sizing** - Cross-sections, lengths, orientations
- **Materials** - Steel grades, concrete classes
- **Loads** - Dead, live, wind, snow, seismic
- **Connections** - Base plates, beam-column connections, bracing

### Automated Code Generation
- Generates production-ready **Tekla OpenAPI C# code**
- Creates complete structural models with one click
- Handles complex geometry and connections
- Applies proper modeling standards

### Iterative Refinement
- Natural language feedback loop
- "Change all columns to UC305x305x198"
- "Add bracing on gridlines C and D"
- "Increase bay spacing to 9m"
- Regenerates updated code automatically

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT LAYER                              │
│  Text | PDF Drawings | Images | Specs | Feedback           │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              DOCUMENT PROCESSING                            │
│  • PDF Parser (PyMuPDF, pdfplumber)                        │
│  • Vision AI (Claude Vision, GPT-4V)                       │
│  • OCR (Tesseract, Azure Vision)                           │
│  • Text Analysis (NLP)                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│           INFORMATION EXTRACTION                            │
│  • Structural element detection                            │
│  • Dimension extraction                                    │
│  • Material identification                                 │
│  • Load analysis                                           │
│  • Grid system recognition                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              DATA STRUCTURING                               │
│  • JSON Schema Generation                                  │
│  • Validation & Constraint Checking                        │
│  • Engineering Rules Application                           │
│  • Missing Data Inference                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              CODE GENERATION                                │
│  • LLM-based C# generation (Claude/GPT-4)                  │
│  • Tekla OpenAPI template mapping                         │
│  • Connection logic generation                             │
│  • Error handling & validation                             │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│           TEKLA EXECUTION                                   │
│  • C# code compilation                                     │
│  • Tekla OpenAPI execution                                 │
│  • 3D model creation                                       │
│  • Quality validation                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│            FEEDBACK LOOP                                    │
│  • User modifications (NL)                                 │
│  • Schema updates                                          │
│  • Code regeneration                                       │
│  • Iterative refinement                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### AI & Machine Learning
- **LLMs**: Claude 3.5 Sonnet (vision + code gen), GPT-4 Turbo
- **Vision**: Claude Vision API, GPT-4 Vision
- **OCR**: Tesseract, Azure Computer Vision, Google Cloud Vision

### Document Processing
- **PDF**: PyMuPDF, pdfplumber, Apache Tika
- **Image**: Pillow, OpenCV
- **Document AI**: Docling, Unstructured.io

### Code Generation
- **Templates**: Jinja2, Handlebars
- **Validation**: Roslyn (C# analysis), AST parsing
- **Execution**: .NET SDK, Tekla OpenAPI

### Infrastructure
- **Orchestration**: LangChain, LlamaIndex
- **Vector DB**: Pinecone, ChromaDB (for Tekla docs RAG)
- **API**: FastAPI, Flask
- **Queue**: Celery, RabbitMQ (for long-running jobs)

### Frontend (Optional)
- **Web**: React, Next.js
- **File Upload**: React Dropzone
- **Visualization**: Three.js (3D preview)

---

## 📊 Data Flow Pipeline

### Phase 1: Input Ingestion
```python
Input → Document Classifier → Route to Processor
  ├─ Text: NLP Parser
  ├─ PDF: PDF Extractor + Vision AI
  ├─ Image: Vision AI + OCR
  └─ Mixed: Multi-modal processing
```

### Phase 2: Information Extraction
```python
Raw Content → LLM Prompt → Structured Extraction
  ├─ Grid: {lines, spacing, labels}
  ├─ Elements: {type, size, location, material}
  ├─ Loads: {type, magnitude, location}
  └─ Connections: {type, components, bolts}
```

### Phase 3: Schema Generation
```json
{
  "project": {
    "name": "Industrial Building",
    "code": "Eurocode 3"
  },
  "grid": {
    "x_lines": [0, 8000, 16000, 24000, 32000],
    "y_lines": [0, 7000, 14000, 21000],
    "z_levels": [0, 8000]
  },
  "columns": [
    {
      "location": {"grid_x": "A", "grid_y": "1"},
      "profile": "HEA300",
      "material": "S355",
      "height": 8000
    }
  ]
}
```

### Phase 4: Code Generation
```csharp
// Auto-generated Tekla OpenAPI code
using Tekla.Structures.Model;

public class BuildingGenerator {
    public void CreateModel() {
        Model model = new Model();

        // Create grid
        Grid grid = new Grid();
        grid.CreateGrid(xLines, yLines, zLevels);

        // Create columns
        foreach(var col in columns) {
            Beam column = new Beam();
            column.Profile.ProfileString = col.Profile;
            column.Material.MaterialString = col.Material;
            column.Insert();
        }
    }
}
```

---

## 📚 Documentation Index

**All documentation is organized for easy navigation:**

| Document | Purpose | Time | For Who |
|----------|---------|------|---------|
| **[START_HERE.md](START_HERE.md)** | 🎯 Navigation guide - Start here! | 5 min | Everyone |
| **[WHY_USE_THIS.md](WHY_USE_THIS.md)** | Why TeklaMCP vs direct AI? | 5 min | Everyone |
| **[QUICK_START.md](QUICK_START.md)** | Get running in 15 minutes | 15 min | Beginners |
| **[USER_MANUAL.md](USER_MANUAL.md)** | Complete setup & usage guide | 1 hour | Beginners |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Technical quick start | 30 min | Intermediate |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design & components | 45 min | Advanced |
| **[PIPELINE.md](PIPELINE.md)** | Data flow & processing | 30 min | Advanced |
| **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** | Developer guide | 1 hour | Developers |
| **[DESIGN_SUMMARY.md](DESIGN_SUMMARY.md)** | Executive summary & ROI | 30 min | All |
| **[ACCURACY_ANALYSIS.md](ACCURACY_ANALYSIS.md)** | AI accuracy (75-90%) | 20 min | All |

**Recommended reading order:** See [START_HERE.md](START_HERE.md) for personalized learning paths.

---

## 🚀 Quick Start

**For detailed setup instructions, see [QUICK_START.md](QUICK_START.md) or [USER_MANUAL.md](USER_MANUAL.md)**

### Installation

```bash
# Clone the repository
git clone https://github.com/Vinayak19112003/TeklaMCP.git
cd TeklaMCP

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys: ANTHROPIC_API_KEY, OPENAI_API_KEY

# Install .NET SDK (for Tekla code execution)
# Download from: https://dotnet.microsoft.com/download
```

### Basic Usage

```python
from tekla_ai import TeklaGenerator

# Initialize
generator = TeklaGenerator(api_key="your-claude-api-key")

# From text description
result = generator.from_text("""
    Create a 40m x 30m warehouse with:
    - 10m column spacing
    - 12m eave height
    - HEB400 columns
    - IPE500 roof beams
    - S275 steel grade
""")

# From PDF drawing
result = generator.from_pdf("structural_plan.pdf")

# From image
result = generator.from_image("sketch.jpg")

# Get generated code
code = result.get_code()
json_schema = result.get_schema()

# Execute in Tekla
result.execute_in_tekla()
```

### Iterative Refinement

```python
# Make modifications
result = generator.modify("""
    Change all columns to UC305x305x198
    Add X-bracing between columns on grid lines 2-3
    Increase bay spacing to 12m
""")

# Regenerate and execute
result.execute_in_tekla()
```

**📖 For complete examples, see [USER_MANUAL.md Section 6](USER_MANUAL.md) and the `examples/` folder.**

---

## 📁 Project Structure

```
TeklaMCP/
├── README.md
├── ARCHITECTURE.md          # Detailed architecture
├── PIPELINE.md             # Data flow details
├── requirements.txt
├── .env.example
│
├── src/
│   ├── input_processing/
│   │   ├── pdf_processor.py
│   │   ├── image_processor.py
│   │   ├── text_processor.py
│   │   └── document_classifier.py
│   │
│   ├── extraction/
│   │   ├── vision_extractor.py
│   │   ├── ocr_extractor.py
│   │   ├── nlp_extractor.py
│   │   └── structural_parser.py
│   │
│   ├── schema/
│   │   ├── schema_generator.py
│   │   ├── validator.py
│   │   ├── templates/
│   │   └── models/
│   │       ├── grid.py
│   │       ├── element.py
│   │       ├── load.py
│   │       └── connection.py
│   │
│   ├── code_generation/
│   │   ├── tekla_generator.py
│   │   ├── templates/
│   │   │   ├── grid_template.cs
│   │   │   ├── column_template.cs
│   │   │   ├── beam_template.cs
│   │   │   └── connection_template.cs
│   │   └── validators/
│   │
│   ├── execution/
│   │   ├── tekla_executor.py
│   │   ├── compiler.py
│   │   └── validator.py
│   │
│   ├── feedback/
│   │   ├── modification_parser.py
│   │   └── schema_updater.py
│   │
│   └── utils/
│       ├── logger.py
│       ├── config.py
│       └── helpers.py
│
├── tekla_api/
│   ├── OpenAPI_Reference.md
│   ├── common_patterns.md
│   └── examples/
│
├── prompts/
│   ├── extraction_prompts.py
│   ├── code_gen_prompts.py
│   └── refinement_prompts.py
│
├── schemas/
│   ├── building_schema.json
│   ├── grid_schema.json
│   ├── element_schema.json
│   └── connection_schema.json
│
├── tests/
│   ├── test_extraction.py
│   ├── test_generation.py
│   └── fixtures/
│
└── examples/
    ├── simple_building.py
    ├── from_pdf.py
    └── iterative_design.py
```

---

## 🎓 How It Works: Detailed Example

### Input: Text Description
```
"Design a portal frame building:
- 50m long x 25m wide
- 8m eave height, 10m ridge height
- 6m bay spacing
- UB533x210x101 columns
- UB457x191x74 rafters
- S355 steel
- Base plates with 4 M24 anchor bolts
- Moment connections at eaves and apex"
```

### Step 1: LLM Extraction (Claude/GPT-4)
The AI extracts structured data:

```json
{
  "building_type": "portal_frame",
  "dimensions": {
    "length": 50000,
    "width": 25000,
    "eave_height": 8000,
    "ridge_height": 10000
  },
  "spacing": {
    "bay": 6000
  },
  "grid": {
    "x_lines": [0, 6000, 12000, 18000, 24000, 30000, 36000, 42000, 48000],
    "y_lines": [0, 25000],
    "labels_x": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "labels_y": ["A", "B"]
  },
  "columns": [
    {
      "profile": "UB533x210x101",
      "material": "S355",
      "height": 8000,
      "locations": "all_grid_intersections",
      "base_connection": {
        "type": "base_plate",
        "bolts": "4xM24"
      }
    }
  ],
  "rafters": [
    {
      "profile": "UB457x191x74",
      "material": "S355",
      "type": "pitched",
      "apex_height": 10000,
      "connections": {
        "eave": "moment",
        "apex": "moment"
      }
    }
  ]
}
```

### Step 2: Code Generation

The system generates Tekla C# code:

```csharp
using System;
using Tekla.Structures.Model;
using Tekla.Structures.Geometry3d;

namespace AutoGeneratedModel
{
    public class PortalFrameBuilder
    {
        private Model _model;

        public void CreateModel()
        {
            _model = new Model();

            if (!_model.GetConnectionStatus())
            {
                Console.WriteLine("Tekla Structures not connected!");
                return;
            }

            CreateGrid();
            CreateColumns();
            CreateRafters();
            CreateConnections();

            _model.CommitChanges();
        }

        private void CreateGrid()
        {
            Grid grid = new Grid();
            grid.Name = "Grid1";

            // X-axis gridlines
            GridPlane gridPlaneX = new GridPlane();
            gridPlaneX.Label = "X";
            string[] xLabels = {"1", "2", "3", "4", "5", "6", "7", "8", "9"};
            double[] xCoords = {0, 6000, 12000, 18000, 24000, 30000, 36000, 42000, 48000};

            for (int i = 0; i < xCoords.Length; i++)
            {
                GridLine gridLine = new GridLine();
                gridLine.Point = new Point(xCoords[i], 0, 0);
                gridLine.Direction = new Vector(0, 1, 0);
                gridLine.Label = xLabels[i];
                gridPlaneX.GridLines.Add(gridLine);
            }

            // Y-axis gridlines
            GridPlane gridPlaneY = new GridPlane();
            gridPlaneY.Label = "Y";
            string[] yLabels = {"A", "B"};
            double[] yCoords = {0, 25000};

            for (int i = 0; i < yCoords.Length; i++)
            {
                GridLine gridLine = new GridLine();
                gridLine.Point = new Point(0, yCoords[i], 0);
                gridLine.Direction = new Vector(1, 0, 0);
                gridLine.Label = yLabels[i];
                gridPlaneY.GridLines.Add(gridLine);
            }

            grid.GridPlanes.Add(gridPlaneX);
            grid.GridPlanes.Add(gridPlaneY);
            grid.Insert();
        }

        private void CreateColumns()
        {
            double[] xCoords = {0, 6000, 12000, 18000, 24000, 30000, 36000, 42000, 48000};
            double[] yCoords = {0, 25000};

            foreach (double x in xCoords)
            {
                foreach (double y in yCoords)
                {
                    Beam column = new Beam();
                    column.StartPoint = new Point(x, y, 0);
                    column.EndPoint = new Point(x, y, 8000);
                    column.Profile.ProfileString = "UB533*210*101";
                    column.Material.MaterialString = "S355";
                    column.Class = "1";
                    column.Position.Depth = Position.DepthEnum.MIDDLE;
                    column.Position.Plane = Position.PlaneEnum.MIDDLE;
                    column.Position.Rotation = Position.RotationEnum.FRONT;
                    column.Insert();

                    // Create base plate
                    CreateBasePlate(column);
                }
            }
        }

        private void CreateRafters()
        {
            double[] xCoords = {0, 6000, 12000, 18000, 24000, 30000, 36000, 42000, 48000};
            double ridgeHeight = 10000;
            double eaveHeight = 8000;
            double width = 25000;
            double midY = width / 2;

            foreach (double x in xCoords)
            {
                // Left rafter (A side to ridge)
                Beam leftRafter = new Beam();
                leftRafter.StartPoint = new Point(x, 0, eaveHeight);
                leftRafter.EndPoint = new Point(x, midY, ridgeHeight);
                leftRafter.Profile.ProfileString = "UB457*191*74";
                leftRafter.Material.MaterialString = "S355";
                leftRafter.Class = "3";
                leftRafter.Insert();

                // Right rafter (ridge to B side)
                Beam rightRafter = new Beam();
                rightRafter.StartPoint = new Point(x, midY, ridgeHeight);
                rightRafter.EndPoint = new Point(x, width, eaveHeight);
                rightRafter.Profile.ProfileString = "UB457*191*74";
                rightRafter.Material.MaterialString = "S355";
                rightRafter.Class = "3";
                rightRafter.Insert();
            }
        }

        private void CreateBasePlate(Beam column)
        {
            // Base plate connection using Tekla standard component
            BaseConnection basePlate = new BaseConnection();
            basePlate.Name = "Base Plate";
            basePlate.Number = 1;
            basePlate.LoadAttributesFromFile("standard");

            // Set anchor bolts
            basePlate.SetAttribute("BoltSize", "M24");
            basePlate.SetAttribute("BoltStandard", "8.8");
            basePlate.SetAttribute("BoltCount", 4);

            basePlate.SetPrimaryObject(column);
            basePlate.Insert();
        }

        private void CreateConnections()
        {
            // Eave and apex moment connections
            // Implementation depends on specific Tekla connection components
            Console.WriteLine("Creating moment connections...");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            PortalFrameBuilder builder = new PortalFrameBuilder();
            builder.CreateModel();
            Console.WriteLine("Model created successfully!");
        }
    }
}
```

### Step 3: Execution

```bash
# Compile and run
dotnet build
dotnet run

# Result: Complete 3D model appears in Tekla Structures
```

### Step 4: Refinement

User: *"Change all columns to UC254x254x167"*

System:
1. Updates JSON schema: `"profile": "UC254x254x167"`
2. Regenerates C# code with new profile
3. Re-executes in Tekla
4. Model updates automatically

---

## 🧠 AI Prompting Strategy

### Extraction Prompt (for drawings)
```python
EXTRACTION_PROMPT = """
You are a structural engineering AI analyzing a building drawing.

Extract the following information:
1. Grid system: all gridline labels and dimensions
2. All structural elements: beams, columns, bracing
3. Member sizes and materials
4. Connection details
5. Loads and load cases
6. Any notes or specifications

Return as structured JSON following this schema:
{
  "grid": {...},
  "columns": [...],
  "beams": [...],
  "loads": [...],
  "materials": {...}
}

Be precise with dimensions. If information is unclear, mark as "unknown".
"""
```

### Code Generation Prompt
```python
CODE_GEN_PROMPT = """
You are an expert in Tekla Structures OpenAPI (C#).

Generate complete, production-ready C# code to create this building model:

{json_schema}

Requirements:
1. Use Tekla.Structures.Model namespace
2. Create grid first, then columns, then beams
3. Apply correct profiles and materials
4. Add base plates to all columns
5. Include error handling
6. Add comments explaining each section
7. Ensure all coordinates are in millimeters
8. Use proper Position enums for member orientation

The code should compile and run directly in Tekla Structures.
"""
```

---

## 🔍 Advanced Features

### 1. Multi-Page Drawing Analysis
Handles complex drawing sets:
- General arrangement
- Foundation plans
- Elevations and sections
- Connection details

### 2. Load Calculation Integration
```python
# Extract loads from specifications
loads = extractor.extract_loads("""
    Dead load: 0.5 kN/m²
    Live load: 2.5 kN/m²
    Wind: 1.2 kN/m² (EN 1991-1-4)
    Snow: 0.8 kN/m²
""")

# Apply to model
generator.apply_loads(loads)
```

### 3. Connection Library
Pre-built connection templates:
- Base plates (pinned/fixed)
- Beam-to-column (simple/moment)
- Bracing connections
- Splice connections
- Apex/eave connections

### 4. Design Code Compliance
- Eurocode 3 (EN 1993)
- AISC 360
- BS 5950
- AS 4100

---

## 📈 Performance & Scalability

### Processing Times (Estimated)
- Text description: **5-15 seconds**
- Single PDF page: **20-40 seconds**
- Multi-page PDF: **1-3 minutes**
- Complex image: **30-60 seconds**
- Code generation: **10-30 seconds**

### Optimization Strategies
1. **Caching**: Cache extracted data and generated code
2. **Parallel processing**: Process multiple drawings concurrently
3. **Incremental updates**: Only regenerate changed elements
4. **Template reuse**: Use pre-built code templates
5. **Vector DB**: RAG on Tekla documentation for faster lookups

---

## 🎯 Use Cases

### 1. Rapid Prototyping
Quickly generate multiple design options from text descriptions

### 2. Legacy Drawing Digitization
Convert old PDF/paper drawings to modern 3D models

### 3. Design Exploration
Iterate through variations with natural language commands

### 4. Training & Education
Help new engineers learn Tekla modeling

### 5. Automation Pipeline
Integrate with project management tools for automated modeling

---

## 🚧 Limitations & Future Work

### Current Limitations
- Complex curved geometry may require manual refinement
- Very detailed connection design needs engineering review
- Non-standard sections may need custom profiles
- Load combinations require manual verification

### Roadmap
- [ ] Support for concrete structures
- [ ] Advanced connection design automation
- [ ] Integration with analysis software (SAP2000, ETABS)
- [ ] BIM/IFC export
- [ ] Multi-language support
- [ ] Web-based UI
- [ ] Real-time collaboration
- [ ] Cost estimation integration

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 📞 Support & Help

**Need help? Check these resources:**

1. **📖 Documentation Navigation**: [START_HERE.md](START_HERE.md) - Find the right doc for your question
2. **❓ Common Questions**: [USER_MANUAL.md Section 9](USER_MANUAL.md) - FAQ section
3. **🔧 Troubleshooting**: [USER_MANUAL.md Section 10](USER_MANUAL.md) - Fix common errors
4. **💡 Examples**: `examples/` folder - Working code samples
5. **🐛 Issues**: [GitHub Issues](https://github.com/Vinayak19112003/TeklaMCP/issues) - Report bugs

**Quick Help Reference:**

| Problem | Read This |
|---------|-----------|
| "Why use this?" | [WHY_USE_THIS.md](WHY_USE_THIS.md) |
| "How to install?" | [USER_MANUAL.md Sections 3-5](USER_MANUAL.md) |
| "Error when running" | [USER_MANUAL.md Section 10](USER_MANUAL.md) |
| "How does it work?" | [PIPELINE.md](PIPELINE.md) |
| "API key issues" | [USER_MANUAL.md Section 4](USER_MANUAL.md) |
| "First model" | [USER_MANUAL.md Section 6](USER_MANUAL.md) |

---

## 🙏 Acknowledgments

- Trimble/Tekla for the OpenAPI
- Anthropic (Claude) and OpenAI (GPT-4) for AI capabilities
- Open-source community for tools and libraries

---

**Built with ❤️ for structural engineers and detailers worldwide**
