from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Base declarative class for SQLAlchemy
Base = declarative_base()

# Define an example table as a model
class ExampleTable(Base):
    __tablename__ = 'example_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Database Handler Module
class DatabaseHandler:
    def __init__(self):
        self.engine = None
        self.session = None
    
    def initialize_database(self):
        """Initialize database connection and create tables."""
        DATABASE_URI = os.getenv("DATABASE_URI")
        if not DATABASE_URI:
            raise Exception("DATABASE_URI environment variable not found.")
        
        try:
            self.engine = create_engine(DATABASE_URI, echo=True)
            Base.metadata.create_all(self.engine)
            self.session = scoped_session(sessionmaker(bind=self.engine))
        except SQLAlchemyError as e:
            print(f"An error occurred while initializing the database: {e}")
            raise
    
    def get_session(self):
        """Get the current database session."""
        if not self.session:
            try:
                self.initialize_database()
            except Exception as e:
                print(f"Failed to initialize database: {e}")
                raise
        return self.session
    
    def add_record(self, record):
        """Add a new record to the database."""
        try:
            session = self.get_session()
            session.add(record)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred while adding the record: {e}")
            raise
    
    def get_records(self):
        """Get all records from the database."""
        try:
            session = self.get_session()
            return session.query(ExampleTable).all()
        except SQLAlchemyError as e:
            print(f"An error occurred while fetching records: {e}")
            raise
    
    def close_connection(self):
        """Close the current database connection."""
        if self.session:
            self.session.close()
            
# Example usage
if __name__ == "__main__":
    db_handler = DatabaseHandler()
    try:
        db_handler.initialize_database()
        
        # Add a new record
        new_record = ExampleTable(name="ExampleName")
        db_handler.add_record(new_record)
        
        # Fetch all records
        records = db_handler.get_records()
        for record in records:
            print(f"ID: {record.id}, Name: {record.name}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        db_handler.close_connection()