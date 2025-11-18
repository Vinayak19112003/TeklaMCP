# GitHub Setup Instructions

Follow these steps to upload InstantEstimate to GitHub:

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the **"+"** button (top right) → **"New repository"**
3. Fill in the details:
   - **Repository name:** `InstantEstimate` (or `instant-estimate`)
   - **Description:** `AI-Powered Cost Estimation Tool for Structural Steel Buildings`
   - **Visibility:** Choose Public or Private
   - **⚠️ IMPORTANT:** Do NOT initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /home/user/instant-estimate

# Add GitHub as remote origin (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/InstantEstimate.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded!

## Alternative: Using Git Credentials

If you get authentication errors when pushing, you'll need to:

### Option A: Personal Access Token (Recommended)

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "InstantEstimate Upload"
4. Select scopes: Check **"repo"** (full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. When pushing, use:
   ```bash
   git push -u origin main
   ```
   - Username: Your GitHub username
   - Password: Paste the token (not your GitHub password)

### Option B: GitHub CLI

```bash
# Install GitHub CLI (if not already installed)
# Then authenticate:
gh auth login

# Push using GitHub CLI
gh repo create InstantEstimate --public --source=. --push
```

## Step 4: Add Repository Topics (Optional but Recommended)

On your GitHub repository page:
1. Click **"Add topics"** (next to About section)
2. Add: `ai`, `cost-estimation`, `construction`, `steel-structures`, `streamlit`, `hackathon`, `python`, `structural-engineering`
3. This helps people discover your project!

## Step 5: Update README with GitHub Links (Optional)

You can add badges to your README:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/InstantEstimate)](https://github.com/YOUR_USERNAME/InstantEstimate/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/InstantEstimate)](https://github.com/YOUR_USERNAME/InstantEstimate/network)
[![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/InstantEstimate)](https://github.com/YOUR_USERNAME/InstantEstimate/issues)
```

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/InstantEstimate.git
```

### Error: "failed to push some refs"
```bash
# Force push (only if you're sure)
git push -u origin main --force
```

### Error: "Authentication failed"
- Make sure you're using a Personal Access Token, not your password
- GitHub disabled password authentication in 2021

## Quick Reference Commands

```bash
# Check git status
git status

# View remote URL
git remote -v

# View commit history
git log --oneline

# Add changes
git add .

# Commit changes
git commit -m "Your message"

# Push changes
git push
```

---

**Need help?** Open an issue on GitHub or check [GitHub Docs](https://docs.github.com)
