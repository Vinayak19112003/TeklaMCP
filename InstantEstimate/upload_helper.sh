#!/bin/bash

# GitHub Upload Helper
# This script will help you push to GitHub

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          GitHub Upload Helper for InstantEstimate         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "Your repository: https://github.com/Vinayak19112003/InstantEstimate"
echo ""
echo "Choose upload method:"
echo ""
echo "1. Push via Git (requires GitHub Personal Access Token)"
echo "2. Show file list (for manual web upload)"
echo "3. Create compressed archive for download"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "To push via Git, you need a Personal Access Token:"
        echo "1. Go to: https://github.com/settings/tokens"
        echo "2. Click 'Generate new token (classic)'"
        echo "3. Select 'repo' scope"
        echo "4. Copy the token"
        echo ""
        read -p "Do you have a token ready? (y/n): " has_token

        if [ "$has_token" = "y" ]; then
            echo ""
            read -p "Enter your GitHub username (Vinayak19112003): " username
            username=${username:-Vinayak19112003}

            read -s -p "Paste your Personal Access Token: " token
            echo ""

            # Try to push using token
            git push https://${username}:${token}@github.com/Vinayak19112003/InstantEstimate.git main

            if [ $? -eq 0 ]; then
                echo ""
                echo "✅ Successfully pushed to GitHub!"
                echo "View your repo: https://github.com/Vinayak19112003/InstantEstimate"
            else
                echo ""
                echo "❌ Push failed. Try manual upload (option 2)"
            fi
        fi
        ;;

    2)
        echo ""
        echo "Files to upload manually to GitHub:"
        echo "─────────────────────────────────────"
        ls -lh *.py *.sh *.md *.txt 2>/dev/null | awk '{print $9, "(" $5 ")"}'
        echo ""
        echo "📋 Upload Instructions:"
        echo "1. Go to: https://github.com/Vinayak19112003/InstantEstimate"
        echo "2. Click 'Add file' → 'Upload files'"
        echo "3. Drag all files from instant-estimate/ folder"
        echo "4. Commit changes"
        echo ""
        echo "Or create files one by one:"
        echo "- Click 'Add file' → 'Create new file'"
        echo "- Copy filename and content from this directory"
        ;;

    3)
        echo ""
        echo "Creating archive..."
        tar -czf InstantEstimate.tar.gz *.py *.sh *.md *.txt .gitignore 2>/dev/null
        echo "✅ Created: InstantEstimate.tar.gz"
        echo ""
        echo "Location: $(pwd)/InstantEstimate.tar.gz"
        echo ""
        echo "Download this file and extract it locally, then:"
        echo "cd InstantEstimate"
        echo "git init"
        echo "git add ."
        echo "git commit -m 'Initial commit'"
        echo "git remote add origin https://github.com/Vinayak19112003/InstantEstimate.git"
        echo "git push -u origin main"
        ;;
esac
