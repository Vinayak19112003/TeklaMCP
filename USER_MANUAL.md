# 📘 TeklaMCP User Manual - Complete Beginner's Guide

**AI-Powered Tekla Structures Model Generator**

This manual will guide you through **everything** from installation to generating your first 3D model, even if you're a complete beginner.

---

## 📑 Table of Contents

1. [What is TeklaMCP?](#what-is-teklamcp)
2. [What You'll Need](#what-youll-need)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Getting API Keys](#getting-api-keys)
5. [Installing Software](#installing-software)
6. [Setting Up TeklaMCP](#setting-up-teklamcp)
7. [Your First Model](#your-first-model)
8. [Understanding the System](#understanding-the-system)
9. [Common Questions](#common-questions)
10. [Troubleshooting](#troubleshooting)
11. [Advanced Usage](#advanced-usage)

---

## 🎯 What is TeklaMCP?

**TeklaMCP** is an AI system that automatically creates 3D structural models in Tekla Structures.

### What It Does:
```
You Type: "Create a 40m x 30m warehouse with HEA300 columns"
           ↓
AI Processes: Understands the description
           ↓
Generates: Complete Tekla 3D model code
           ↓
Result: Full building model in Tekla Structures
```

### Real Example:
**Before (Manual - 4 hours):**
- Open Tekla
- Click to create grid (15 minutes)
- Manually place 24 columns one by one (1 hour)
- Manually create 48 beams (1.5 hours)
- Add connections manually (1 hour)
- Check and fix errors (30 minutes)

**After (With TeklaMCP - 2 minutes):**
- Type description
- Click generate
- **Done!** Complete model created

---

## 🛠️ What You'll Need

### 1. Computer Requirements
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space
- **Internet**: For AI processing

### 2. Software (We'll install these)
- ✅ Python 3.10 or newer
- ✅ Git (for downloading project)
- ✅ .NET SDK 6.0 or newer
- ✅ Tekla Structures (optional for viewing models)
- ✅ Text editor (VS Code recommended)

### 3. Accounts Needed (Free)
- ✅ Anthropic Claude account (for AI)
- ✅ GitHub account (optional)

### 4. Costs
- **TeklaMCP**: FREE ✅
- **Python/Git/.NET**: FREE ✅
- **Claude API**: Pay-as-you-go (~$0.05 per model)
- **Tekla Structures**: Commercial software (trial available)

---

## 📝 Step-by-Step Setup

### PART 1: Install Python

#### Windows:

**Step 1:** Go to https://www.python.org/downloads/

**Step 2:** Click **"Download Python 3.11.x"** (or latest version)

**Step 3:** Run the installer
- ⚠️ **IMPORTANT**: Check ☑️ **"Add Python to PATH"**
- Click **"Install Now"**

**Step 4:** Verify installation
```bash
# Open Command Prompt (Press Win+R, type cmd, press Enter)
python --version
```
You should see: `Python 3.11.x`

#### Mac/Linux:
```bash
# Mac (using Homebrew)
brew install python@3.11

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11 python3-pip

# Verify
python3 --version
```

---

### PART 2: Install Git

#### Windows:

**Step 1:** Go to https://git-scm.com/download/win

**Step 2:** Download and run installer
- Use default settings (just keep clicking "Next")

**Step 3:** Verify
```bash
git --version
```
You should see: `git version 2.x.x`

#### Mac/Linux:
```bash
# Mac
brew install git

# Linux
sudo apt install git

# Verify
git --version
```

---

### PART 3: Install .NET SDK

#### Windows:

**Step 1:** Go to https://dotnet.microsoft.com/download

**Step 2:** Download **.NET 8.0 SDK** (or latest)

**Step 3:** Run installer (use default settings)

**Step 4:** Verify
```bash
dotnet --version
```
You should see: `8.0.xxx`

#### Mac/Linux:
```bash
# Mac
brew install dotnet-sdk

# Linux - follow instructions at:
# https://learn.microsoft.com/en-us/dotnet/core/install/linux

# Verify
dotnet --version
```

---

### PART 4: Install Tekla Structures (Optional)

⚠️ **Note**: Tekla is needed to **view** the final 3D models. You can generate code without it.

#### Option A: Get Tekla (Commercial)

**Step 1:** Go to https://www.tekla.com/

**Step 2:** Contact Tekla for:
- Free trial (30 days)
- Educational license (if student)
- Commercial license (purchase)

**Step 3:** Download and install
- Follow Tekla installer instructions
- Install version 2021 or newer

#### Option B: Skip Tekla for Now
- You can still generate the C# code
- Code can be run later when you have Tekla
- Focus on learning the AI system first

---

### PART 5: Install VS Code (Text Editor)

**Step 1:** Go to https://code.visualstudio.com/

**Step 2:** Download and install

**Step 3:** Open VS Code

**Step 4:** Install Python extension
- Click Extensions icon (left sidebar)
- Search "Python"
- Install "Python" by Microsoft

---

## 🔑 Getting API Keys

### Get Claude API Key (Required)

**Step 1:** Go to https://console.anthropic.com/

**Step 2:** Create account
- Click **"Sign Up"**
- Use email and password
- Verify email

**Step 3:** Add payment method
- Go to **Settings** → **Billing**
- Add credit/debit card
- ⚠️ You only pay for what you use (~$0.05 per model)

**Step 4:** Get API key
- Go to **Settings** → **API Keys**
- Click **"Create Key"**
- Copy the key (starts with `sk-ant-...`)
- ⚠️ **SAVE THIS KEY SECURELY** - you'll need it later

**Example key format:**
```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Get OpenAI API Key (Optional)

If you want to use GPT-4 as backup:

**Step 1:** Go to https://platform.openai.com/

**Step 2:** Create account

**Step 3:** Go to API Keys

**Step 4:** Create new key

**Step 5:** Copy key (starts with `sk-...`)

---

## 💻 Setting Up TeklaMCP

### Step 1: Download the Project

**Option A: Using Git (Recommended)**

```bash
# Open Command Prompt or Terminal

# Navigate to where you want the project
cd C:\Users\YourName\Documents

# Clone the project
git clone https://github.com/Vinayak19112003/TeklaMCP.git

# Enter project folder
cd TeklaMCP
```

**Option B: Download ZIP**

1. Go to the GitHub repository
2. Click green **"Code"** button
3. Click **"Download ZIP"**
4. Extract ZIP to `C:\Users\YourName\Documents\TeklaMCP`

### Step 2: Open Project in VS Code

```bash
# If you're in the TeklaMCP folder:
code .
```

Or:
1. Open VS Code
2. File → Open Folder
3. Select `TeklaMCP` folder

### Step 3: Create Virtual Environment

```bash
# In VS Code, open Terminal (View → Terminal)

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# You should see (venv) before your prompt
```

### Step 4: Install Python Packages

```bash
# Make sure virtual environment is active (you see "venv")

# Install all required packages
pip install -r requirements.txt

# This will take 2-5 minutes
# You'll see packages installing...
```

**What gets installed:**
- `anthropic` - Claude AI
- `openai` - GPT-4 (optional)
- `pydantic` - Data validation
- `PyMuPDF` - PDF processing
- `opencv-python` - Image processing
- `pytesseract` - OCR
- And more...

### Step 5: Configure API Keys

**Step 1:** Create `.env` file

```bash
# Copy the example file
# Windows:
copy .env.example .env

# Mac/Linux:
cp .env.example .env
```

**Step 2:** Edit `.env` file

Open `.env` in VS Code and add your API keys:

```bash
# AI API Keys
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
OPENAI_API_KEY=sk-YOUR_OPENAI_KEY_HERE  # Optional

# Leave these empty for now
AZURE_VISION_KEY=
AZURE_VISION_ENDPOINT=
GOOGLE_VISION_KEY=

# Application Settings (keep defaults)
LOG_LEVEL=INFO
MAX_FILE_SIZE_MB=50
CACHE_ENABLED=true
CACHE_TTL_HOURS=24

# Processing Settings
AUTO_EXECUTE=false
PARALLEL_PROCESSING=true
MAX_WORKERS=4

# Tekla Settings (update if you installed Tekla)
TEKLA_VERSION=2023
TEKLA_API_PATH=C:\Program Files\Tekla Structures\2023.0\nt\bin\plugins

# Development
DEBUG=false
SAVE_INTERMEDIATE_RESULTS=true
```

**Step 3:** Save the file (Ctrl+S)

---

## 🚀 Your First Model

### Example 1: Simple Warehouse (Text to Model)

Let's create your first building!

**Step 1:** Create a test file

```bash
# Create a new file called test.py
# In VS Code: File → New File
# Save as: test.py
```

**Step 2:** Copy this code into `test.py`:

```python
"""
My First TeklaMCP Model
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from input_processing import TextProcessor
from schema import SchemaGenerator, SchemaValidator
from code_generation import TeklaCodeGenerator
from utils import ensure_dir
import json

def main():
    print("=" * 60)
    print("Creating My First Warehouse")
    print("=" * 60)

    # Your building description
    description = """
    Create a simple warehouse:
    - 30 meters long
    - 20 meters wide
    - 8 meters high
    - 6 meter column spacing
    - HEA300 columns
    - IPE400 beams
    - S355 steel
    - Simple base plates
    """

    print("\n📝 Step 1: Processing your description...")
    print(f"Description: {description.strip()}")

    # Process text
    processor = TextProcessor()
    extracted_data = processor.process(description)

    print(f"✅ Extracted {len(extracted_data)} data fields")
    print(f"   - Building type: {extracted_data.get('building_type')}")
    print(f"   - Dimensions: {extracted_data.get('dimensions')}")

    print("\n📐 Step 2: Generating building schema...")

    # Generate schema
    schema_gen = SchemaGenerator()
    schema = schema_gen.generate(extracted_data)

    print(f"✅ Schema created:")
    print(f"   - Grid: {len(schema.grid.x_lines)} x {len(schema.grid.y_lines)}")
    print(f"   - Columns: {len([e for e in schema.elements if e.type == 'column'])}")
    print(f"   - Beams: {len([e for e in schema.elements if e.type == 'beam'])}")
    print(f"   - Total elements: {len(schema.elements)}")

    print("\n✅ Step 3: Validating schema...")

    # Validate
    validator = SchemaValidator()
    is_valid, warnings = validator.validate(schema)

    if is_valid:
        print("✅ Validation PASSED")
    else:
        print("❌ Validation FAILED")

    if warnings:
        print(f"   Warnings: {len(warnings)}")
        for w in warnings[:3]:  # Show first 3
            print(f"   - [{w.severity}] {w.message}")

    print("\n💻 Step 4: Generating Tekla C# code...")

    # Generate code
    code_gen = TeklaCodeGenerator()
    code = code_gen.generate(schema)

    lines = len(code.split('\n'))
    print(f"✅ Generated {lines} lines of C# code")

    print("\n💾 Step 5: Saving files...")

    # Save outputs
    output_dir = Path(__file__).parent / "output" / "my_first_warehouse"
    ensure_dir(output_dir)

    # Save extracted data
    with open(output_dir / "extracted_data.json", 'w') as f:
        json.dump(extracted_data, f, indent=2)

    # Save schema
    with open(output_dir / "schema.json", 'w') as f:
        f.write(schema.model_dump_json(indent=2))

    # Save C# code
    with open(output_dir / "TeklaModel.cs", 'w') as f:
        f.write(code)

    print(f"✅ All files saved to: {output_dir}")
    print("\n📂 Generated files:")
    print(f"   1. extracted_data.json - Raw extracted data")
    print(f"   2. schema.json - Validated building schema")
    print(f"   3. TeklaModel.cs - Tekla C# code")

    print("\n🎉 SUCCESS! Your first model is ready!")

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("\n1. View the generated files:")
    print(f"   - Open: {output_dir}")
    print("\n2. To run in Tekla (if installed):")
    print(f"   - Open Tekla Structures")
    print(f"   - File → New Model")
    print(f"   - Copy TeklaModel.cs content")
    print(f"   - Run as Tekla macro")
    print("\n3. Try modifying the description:")
    print("   - Change dimensions")
    print("   - Change column sizes")
    print("   - Add more details")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
```

**Step 3:** Run it!

```bash
# Make sure virtual environment is active (you see "venv")
python test.py
```

**What Happens:**

```
============================================================
Creating My First Warehouse
============================================================

📝 Step 1: Processing your description...
✅ Extracted 8 data fields

📐 Step 2: Generating building schema...
✅ Schema created:
   - Grid: 6 x 4
   - Columns: 24
   - Beams: 48
   - Total elements: 72

✅ Step 3: Validating schema...
✅ Validation PASSED

💻 Step 4: Generating Tekla C# code...
✅ Generated 350 lines of C# code

💾 Step 5: Saving files...
✅ All files saved to: output/my_first_warehouse

🎉 SUCCESS! Your first model is ready!
```

**Step 4:** Check the output

```bash
# Navigate to output folder
cd output/my_first_warehouse

# You'll find:
# - extracted_data.json (what AI understood)
# - schema.json (validated structure)
# - TeklaModel.cs (Tekla code)
```

**Step 5:** View the files

Open `schema.json` to see the building structure:
```json
{
  "metadata": {
    "name": "warehouse",
    "design_code": "EC3"
  },
  "grid": {
    "x_lines": [
      {"label": "1", "coordinate": 0},
      {"label": "2", "coordinate": 6000},
      {"label": "3", "coordinate": 12000},
      ...
    ]
  },
  "elements": [
    {
      "id": "COL-1",
      "type": "column",
      "profile": "HEA300",
      "start_point": {"x": 0, "y": 0, "z": 0},
      "end_point": {"x": 0, "y": 0, "z": 8000}
    },
    ...
  ]
}
```

Open `TeklaModel.cs` to see the Tekla code (C#):
```csharp
using System;
using Tekla.Structures.Model;
using Tekla.Structures.Geometry3d;

namespace AutoGeneratedModel
{
    public class WarehouseBuilder
    {
        private Model _model;

        public void CreateModel()
        {
            _model = new Model();

            if (!_model.GetConnectionStatus())
            {
                Console.WriteLine("Tekla not connected!");
                return;
            }

            CreateGrid();
            CreateColumns();
            CreateBeams();

            _model.CommitChanges();
            Console.WriteLine("Model created successfully!");
        }

        private void CreateGrid()
        {
            // Grid creation code...
        }

        private void CreateColumns()
        {
            // Column creation code...
        }
        // ...
    }
}
```

---

## 🏃 Running in Tekla Structures

If you have Tekla installed:

### Method 1: Copy-Paste (Easiest)

**Step 1:** Open Tekla Structures
- Start Tekla
- File → New Model
- Choose template (e.g., "metric")

**Step 2:** Open the generated `TeklaModel.cs` file
- Copy all content (Ctrl+A, Ctrl+C)

**Step 3:** In Tekla:
- Applications → Plugins → (create new plugin)
- Paste the code
- Click "Run"

**Step 4:** Watch your model appear! 🎉

### Method 2: Compile and Run (Advanced)

```bash
# Navigate to output folder
cd output/my_first_warehouse

# Create project file
dotnet new console -n TeklaModel

# Replace Program.cs with TeklaModel.cs
# Then build
dotnet build

# Run (Tekla must be open)
dotnet run
```

---

## 📖 Understanding the System

### How It Works (Simple Explanation)

```
1. You Write Text
   ↓
   "40m x 30m warehouse, HEA300 columns"

2. TextProcessor (AI reads it)
   ↓
   Claude AI understands: length=40000mm, width=30000mm, etc.

3. SchemaGenerator (Creates structure)
   ↓
   Converts to organized data (JSON)

4. SchemaValidator (Checks it)
   ↓
   Makes sure everything is correct

5. TeklaCodeGenerator (Writes code)
   ↓
   Claude AI writes C# code for Tekla

6. Output: TeklaModel.cs
   ↓
   Ready to run in Tekla!
```

### The Files Explained

**Input Files:**
- Your text description
- OR PDF drawing
- OR image/sketch

**Processing Files (src/):**
- `input_processing/` - Reads your input
- `extraction/` - Extracts building details
- `schema/` - Organizes data
- `code_generation/` - Writes Tekla code

**Output Files:**
- `extracted_data.json` - What AI understood
- `schema.json` - Organized building data
- `TeklaModel.cs` - Tekla code

**Templates:**
- `src/code_generation/templates/*.cs` - Code patterns

---

## ❓ Common Questions

### Q1: Do I need Tekla Structures installed?

**A:** No, not immediately.
- You can generate the C# code without Tekla
- You only need Tekla to **view** the final 3D model
- Focus on learning the AI system first

### Q2: How much does it cost?

**A:**
- **TeklaMCP software**: FREE
- **Claude API**: ~$0.05-0.10 per building model
- **Tekla Structures**: Commercial (trial available)

### Q3: Do I need to know programming?

**A:** No!
- Just write text descriptions
- The AI does the programming
- Examples are provided

### Q4: What if I get errors?

**A:** Common fixes:
1. Check API key in `.env` file
2. Make sure virtual environment is active
3. See [Troubleshooting](#troubleshooting) section

### Q5: Can I use PDF drawings?

**A:** Yes!
```python
from input_processing import PDFProcessor

processor = PDFProcessor()
result = processor.process("my_drawing.pdf")
```

### Q6: Can I modify the generated model?

**A:** Yes! Two ways:
1. **Edit description** and regenerate
2. **Use feedback system**:
```python
from feedback import ModificationParser, SchemaUpdater

feedback = "Change all columns to UC356x406x287"
# System updates and regenerates
```

### Q7: What building types can I create?

**A:** Any steel structure:
- Warehouses
- Portal frames
- Office buildings
- Industrial buildings
- Sheds/shelters
- Custom structures

### Q8: Is my data secure?

**A:**
- Your descriptions are sent to Claude AI for processing
- No data is stored by Anthropic after processing
- Your generated models stay on your computer

---

## 🔧 Troubleshooting

### Problem 1: "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
# 1. Check .env file exists
ls .env

# 2. Open .env and verify key is there
# Should look like:
# ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# 3. Make sure no spaces around =
# ✅ ANTHROPIC_API_KEY=sk-ant-xxx
# ❌ ANTHROPIC_API_KEY = sk-ant-xxx

# 4. Restart your program
```

### Problem 2: "Module not found" error

**Solution:**
```bash
# 1. Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# 2. Reinstall packages
pip install -r requirements.txt

# 3. Verify installation
pip list
```

### Problem 3: "Python not recognized"

**Solution:**
```bash
# Windows:
# 1. Reinstall Python
# 2. CHECK "Add Python to PATH"
# 3. Restart Command Prompt

# Verify:
python --version

# If still not working, use full path:
C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe
```

### Problem 4: Claude API errors

**Solution:**
```bash
# Error: "Invalid API key"
# - Check key is correct in .env
# - No extra spaces
# - Key starts with sk-ant-

# Error: "Rate limit exceeded"
# - Wait a few minutes
# - You're making too many requests

# Error: "Insufficient credits"
# - Add payment method at console.anthropic.com
# - Add $10-20 credit
```

### Problem 5: Generated code has errors

**Solution:**
```bash
# 1. Check the schema.json first
# Make sure data looks correct

# 2. Try regenerating with more detail:
description = """
Create warehouse:
- EXACTLY 40 meters long
- EXACTLY 30 meters wide
- 8 meters eave height
- 6 meter bay spacing in BOTH directions
- Use HEA300 sections for ALL columns
- Use IPE400 for ALL beams
- Material: S355 steel
"""

# 3. Check validation warnings
# Run validator and fix issues
```

### Problem 6: "Tekla not connected"

**Solution:**
```bash
# 1. Open Tekla Structures first
# 2. Create or open a model (File → New Model)
# 3. Then run your code

# Or: Generate code without executing
# Just save the .cs file and run it later
```

---

## 🎓 Learning Path

### Week 1: Basics
**Day 1-2:** Setup
- ✅ Install all software
- ✅ Get API keys
- ✅ Run first example

**Day 3-4:** Simple Buildings
- ✅ Try different descriptions
- ✅ Change dimensions
- ✅ Try different sections

**Day 5-7:** Understand Output
- ✅ Read schema.json
- ✅ Understand element structure
- ✅ View generated C# code

### Week 2: Intermediate
**Day 1-3:** Complex Buildings
- ✅ Multi-story buildings
- ✅ Different grid layouts
- ✅ Custom connections

**Day 4-5:** PDF Processing
- ✅ Process PDF drawings
- ✅ Extract from images
- ✅ Combine sources

**Day 6-7:** Modifications
- ✅ Use feedback system
- ✅ Iterative design
- ✅ Fine-tune models

### Week 3: Advanced
- ✅ Custom code templates
- ✅ Add new element types
- ✅ Create connection library
- ✅ Integrate with Tekla

---

## 💡 Usage Examples

### Example 1: Portal Frame Building

```python
description = """
Create a portal frame building:
- 50 meters long
- 25 meters wide
- 8 meters eave height
- 10 meters ridge height
- 6 meter bay spacing
- UB533x210x101 columns
- UB457x191x74 rafters
- S355 steel
- Moment connections at eaves and apex
"""

# Process and generate...
```

### Example 2: Multi-Story Office

```python
description = """
Create an office building:
- 30m x 20m footprint
- 4 floors
- 3.5m floor height
- 6m column spacing
- UC305x305x198 columns
- UB457x191x74 floor beams
- Simple connections
- S355 steel
"""
```

### Example 3: Industrial Shed

```python
description = """
Create industrial shed:
- 60m long x 40m wide
- 12m eave height
- 10m column spacing
- Heavy columns UC356x406x287
- Roof beams UB610x229x125
- X-bracing on all perimeter bays
- S355 steel
- Crane beam at 9m height (optional)
"""
```

### Example 4: From PDF

```python
from input_processing import PDFProcessor

processor = PDFProcessor()

# Process your PDF drawing
result = processor.process("path/to/your/structural_plan.pdf")

# Generate schema and code as usual
schema_gen = SchemaGenerator()
schema = schema_gen.generate(result)

code_gen = TeklaCodeGenerator()
code = code_gen.generate(schema)
```

---

## 🎯 Tips for Best Results

### Writing Good Descriptions

**❌ Bad (Too Vague):**
```
"Make a building"
```

**✅ Good (Clear Details):**
```
"Create a 40m x 30m warehouse, 10m high,
8m column spacing, HEA300 columns,
IPE400 beams, S355 steel, simple base plates"
```

### Include These Details:

1. **Dimensions**
   - Length, width, height
   - Use meters: "40m" or "40 meters"

2. **Grid/Spacing**
   - Column spacing: "6m spacing" or "6 meter bays"
   - Can be different in X and Y directions

3. **Member Sizes**
   - Columns: "HEA300" or "UC305x305x198"
   - Beams: "IPE400" or "UB457x191x74"

4. **Material**
   - Steel grade: "S355", "S275", "S235"

5. **Connections** (optional)
   - "Simple base plates"
   - "4xM24 bolts"
   - "Moment connections"

### Example Template:

```
Create a [building type]:
- [length]m long x [width]m wide
- [height]m high (or eave height)
- [spacing]m column spacing
- [section] columns
- [section] beams
- [material] steel
- [connection type] connections
- [additional details]
```

---

## 📊 Cost Breakdown

### Per Building Model:

| Item | Cost |
|------|------|
| Text processing | $0.01 - $0.02 |
| PDF processing (1 page) | $0.05 - $0.10 |
| PDF processing (multi-page) | $0.10 - $0.30 |
| Code generation | $0.02 - $0.05 |
| **Total (text)** | **~$0.05** |
| **Total (PDF)** | **~$0.15** |

### Monthly Estimate:

If you generate **20 buildings per month**:
- Cost: ~$1 - $3 per month
- Much cheaper than manual modeling time!

---

## 🚀 Advanced Usage

### Custom Templates

You can modify C# templates in:
```
src/code_generation/templates/
```

### Add Custom Element Types

Edit:
```python
# src/schema/models/element.py

class ElementType(str, Enum):
    COLUMN = "column"
    BEAM = "beam"
    # Add your custom type:
    CUSTOM = "custom_element"
```

### Create Connection Library

Add standard connections:
```python
# src/schema/models/connection.py

# Define your standard connections
STANDARD_BASE_PLATE = Connection(
    type="base_plate",
    bolts=BoltSpecification(size="M24", quantity=4)
)
```

---

## 📞 Getting Help

### If You're Stuck:

1. **Check this manual** - Most answers are here
2. **Read error messages** - They usually tell you what's wrong
3. **Check examples/** folder - Working examples provided
4. **Review logs** - Check `output/` folder for error details

### Resources:

- **Tekla API Docs**: `tekla_api/OpenAPI_Reference.md`
- **Architecture**: `ARCHITECTURE.md`
- **Examples**: `examples/` folder
- **Tests**: `tests/` folder

---

## ✅ Quick Reference

### Daily Workflow:

```bash
# 1. Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 2. Run your script
python my_script.py

# 3. Check output
cd output/
# View generated files

# 4. Deactivate when done
deactivate
```

### File Locations:

```
TeklaMCP/
├── .env                    # Your API keys HERE
├── test.py                 # Your test scripts
├── output/                 # Generated files appear HERE
├── examples/               # Example scripts
└── src/                    # Don't modify unless advanced
```

### Common Commands:

```bash
# Check Python
python --version

# Check packages
pip list

# Install package
pip install package-name

# Run example
python examples/simple_building.py

# Check files
dir          # Windows
ls -la       # Mac/Linux
```

---

## 🎉 Congratulations!

You now know how to:
- ✅ Set up TeklaMCP
- ✅ Get API keys
- ✅ Generate your first model
- ✅ Understand the system
- ✅ Troubleshoot problems
- ✅ Use advanced features

**Start experimenting and have fun! 🚀**

---

## 📝 Summary Checklist

Before you start, make sure:

- [ ] Python 3.10+ installed
- [ ] Git installed
- [ ] .NET SDK installed
- [ ] Claude API key obtained
- [ ] Project downloaded
- [ ] Virtual environment created
- [ ] Packages installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with API key
- [ ] First example runs successfully

**If all checked, you're ready to go! 🎊**

---

**Version**: 1.0
**Last Updated**: 2025-11-15
**Author**: TeklaMCP Team

For questions or issues, check the documentation files or review the examples folder.
