# Quick Start Guide

## 🎯 Get Running in 5 Minutes

### Option 1: Local Development (Recommended for Development)

#### Windows
```bash
# Run the setup script
setup.bat

# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

# Start the app
uvicorn app.main:app --reload
```

#### macOS/Linux
```bash
# Run the setup script
bash setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Start the app
uvicorn app.main:app --reload
```

### Option 2: Docker (Recommended for Consistency)

```bash
# Build and start
docker-compose up

# View logs
docker-compose logs -f app

# Stop
docker-compose down
```

## 📍 Access Points

Once running, you can access:

- **API Docs (Interactive)**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **App Info**: http://localhost:8000/api/info

## 🔑 Configuration

### Essential Setup
1. Copy `.env.example` to `.env`
2. (Optional) Add your OpenAI API key to `.env`
3. Update any other settings as needed

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
DEBUG=True  # For development
ENVIRONMENT=development
```

Without an OpenAI key, the app will use template responses.

## 🧪 Test the API

### Using curl

```bash
# Create a session
curl -X POST http://localhost:8000/api/chat/session/create

# Send a message
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am feeling anxious today",
    "mode": "companion"
  }'

# Get available modes
curl http://localhost:8000/api/chat/modes
```

### Using the Interactive Docs
1. Go to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

## 📚 Database

### Check Database (SQLite - Development)
```bash
# View SQLite database
sqlite3 chatbot.db

# Example queries in sqlite3 shell:
.tables
SELECT * FROM users;
SELECT * FROM chat_sessions;
SELECT * FROM messages;
```

### Switch to PostgreSQL (Production)
Update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db
```

## 🐛 Troubleshooting

### Issue: Module not found errors
```bash
# Ensure you're in the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: OpenAI API errors
- Verify your API key is correct in `.env`
- Check API key has sufficient credits
- Check rate limits

### Issue: Database locked (SQLite)
```bash
# Delete and recreate
rm chatbot.db
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Issue: Port 8000 already in use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

## 📖 Next Steps

1. **Explore the API**: Open http://localhost:8000/docs
2. **Read the Documentation**: Check [README.md](README.md) and [PROJECT_PLAN.md](PROJECT_PLAN.md)
3. **Try different modes**: Send messages with different `mode` values
4. **Test crisis detection**: Try messages with keywords like "want to die"
5. **Check the database**: Use SQLite shell to inspect data

## 🚀 Development Workflow

### Making Changes

1. Make code changes (hot-reload is enabled)
2. The API will automatically reload
3. Test using the docs at `/docs`
4. Check database with SQLite explorer

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_chat.py -v

# With coverage
pytest --cov=app
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking (if configured)
mypy app/
```

## 📝 Common Tasks

### Add a new endpoint
1. Create handler in `app/routes/file.py`
2. Import and include router in `app/main.py`
3. Add tests in `tests/test_file.py`

### Add a new database model
1. Create model class in `app/models/file.py`
2. Import in `app/models/__init__.py`
3. Create migration if needed
4. Update schemas in `app/schemas/file.py`

### Add a new dependency
1. Add to `requirements.txt`
2. Install: `pip install -r requirements.txt`
3. Use in code

## 🔗 Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM Guide](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Pydantic Validation](https://docs.pydantic.dev/latest/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## ❓ Need Help?

1. Check existing issues in the project
2. Review error logs in the terminal
3. Check `.env` configuration
4. Verify all dependencies are installed
5. Try the troubleshooting section above
