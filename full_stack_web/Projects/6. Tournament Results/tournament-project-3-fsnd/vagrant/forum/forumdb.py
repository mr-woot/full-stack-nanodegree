#
# Database access functions for the web forum.
#

import time
import psycopg2

# Database connection


def ConnectDB():
    try:
        DB = psycopg2.connect("dbname=forum")
    except:
        print "Connectivity Problem."
    return DB

# Get posts from database.


def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    DB = ConnectDB()
    c = DB.cursor()
    c.execute("SELECT time, content FROM posts ORDER BY time DESC")
    posts = [{'content': str(row[1]), 'time': str(row[0])}
             for row in c.fetchall()]
    DB.close()
    return posts

# Add a post to the database.


def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = ConnectDB()
    c = DB.cursor()
    c.execute("INSERT INTO posts (content) VALUES (%s);", (content,))
    c.execute("UPDATE posts SET content='cheese' WHERE content LIKE '%spam%';")
    c.execute("DELETE FROM posts WHERE content='cheese';")
    DB.commit()
    DB.close()
