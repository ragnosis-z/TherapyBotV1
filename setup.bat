@echo off
REM Quick start script for local development (Windows)

echo 🚀 Starting Therapeutic AI Chatbot Setup...

REM Check Python version
python --version
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.11+
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Copy environment template
if not exist ".env" (
    echo ⚙️ Creating .env from template...
    copy .env.example .env
    echo 📝 Please edit .env with your configuration (especially OPENAI_API_KEY)
)

REM Create database tables
echo 🗄️ Initializing database...
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

REM Run tests
echo 🧪 Running tests...
pytest tests/ -v

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your OpenAI API key (optional)
echo 2. Run: uvicorn app.main:app --reload
echo 3. Visit: http://localhost:8000/docs
echo.
