#!/bin/bash

# Summify Installation Verification Script

echo "🔍 Summify Installation Verification"
echo "===================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "  ✅ $PYTHON_VERSION"
else
    echo "  ❌ Python 3 not found"
    exit 1
fi

# Check pip
echo ""
echo "✓ Checking pip..."
if python3 -m pip --version &> /dev/null; then
    echo "  ✅ pip installed"
else
    echo "  ❌ pip not found"
    exit 1
fi

# Check required files
echo ""
echo "✓ Checking project files..."
required_files=(
    "requirements.txt"
    "backend/main.py"
    "backend/ai_tools.py"
    "backend/database.py"
    "frontend/index.html"
    "frontend/app.js"
    "frontend/style.css"
    "README.md"
    "QUICKSTART.md"
    "DEVELOPMENT.md"
    "DEPLOYMENT.md"
)

missing_files=0
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING)"
        ((missing_files++))
    fi
done

if [ $missing_files -gt 0 ]; then
    echo ""
    echo "❌ Missing $missing_files files"
    exit 1
fi

# Check OPENAI_API_KEY
echo ""
echo "✓ Checking OpenAI API Key..."
if [ -z "$OPENAI_API_KEY" ]; then
    if [ -f ".env" ]; then
        echo "  ⚠️  API key not in environment, but .env file found"
    else
        echo "  ⚠️  OPENAI_API_KEY not set"
        echo "     Set it with: export OPENAI_API_KEY='sk-...'"
    fi
else
    echo "  ✅ API key found"
fi

# Check dependencies (if installed)
echo ""
echo "✓ Checking Python packages..."
packages=("fastapi" "uvicorn" "pdfplumber" "openai")
for package in "${packages[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        VERSION=$(python3 -c "import $package; print($package.__version__ if hasattr($package, '__version__') else 'installed')" 2>/dev/null)
        echo "  ✅ $package ($VERSION)"
    else
        echo "  ❌ $package not installed"
    fi
done

# Summary
echo ""
echo "===================================="
echo "✅ Installation Verification Complete!"
echo ""
echo "📖 Next Steps:"
echo "1. Set OPENAI_API_KEY: export OPENAI_API_KEY='your-key-here'"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Start server: bash start.sh"
echo "4. Open: http://localhost:8000"
echo ""
echo "📚 Documentation:"
echo "- QUICKSTART.md    - Get started in 30 seconds"
echo "- README.md        - Full feature documentation"
echo "- DEVELOPMENT.md   - Architecture and development"
echo "- DEPLOYMENT.md    - Production deployment guide"
echo ""
