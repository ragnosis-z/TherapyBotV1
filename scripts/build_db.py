import os
import sys

# Make the app package importable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from dotenv import load_dotenv

def main():
    print("Loading environment variables...")
    load_dotenv(os.path.join(parent_dir, '.env'))
    
    # Import engine and Base from database module, and models to register them
    print("Initializing database engine and models...")
    try:
        from app.database import engine, Base
        import app.models  
    except ImportError as e:
        print(f"Failed to import app modules: {e}")
        sys.exit(1)
        
    print("Building database tables...")
    try:
        # create_all will only create tables that do not exist yet
        # If we need to drop and recreate, we'd use Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("Successfully built all database tables!")
        
        # Verify created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Verified tables in database: {', '.join(tables)}")
        
    except Exception as e:
        print(f"Error during database build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
