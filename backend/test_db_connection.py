from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5433/dam"

def main():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        with engine.connect() as connection:
            print("Successfully connected to the database!")
    except OperationalError as e:
        print(f"Failed to connect: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
