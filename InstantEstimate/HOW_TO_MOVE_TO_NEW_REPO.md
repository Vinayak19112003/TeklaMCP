# How to Move InstantEstimate to Its Own Repository

The InstantEstimate project is currently uploaded to the TeklaMCP repository as a folder.
Follow these steps to move it to the separate InstantEstimate repository.

## Current Location

**GitHub:** https://github.com/Vinayak19112003/TeklaMCP/tree/claude/ai-tekla-model-generator-01N46iAnJG1QzeZTZLd8ZbR2/InstantEstimate

**Branch:** `claude/ai-tekla-model-generator-01N46iAnJG1QzeZTZLd8ZbR2`

## Steps to Move to New Repository

### Method 1: Using GitHub Web Interface (Easiest)

1. **Navigate to the InstantEstimate folder:**
   - Go to: https://github.com/Vinayak19112003/TeklaMCP
   - Switch to branch: `claude/ai-tekla-model-generator-01N46iAnJG1QzeZTZLd8ZbR2`
   - Click on `InstantEstimate` folder

2. **Download all files:**
   - Click on each file and download it
   - OR: Click "Code" → "Download ZIP" → Extract only InstantEstimate folder

3. **Upload to InstantEstimate repository:**
   - Go to: https://github.com/Vinayak19112003/InstantEstimate
   - Click "Add file" → "Upload files"
   - Drag all the downloaded files
   - Commit message: "Initial commit: Complete InstantEstimate project"
   - Click "Commit changes"

### Method 2: Using Git Clone and Push

```bash
# Step 1: Clone TeklaMCP repository
git clone https://github.com/Vinayak19112003/TeklaMCP.git temp-tekla
cd temp-tekla

# Step 2: Switch to the branch
git checkout claude/ai-tekla-model-generator-01N46iAnJG1QzeZTZLd8ZbR2

# Step 3: Copy InstantEstimate folder
cp -r InstantEstimate ~/InstantEstimate-standalone
cd ~/InstantEstimate-standalone

# Step 4: Initialize new git repository
git init
git add .
git commit -m "Initial commit: Complete InstantEstimate project"

# Step 5: Push to InstantEstimate repository
git remote add origin https://github.com/Vinayak19112003/InstantEstimate.git
git branch -M main
git push -u origin main
```

### Method 3: Direct Download from Current Server

If you have access to the server where this is running:

```bash
# Step 1: Copy the folder
cp -r /home/user/instant-estimate ~/InstantEstimate-clean

# Step 2: Remove git history
cd ~/InstantEstimate-clean
rm -rf .git

# Step 3: Initialize new repository
git init
git add .
git commit -m "Initial commit: Complete InstantEstimate project"

# Step 4: Push to GitHub
git remote add origin https://github.com/Vinayak19112003/InstantEstimate.git
git branch -M main
git push -u origin main
```

## Files That Will Be Moved

Total: 13 files

```
InstantEstimate/
├── .gitignore                  - Git ignore rules
├── GITHUB_SETUP.md            - GitHub setup instructions
├── PUSH_TO_GITHUB.txt         - Push guide
├── README.md                  - Main documentation (7 KB)
├── app.py                     - Streamlit web interface (20 KB)
├── demo.sh                    - Demo launcher script
├── main.py                    - Main pipeline (10 KB)
├── pricing_engine.py          - Cost calculation (15 KB)
├── quantity_extractor.py      - Quantity extraction (17 KB)
├── report_generator.py        - Report generation (19 KB)
├── requirements.txt           - Dependencies
├── test_example.py            - Test suite (9 KB)
└── upload_helper.sh           - Upload helper script
```

## After Moving

1. **Delete from TeklaMCP** (optional):
   ```bash
   cd /home/user/TeklaMCP
   git rm -r InstantEstimate/
   git commit -m "Remove InstantEstimate folder (moved to separate repo)"
   git push
   ```

2. **Verify InstantEstimate repository:**
   - Go to: https://github.com/Vinayak19112003/InstantEstimate
   - Check all files are present
   - Verify README.md is displayed

3. **Update repository settings:**
   - Add description: "AI-Powered Cost Estimation Tool for Structural Steel Buildings"
   - Add topics: `ai`, `cost-estimation`, `construction`, `streamlit`, `hackathon`
   - Add website: (if you deploy it)

## Quick Download Link

You can download the entire InstantEstimate folder as a ZIP from GitHub:

**Direct link:** https://github.com/Vinayak19112003/TeklaMCP/tree/claude/ai-tekla-model-generator-01N46iAnJG1QzeZTZLd8ZbR2/InstantEstimate

Click "Code" → "Download ZIP" → Extract only the `InstantEstimate` folder

---

**Recommended:** Use Method 1 (Web Interface) - it's the easiest and requires no terminal commands!
