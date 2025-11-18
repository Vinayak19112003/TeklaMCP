#!/bin/bash

# InstantEstimate Demo Launcher
# This script sets up the environment and launches the application

echo "╔════════════════════════════════════════════════════════════╗"
echo "║             InstantEstimate - Demo Launcher               ║"
echo "║        AI-Powered Structural Cost Estimation Tool         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check Python installation
echo -e "${BLUE}📦 Step 1: Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}   ✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}   ✗ Python 3 not found!${NC}"
    echo "   Please install Python 3.10 or higher from https://www.python.org/"
    exit 1
fi
echo ""

# Step 2: Install dependencies
echo -e "${BLUE}📥 Step 2: Installing dependencies...${NC}"
echo "   This may take a few minutes..."

if python3 -m pip install -r requirements.txt --quiet; then
    echo -e "${GREEN}   ✓ Dependencies installed successfully${NC}"
else
    echo -e "${YELLOW}   ⚠ Some dependencies may have failed to install${NC}"
    echo "   You can manually install with: pip install -r requirements.txt"
fi
echo ""

# Step 3: Run tests
echo -e "${BLUE}🧪 Step 3: Running tests...${NC}"
if python3 test_example.py; then
    echo -e "${GREEN}   ✓ All tests passed!${NC}"
else
    echo -e "${YELLOW}   ⚠ Some tests failed, but demo will continue...${NC}"
fi
echo ""

# Step 4: Display menu
echo -e "${BLUE}🚀 Step 4: Choose how to run InstantEstimate:${NC}"
echo ""
echo "   1) Launch Web Interface (Streamlit)"
echo "   2) Run Command Line Demo (Python)"
echo "   3) Run Tests Only"
echo "   4) Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🌐 Launching Streamlit Web Interface...${NC}"
        echo ""
        echo "   The app will open in your default browser at:"
        echo "   http://localhost:8501"
        echo ""
        echo "   Press Ctrl+C to stop the server"
        echo ""
        sleep 2
        python3 -m streamlit run app.py
        ;;
    2)
        echo ""
        echo -e "${GREEN}💻 Running Command Line Demo...${NC}"
        echo ""
        python3 main.py
        ;;
    3)
        echo ""
        echo -e "${GREEN}🧪 Running Tests...${NC}"
        echo ""
        python3 test_example.py
        ;;
    4)
        echo ""
        echo -e "${BLUE}👋 Goodbye!${NC}"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        echo ""
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Demo completed!${NC}"
echo ""
