from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Base, Song, User

engine = create_engine('sqlite:///songdirwithusers.db')
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


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Songs for EDM genre
genre1 = Genre(user_id=1, name="EDM")

session.add(genre1)
session.commit()


song1 = Song(user_id=1, name="Closer", author="Chainsmokers ft. Halsey", youtube_url="https://www.youtube.com/watch?v=0zGcUoRlhmw&list=PLMC9KNkIncKtpLj36iKalePx05KmqaHXF", genre=genre1)

session.add(song1)
session.commit()

song2 = Song(user_id=1, name="Let Me Love You", author="Justin Bieber", youtube_url="https://www.youtube.com/watch?v=SMs0GnYze34&list=PLMC9KNkIncKtpLj36iKalePx05KmqaHXF&index=2", genre=genre1)
session.add(song2)
session.commit()

song3 = Song(user_id=1, name="My Way", author="Calvin Harris", youtube_url="https://www.youtube.com/watch?v=b4Bj7Zb-YD4&list=PLMC9KNkIncKtpLj36iKalePx05KmqaHXF&index=3", genre=genre1)
session.add(song3)
session.commit()

song4 = Song(user_id=1, name="Cold Water", author="Major Lazer ft. Justin Bieber", youtube_url="https://www.youtube.com/watch?v=nBtDsQ4fhXY&index=4&list=PLMC9KNkIncKtpLj36iKalePx05KmqaHXF", genre=genre1)
session.add(song4)
session.commit()

song5 = Song(user_id=1, name="Don't Let Me Down", author="Chainsmokers ft. Daya", youtube_url="https://www.youtube.com/watch?v=Io0fBr1XBUA&list=PLMC9KNkIncKtpLj36iKalePx05KmqaHXF&index=5", genre=genre1)
session.add(song5)
session.commit()


song6 = Song(user_id=1, name="Why", author="Andra", youtube_url="https://www.youtube.com/watch?v=rhcc1KQlCS4&list=PLMC9KNkIncKtpLj36iKalePx05KmqaHXF&index=6", genre=genre1)
session.add(song6)
session.commit()

# Songs for Bollywood genre
genre2 = Genre(user_id=1, name="Bollywood")
session.add(genre2)
session.commit()

song1 = Song(user_id=1, name="Kala Chashmah", author="Badshah ft. Neha Kakkar", youtube_url="https://www.youtube.com/watch?v=k4yXQkG2s1E&list=PLMRKdK25AuPVbQndF8hhyfyrUzgs5JbwR&index=1", genre=genre2)
session.add(song1)
session.commit()

song2 = Song(user_id=1, name="Kar Gayi Chull", author="Badshah ft. Neha Kakkar", youtube_url="https://www.youtube.com/watch?v=NTHz9ephYTw&list=PLMRKdK25AuPVbQndF8hhyfyrUzgs5JbwR&index=2", genre=genre2)
session.add(song2)
session.commit()

song3 = Song(user_id=1, name="Bulleya", author="Amit Mishra", youtube_url="https://www.youtube.com/watch?v=hXh35CtnSyU&list=PLMRKdK25AuPVbQndF8hhyfyrUzgs5JbwR&index=3", genre=genre2)
session.add(song3)
session.commit()

song4 = Song(user_id=1, name="Baby Ko Base Pasand Hai", author="Vishal, Badshah, Shalmali", youtube_url="https://www.youtube.com/watch?v=aWMTj-rejvc&list=PLMRKdK25AuPVbQndF8hhyfyrUzgs5JbwR&index=4", genre=genre2)
session.add(song4)
session.commit()

song5 = Song(user_id=1, name="Ae Dil Hai Mushkil", author="Arjit", youtube_url="https://www.youtube.com/watch?v=vUCM_0evdQY&list=PLMRKdK25AuPVbQndF8hhyfyrUzgs5JbwR&index=5", genre=genre2)
session.add(song5)
session.commit()


# Songs for Indie genre
genre3 = Genre(user_id=1, name="")
session.add(genre3)
session.commit()

song1 = Song(user_id=1, name="Bloom", author="The Paper Kites", youtube_url="https://www.youtube.com/watch?v=8inJtTG_DuU&index=2&list=PLTe4Aumnr7KCZMhGPOmdOM1Wz1Mqy5FdT", genre=genre3)
session.add(song1)
session.commit()

song2 = Song(user_id=1, name="American Love", author="Wild", youtube_url="https://www.youtube.com/watch?v=XShnI61LXCQ&list=PLTe4Aumnr7KCZMhGPOmdOM1Wz1Mqy5FdT&index=4", genre=genre3)
session.add(song2)
session.commit()

song3 = Song(user_id=1, name="Renegades", author="X Ambassadors", youtube_url="https://www.youtube.com/watch?v=8j741TUIET0&index=5&list=PLTe4Aumnr7KCZMhGPOmdOM1Wz1Mqy5FdT", genre=genre3)
session.add(song3)
session.commit()

song4 = Song(user_id=1, name="Georgia", author="Vance Joy", youtube_url="https://www.youtube.com/watch?v=DQMbHNofCzw&index=6&list=PLTe4Aumnr7KCZMhGPOmdOM1Wz1Mqy5FdT", genre=genre3)
session.add(song4)
session.commit()

song5 = Song(user_id=1, name="I Will Wait", author="Mumford and Sons", youtube_url="https://www.youtube.com/watch?v=rGKfrgqWcv0&index=8&list=PLTe4Aumnr7KCZMhGPOmdOM1Wz1Mqy5FdT", genre=genre3)
session.add(song5)
session.commit()


