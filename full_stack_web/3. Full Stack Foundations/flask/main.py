from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Declares the base of sqlalchemy
Base = declarative_base()

# Table class


class Shelter(Base):
    """Table Class that defines the attributes of the table
            in sqlalchemy.
    """
    __tablename__ = 'shelter'

    # Column declarations here
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)


class Puppy(Base):
    """Table Class that defines the attributes of the table
            in sqlalchemy.
    """
    __tablename__ = 'puppy'

    # Column declarations here
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))

# Creates the engine
engine = create_engine('sqlite:///main.db')

# Binds the metadata with engine
Base.metadata.create_all(engine)
