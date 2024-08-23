from sqlalchemy import create_engine, Column, Integer, String, MetaData
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
        
        self.engine = create_engine(DATABASE_URI, echo=True)
        Base.metadata.create_all(self.engine)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self):
        """Get the current database session."""
        if not self.session:
            self.initialize_database()
        return self.session
    
    def add_record(self, record):
        """Add a new record to the database."""
        session = self.get_session()
        session.add(record)
        session.commit()
        
    def get_records(self):
        """Get all records from the database."""
        session = self.get_session()
        return session.query(ExampleTable).all()
    
    def close_connection(self):
        """Close the current database connection."""
        if self.session:
            self.session.close()
            
# Example usage
if __name__ == "__main__":
    db_handler = DatabaseHandler()
    db_handler.initialize_database()
    
    # Add a new record
    new_record = ExampleTable(name="ExampleName")
    db_handler.add_record(new_record)
    
    # Fetch all records
    records = db_handler.get_records()
    for record in records:
        print(f"ID: {record.id}, Name: {record.name}")
    
    # Close the database connection
    db_handler.close_connection()