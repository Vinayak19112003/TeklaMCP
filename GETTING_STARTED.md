# Getting Started - AI Tekla Model Generator

Quick start guide to get up and running in 15 minutes.

---

## ⚡ Quick Start (5 Steps)

### Step 1: Clone and Setup (2 minutes)

```bash
# Clone the repository
git clone https://github.com/yourrepo/TeklaMCP.git
cd TeklaMCP

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use any text editor
```

Add your keys:
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

Get API keys:
- **Claude**: https://console.anthropic.com/
- **OpenAI**: https://platform.openai.com/api-keys

### Step 3: Install .NET SDK (3 minutes)

Download and install .NET SDK:
- **Download**: https://dotnet.microsoft.com/download
- **Version**: 6.0 or later

Verify installation:
```bash
dotnet --version
```

### Step 4: Install Tekla Structures (if not already installed)

- Download Tekla Structures (2021 or later)
- Install with OpenAPI support enabled
- Launch Tekla and create a new model

### Step 5: Run Your First Generation (2 minutes)

```bash
# Generate from text
python example_usage.py
```

Or create a simple script:

```python
from src.main import TeklaAIGenerator

generator = TeklaAIGenerator()

result = generator.from_text("""
    30m x 20m warehouse,
    8m height,
    HEA300 columns,
    IPE400 beams,
    S355 steel
""")

result.save("output/my_first_building")
```

Run it:
```bash
python my_first_generation.py
```

Check outputs:
```bash
ls output/my_first_building/
# extracted.json
# schema.json
# TeklaModel.cs
```

---

## 📖 Understanding the Workflow

```
Your Input → AI Processing → Tekla Code → 3D Model
```

### What Happens:

1. **Input**: You provide text, PDF, or image
2. **AI Extraction**: Claude/GPT-4 extracts structural details
3. **Schema Generation**: Data converted to validated JSON
4. **Code Generation**: Tekla C# code created
5. **Execution**: Code runs in Tekla to create 3D model

---

## 🎯 Your First Building

### Example: Simple Warehouse

**Input:**
```python
description = """
Create an industrial warehouse:
- 40 meters long x 25 meters wide
- 10 meter eave height
- 8 meter column spacing in both directions
- UC305x305x198 columns, S355 steel
- UB457x191x74 roof beams
- Simple base plates with 4xM24 bolts
"""

generator = TeklaAIGenerator()
result = generator.from_text(description)
```

**What You Get:**

1. **extracted.json** - Raw extracted data:
```json
{
  "building_type": "industrial_warehouse",
  "dimensions": {
    "length": 40000,
    "width": 25000,
    "height": 10000
  },
  "grid": {
    "x_spacing": 8000,
    "y_spacing": 8000,
    "x_count": 5,
    "y_count": 3
  },
  "columns": {
    "profile": "UC305x305x198",
    "material": "S355"
  }
}
```

2. **schema.json** - Validated building schema with all elements

3. **TeklaModel.cs** - Complete C# code:
```csharp
using Tekla.Structures.Model;

public class WarehouseModel
{
    public void CreateModel()
    {
        Model model = new Model();
        CreateGrid();
        CreateColumns();
        CreateBeams();
        model.CommitChanges();
    }
    // ... full implementation
}
```

### Compile and Run:

```bash
cd output/my_first_building

# Compile
dotnet build TeklaModel.cs

# Run (Tekla must be open)
dotnet run
```

**Result**: Complete 3D warehouse model appears in Tekla!

---

## 🔄 Making Changes

### Iterative Refinement

```python
# Initial model
result = generator.from_text("30m x 20m building, HEA300 columns")

# Make modification
updated = generator.modify(result.schema, """
    Change all columns to UC356x406x287
    and add bracing on perimeter bays
""")

# Save updated model
updated.save("output/updated_building")
```

The AI understands natural language modifications:
- "Change all columns to X"
- "Add bracing between grid lines A and B"
- "Increase spacing to 10m"
- "Use S355J2 material instead"

---

## 📁 File Structure

```
TeklaMCP/
├── README.md              ← Start here for overview
├── GETTING_STARTED.md     ← You are here!
├── ARCHITECTURE.md        ← Deep dive into system design
├── PIPELINE.md            ← How data flows through system
├── IMPLEMENTATION_GUIDE.md ← Step-by-step implementation
│
├── requirements.txt       ← Python dependencies
├── .env.example          ← Configuration template
├── example_usage.py      ← Usage examples
│
└── src/                  ← Source code (you'll implement this)
    ├── input_processing/
    ├── extraction/
    ├── schema/
    ├── code_generation/
    └── execution/
```

---

## 🎓 Learning Path

### Beginner (Week 1)
1. ✅ Read README.md
2. ✅ Follow this GETTING_STARTED guide
3. ✅ Run example_usage.py
4. ✅ Generate your first building from text
5. ✅ Try modifying a generated model

### Intermediate (Week 2)
1. ✅ Read ARCHITECTURE.md
2. ✅ Implement TextProcessor
3. ✅ Implement SchemaGenerator
4. ✅ Implement TeklaCodeGenerator
5. ✅ Test with various building types