# Songs for Rock genre
genre4 = Genre(user_id=1, name="Rock")
session.add(genre4)
session.commit()

song1 = Song(user_id=1, name="Moth Into Flame", author="Metallica", youtube_url="https://www.youtube.com/watch?v=4tdKl-gTpZg&list=PLRZlMhcYkA2HybvsMzUcsqoxqlCEHXnpC&index=1", genre=genre4)
session.add(song1)
session.commit()

song2 = Song(user_id=1, name="Heathens (Suicide Squad)", author="Twenty One Pilots", youtube_url="https://www.youtube.com/watch?v=UprcpdwuwCg&index=2&list=PLRZlMhcYkA2HybvsMzUcsqoxqlCEHXnpC", genre=genre4)
session.add(song2)
session.commit()

song3 = Song(user_id=1, name="The Stage", author="Avenged Sevenfold", youtube_url="https://www.youtube.com/watch?v=fBYVlFXsEME&list=PLRZlMhcYkA2HybvsMzUcsqoxqlCEHXnpC&index=3", genre=genre4)
session.add(song3)
session.commit()

song4 = Song(user_id=1, name="Ride", author="Twenty One Pilots", youtube_url="https://www.youtube.com/watch?v=Pw-0pbY9JeU&list=PLRZlMhcYkA2HybvsMzUcsqoxqlCEHXnpC&index=4", genre=genre4)
session.add(song4)
session.commit()

song5 = Song(user_id=1, name="Unsteady", author="X Ambassadors", youtube_url="https://www.youtube.com/watch?v=V0lw3qylVfY&index=6&list=PLRZlMhcYkA2HybvsMzUcsqoxqlCEHXnpC", genre=genre4)
session.add(song5)
session.commit()


# Songs for Hip Hop genre
genre5 = Genre(user_id=1, name="Hip Hop")
session.add(genre5)
session.commit()

song1 = Song(user_id=1, name="Buy Back the Block", author="Rick Ross ft. 2 Chainz, Gucci Mane", youtube_url="https://www.youtube.com/watch?v=BUu8u7fX8Pc&index=5&list=PLz8JsiLUtVnD2t0qlJYDhXtyiCWTv37DA", genre=genre5)
session.add(song1)
session.commit()

song2 = Song(user_id=1, name="All Night", author="Beyonce", youtube_url="https://www.youtube.com/watch?v=gM89Q5Eng_M&index=7&list=PLz8JsiLUtVnD2t0qlJYDhXtyiCWTv37DA", genre=genre5)
session.add(song2)
session.commit()

song3 = Song(user_id=1, name="Shake It Fast", author="Rae Sremmurd ft. Juicy J", youtube_url="https://www.youtube.com/watch?v=7pqTa1lQjtY&index=8&list=PLz8JsiLUtVnD2t0qlJYDhXtyiCWTv37DA", genre=genre5)
session.add(song3)
session.commit()

song4 = Song(user_id=1, name="Know My Name", author="DJ Mustard ft. Rich The Kid, RJ", youtube_url="https://www.youtube.com/watch?v=9LjkAjWOZOY&index=9&list=PLz8JsiLUtVnD2t0qlJYDhXtyiCWTv37DA", genre=genre5)
session.add(song4)
session.commit()

song5 = Song(user_id=1, name="Lil Baby", author="2 Chainz ft. Ty Dolla $ign", youtube_url="https://www.youtube.com/watch?v=2q4uFnokRrU&index=11&list=PLz8JsiLUtVnD2t0qlJYDhXtyiCWTv37DA", genre=genre5)
session.add(song5)
session.commit()


# Songs for Pop genre
genre6 = Genre(user_id=1, name="Pop")
session.add(genre6)
session.commit()

song1 = Song(user_id=1, name="Bad Things", author="Machine Gun Kelly, Camila Cabello", youtube_url="https://www.youtube.com/watch?v=QpbQ4I3Eidg&index=6&list=PL9NY5axt700FjL6HlEhqlMFT1gjMGVBgy", genre=genre6)
session.add(song1)
session.commit()

song2 = Song(user_id=1, name="24K Magic", author="Bruno Mars", youtube_url="https://www.youtube.com/watch?v=UqyT8IEBkvY&list=PL9NY5axt700FjL6HlEhqlMFT1gjMGVBgy&index=8", genre=genre6)
session.add(song2)
session.commit()

song3 = Song(user_id=1, name="Slumber Party", author="Britney Spears ft. Tinashe", youtube_url="https://www.youtube.com/watch?v=2RRY3OVqtwc&list=PL9NY5axt700FjL6HlEhqlMFT1gjMGVBgy&index=12", genre=genre6)
session.add(song3)
session.commit()

song4 = Song(user_id=1, name="We Don't Talk Anymore", author="Charlie Puth", youtube_url="https://www.youtube.com/watch?v=3AtDnEC4zak&index=13&list=PL9NY5axt700FjL6HlEhqlMFT1gjMGVBgy", genre=genre6)
session.add(song4)
session.commit()

song5 = Song(user_id=1, name="Trust Nobody", author="Cashmere Cat ft. Selena Gomez, Tory Lanez", youtube_url="https://www.youtube.com/watch?v=1Vn1BXfsd4Q&list=PL9NY5axt700FjL6HlEhqlMFT1gjMGVBgy&index=14", genre=genre6)
session.add(song5)
session.commit()



print "added song to genres!"