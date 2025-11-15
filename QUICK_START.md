# ⚡ Quick Start Guide - 15 Minutes to Your First Model

Get TeklaMCP running in 15 minutes!

---

## 🎯 What You'll Do

1. Install Python (5 min)
2. Get API key (3 min)
3. Setup project (5 min)
4. Generate first model (2 min)

---

## Step 1: Install Python (5 minutes)

### Windows:
1. Go to https://www.python.org/downloads/
2. Download Python 3.11
3. Run installer
4. ⚠️ **CHECK** ☑️ "Add Python to PATH"
5. Click "Install Now"

### Verify:
```bash
python --version
```
Should show: `Python 3.11.x`

---

## Step 2: Get Claude API Key (3 minutes)

1. Go to https://console.anthropic.com/
2. Sign up (free)
3. Add payment method (you only pay for usage ~$0.05 per model)
4. Go to Settings → API Keys
5. Create key
6. **Copy it** (starts with `sk-ant-...`)

---

## Step 3: Setup Project (5 minutes)

```bash
# Download project
git clone https://github.com/Vinayak19112003/TeklaMCP.git
cd TeklaMCP

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages (takes 2-3 minutes)
pip install -r requirements.txt

# Create .env file
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env
```

Now edit `.env` file and add your API key:
```bash
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

---

## Step 4: Generate Your First Model (2 minutes)

Create `test.py`:

```python
from src.input_processing import TextProcessor
from src.schema import SchemaGenerator
from src.code_generation import TeklaCodeGenerator
from src.utils import ensure_dir
from pathlib import Path

# Your building
description = """
30m x 20m warehouse, 8m high,
6m spacing, HEA300 columns,
IPE400 beams, S355 steel
"""

# Process
print("Processing...")
proc = TextProcessor()
data = proc.process(description)

print("Generating schema...")
gen = SchemaGenerator()
schema = gen.generate(data)

print("Generating code...")
code_gen = TeklaCodeGenerator()
code = code_gen.generate(schema)

# Save
output_dir = Path("output/my_first")
ensure_dir(output_dir)

with open(output_dir / "TeklaModel.cs", 'w') as f:
    f.write(code)

print(f"✅ Done! Check: {output_dir}")
```

Run it:
```bash
python test.py
```

**Result:**
```
Processing...
✅ Extracted data
Generating schema...
✅ 20 elements created
Generating code...
✅ 300 lines of C# code generated
✅ Done! Check: output/my_first
```

---

## 🎉 Success!

You just:
- ✅ Installed everything
- ✅ Got AI working
- ✅ Generated your first Tekla model

**Next:**
- Check `output/my_first/TeklaModel.cs`
- Try changing the description
- Read USER_MANUAL.md for details

---

## ⚠️ Common Issues

**"ANTHROPIC_API_KEY not found"**
→ Check `.env` file has your key

**"Module not found"**
→ Activate virtual environment: `venv\Scripts\activate`

**"Python not recognized"**
→ Reinstall Python with "Add to PATH" checked

---

## 📚 Learn More

- **Full Guide**: USER_MANUAL.md
- **Examples**: examples/ folder
- **Architecture**: ARCHITECTURE.md

**Happy building! 🏗️**