### Advanced (Week 3+)
1. ✅ Read PIPELINE.md
2. ✅ Implement PDFProcessor with Vision AI
3. ✅ Add RAG system for Tekla API
4. ✅ Implement FeedbackProcessor
5. ✅ Build web interface (optional)
6. ✅ Deploy as API service (optional)

---

## 💡 Tips for Success

### 1. Start Simple
Begin with text-only inputs:
```python
"20m x 15m building, HEA200 columns, IPE300 beams"
```

Don't start with complex PDFs or multi-story buildings.

### 2. Validate Each Stage
Check outputs at each step:
- Extracted data makes sense?
- Schema looks correct?
- Code compiles?
- Model creates successfully?

### 3. Use Good Descriptions
**Bad:**
```
"Make a building"
```

**Good:**
```
"Create a 30m x 20m industrial building with:
- 6m bay spacing
- 8m height
- HEA300 columns
- IPE400 beams
- S355 steel
- Simple base plates"
```

More detail = better results!

### 4. Check API Quotas
- Claude: https://console.anthropic.com/usage
- OpenAI: https://platform.openai.com/usage

Monitor your usage to avoid surprises.

### 5. Cache When Possible
Processing PDFs costs API credits. Enable caching:
```python
# In .env
CACHE_ENABLED=true
```

Re-processing the same file? Instant results from cache!

---

## 🐛 Troubleshooting

### Issue: "ANTHROPIC_API_KEY not found"
```
Solution:
1. Check .env file exists
2. Check API key is correct
3. Check you've loaded .env (use python-dotenv)
```

### Issue: "Tekla not connected"
```
Solution:
1. Launch Tekla Structures
2. File → New Model
3. Leave model open
4. Run your code
```

### Issue: "Code compilation failed"
```
Solution:
1. Check .NET SDK installed: dotnet --version
2. Check Tekla API references in code
3. Read error message carefully
4. Common fix: Use * not x in profile strings
   ✓ "UC305*305*198"
   ✗ "UC305x305x198"
```

### Issue: "Low quality extraction"
```
Solution:
1. Provide more detail in input
2. Use higher quality images/PDFs
3. Try different AI model (GPT-4 vs Claude)
4. Add examples in prompts
```

### Issue: "Model created but looks wrong"
```
Solution:
1. Check extracted.json - is data correct?
2. Check schema.json - elements in right place?
3. Verify grid coordinates
4. Check units (should be millimeters)
5. Test with simpler building first
```

---

## 📚 Next Steps

### After First Successful Generation:

1. **Try Different Building Types**
   - Warehouse
   - Portal frame
   - Multi-story office
   - Shed/canopy

2. **Experiment with Modifications**
   - Change member sizes
   - Add/remove bracing
   - Modify spacing
   - Change materials

3. **Process a PDF Drawing**
   ```python
   result = generator.from_pdf("plan.pdf")
   ```

4. **Read Detailed Docs**
   - ARCHITECTURE.md - understand system design
   - PIPELINE.md - understand data flow
   - IMPLEMENTATION_GUIDE.md - implement features

5. **Contribute**
   - Add new features
   - Improve prompts
   - Add connection types
   - Share your results!

---

## 🤝 Getting Help

### Resources
- **Documentation**: Read all .md files in repo
- **Examples**: See example_usage.py
- **Code**: Check IMPLEMENTATION_GUIDE.md

### Community (Future)
- GitHub Issues
- Discord/Slack channel
- Stack Overflow tag

### Professional Support
- Contact: support@yourdomain.com
- Consulting available for:
  - Custom implementations
  - Enterprise deployment
  - Training and workshops

---

## ✅ Checklist

Before you begin, make sure you have:

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env file configured with API keys
- [ ] .NET SDK installed
- [ ] Tekla Structures installed (optional for execution)
- [ ] Read README.md
- [ ] Tested API keys work

Ready to implement:
- [ ] Implemented TextProcessor
- [ ] Implemented SchemaGenerator
- [ ] Implemented TeklaCodeGenerator
- [ ] Generated first building successfully
- [ ] Modified generated building
- [ ] Ready to process PDFs (advanced)

---

## 🎉 Success!

You've generated your first AI-powered Tekla model!

**What you've achieved:**
- ✅ Set up development environment
- ✅ Configured AI APIs
- ✅ Generated building from text
- ✅ Created Tekla 3D model
- ✅ Saved reusable code

**You can now:**
- Generate buildings from simple descriptions
- Modify existing models with natural language
- Create consistent, standard-compliant models
- Save hours of manual modeling time

---

## 📈 Performance Expectations

| Task | Time | Credits |
|------|------|---------|
| Simple text (warehouse) | 15-30s | $0.05 |
| Complex text (portal frame) | 30-60s | $0.10 |
| PDF (single page) | 1-2 min | $0.15 |
| PDF (multi-page) | 3-5 min | $0.30 |
| Modification | 10-20s | $0.03 |

**Note**: Times approximate, credits based on Claude Sonnet pricing

---

**Happy Building! 🏗️**

Questions? Check the other documentation files or open an issue on GitHub.
