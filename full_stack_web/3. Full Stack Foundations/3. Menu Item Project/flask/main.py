from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Declares the base of sqlalchemy
Base = declarative_base()

# Table class


class Table(Base):
    """Table Class that defines the attributes of the table
            in sqlalchemy.
    """
    __tablename__ = 'tablename'

    # Column declarations here
    id = Column(Integer, primary_key=True)
    col1 = Column(String(80), nullable=False)
    col2 = Column(String(250))
    col3 = Column(String)

# Creates the engine
engine = create_engine('sqlite:///main.db')

# Binds the metadata with engine
Base.metadata.create_all(engine)
