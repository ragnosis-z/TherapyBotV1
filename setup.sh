#!/bin/bash
# Quick start script for local development

echo "🚀 Starting Therapeutic AI Chatbot Setup..."

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate  # Use venv\Scripts\activate.bat on Windows

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment template
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from template..."
    cp .env.example .env
    echo "📝 Please edit .env with your configuration (especially OPENAI_API_KEY)"
fi

# Create database tables
echo "🗄️  Initializing database..."
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key (optional)"
echo "2. Run: uvicorn app.main:app --reload"
echo "3. Visit: http://localhost:8000/docs"
echo ""
