from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Song, User

engine = create_engine('sqlite:///tempmusic.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# create a dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="Robo HARI", email="tinnadasdHIHDAyTim@udacity.com",
             picture='https://pbs.twimgdaSD.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

User3 = User(name="Robo 324", email="s234fsdf@udacity.com",
             picture='https://pbs.twimdgdaSD.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User3)
session.commit()

# Looping genre music dump
loopingGenre = Genre(name = "looping", user_id = 1)

session.add(loopingGenre)
session.commit()

song1 = Song(name = "Retcon",
			band_name = "Mylets",
			country = "US",
			youtube_url = "https://www.youtube.com/watch?v=GJ9OQLovpr4",
			genre = loopingGenre,
            user_id = 1)
session.add(song1)
session.commit()

song2 = Song(name = "Indian Winter",
			band_name = "El Ten Eleven",
			country = "US",
			youtube_url = "https://www.youtube.com/watch?v=mTkPfjSXFpo",
			genre = loopingGenre,
            user_id = 1)
session.add(song2)
session.commit()

song3 = Song(name = "Emulsifaction",
			band_name = "Reggie Watts",
			country = "US",
			youtube_url = "https://www.youtube.com/watch?v=HXhZAigtFTE",
			genre = loopingGenre,
            user_id = 1)
session.add(song3)
session.commit()

song4 = Song(name = "Toe Tore Oh",
			band_name = "Dustin Wong",
			country = "Japan",
			youtube_url = "https://www.youtube.com/watch?v=j1PuWrE9nKY",
			genre = loopingGenre,
            user_id = 1)
session.add(song4)
session.commit()


# Video games genre music dump
videoGameGenre = Genre(name = "video game", user_id = 1)

song1 = Song(name = "Manlorette Party",
			band_name = "Staypuft",
			country = "US",
			youtube_url = "https://www.youtube.com/watch?v=254sCXAaZNE",
			genre = videoGameGenre)
session.add(song1)
session.commit()

song2 = Song(name = "Adventure",
			band_name = "Disasterpeace",
			country = "US",
			youtube_url = "https://www.youtube.com/watch?v=76GnOwHorn0",
			genre = videoGameGenre)
session.add(song2)
session.commit()

song3 = Song(name = "Lone Star",
			band_name = "Jim Guthrie",
			country = "Canada",
			youtube_url = "https://www.youtube.com/watch?v=wOOqdRsbHKA",
			genre = videoGameGenre)
session.add(song3)
session.commit()

song4 = Song(name = "Minecraft",
			band_name = "C418",
			country = "Germany",
			youtube_url = "https://www.youtube.com/watch?v=qq-RGFyaq0U",
			genre = videoGameGenre)
session.add(song4)
session.commit()

# Mathematical genre music dump
mathematicalGenre = Genre(name = "mathematical", user_id = 1)

song1 = Song(name = "Abraxical Solapse",
			band_name = "Physics House Band",
			country = "UK",
			youtube_url = "https://www.youtube.com/watch?v=rdxZ4eoLMn4",
			genre = mathematicalGenre)
session.add(song1)
session.commit()

song2 = Song(name = "Bond",
			band_name = "LITE",
			country = "Japan",
			youtube_url = "https://www.youtube.com/watch?v=BlWiRjIcjOk",
			genre = mathematicalGenre)
session.add(song2)
session.commit()

song3 = Song(name = "40 Rods to the Hog's Head",
			band_name = "Tera Melos",
			country = "US",
			youtube_url = "https://www.youtube.com/watch?v=-FypjUkPfYE",
			genre = mathematicalGenre,
            user_id = 1)
session.add(song3)
session.commit()

song4 = Song(name = "Little Bubble, Where You Going?",
			band_name = "Piglet",
			country = "US",
			youtube_url = "https://www.youtube.com/watch?v=OllEOofj4O8",
			genre = mathematicalGenre,
            user_id = 1)
session.add(song4)
session.commit()
