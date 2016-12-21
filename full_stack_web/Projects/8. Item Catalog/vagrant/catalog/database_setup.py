from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))

class Genre(Base):
	__tablename__ = 'genre'

	id = Column(Integer, primary_key=True)
	name = Column(String(80), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
	   """return object data in easily serializeable format"""
	   return {
	   		'name'		:	self.name,
	   		'id'		:	self.id
	   }

class Song(Base):
    __tablename__ = 'band'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    band_name = Column(String(80))
    country = Column(String(80))
    youtube_url = Column(String(250))
    genre_id = Column(Integer,ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'         : self.id,
           'band_name'	: self.band_name,
           'country'	: self.country,
           'youtube_url'	: self.youtube_url
       }

engine = create_engine('sqlite:///tempmusic.db')

Base.metadata.create_all(engine)
