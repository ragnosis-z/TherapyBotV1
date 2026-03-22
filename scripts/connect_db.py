import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

def main():
    # Load .env file from the parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(current_dir), '.env')
    load_dotenv(dotenv_path=env_path)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not found in environment variables.")
        sys.exit(1)
    
    if "<YOUR_DB_PASSWORD>" in db_url:
        print("Warning: Password placeholder found in DATABASE_URL. Please update it in the .env file with your actual Supabase DB password.")
        sys.exit(1)

    print(f"Attempting to connect to the database...")

    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            print("Successfully connected to the database!")
            
            # Initialize one basic table
            metadata = MetaData()
            test_table = Table(
                'init_test_table', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(50))
            )
            
            metadata.create_all(engine)
            print("Successfully created 'init_test_table'. Database is initialized and ready.")
            
    except Exception as e:
        print(f"Failed to connect to the database or create table:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
