from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
from flask import url_for
from flask import flash
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base
from database_setup import Genre
from database_setup import Song
from database_setup import User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///tempmusic.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def login():
    # create a state token to prevent request forgery
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32))
    # store it in session for later use
    login_session['state'] = state
    return render_template('login.html', STATE = state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # A Bug in google logout code, instead of assigning like this:
    # access_token = credentials.access_token
    # it should be like below
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# Disconnect based on provider
@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showGenres'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showGenres'))


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view music dump
@app.route('/genre/<int:genre_id>/JSON')
def genreSongsJSON(genre_id):
    genre = session.query(Genre).filter_by(id = genre_id).one()
    songs = session.query(Song).filter_by(genre_id = genre_id).all()
    return jsonify(songs = [i.serialize for i in songs])

@app.route('/genre/<int:genre_id>/<int:song_id>/JSON')
def songJSON(genre_id, song_id):
    song = session.query(Song).filter_by(id = song_id).one()
    return jsonify(song = song.serialize)

@app.route('/genre/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres = [i.serialize for i in genres])

# Show all genres
@app.route('/')
def showGenres():
    songs = session.query(Song).order_by(asc(Song.name))
    genres = session.query(Genre).order_by(asc(Genre.name))
    if 'username' not in login_session:
        return render_template('publicsongs.html', songs = songs, genres = genres)
    else:
        return render_template('songs.html', songs = songs, genres = genres, username=login_session.get('username'))

# Create a new music genre
@app.route('/genre/new', methods=['GET','POST'])
def newGenre():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newGenre = Genre(name = request.form['name'],
                         user_id=login_session['user_id'])
        session.add(newGenre)
        flash('Succesfully added %s genre' % newGenre.name)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('new-genre.html')

# Edit a genre
@app.route('/genre/<int:genre_id>/edit/', methods = ['GET', 'POST'])
def editGenre(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedGenre = session.query(Genre).filter_by(id = genre_id).one()
    if editedGenre.user_id != login_session['user_id']:
        return """<script>(function() {alert("not authorized");})();</script>"""
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
            flash('Genre successfully edited %s' % editedGenre.name)
            return redirect(url_for('showGenres'))
    else:
        return render_template('edit-genre.html', genre = editedGenre)

# Delete a genre
@app.route('/genre/<int:genre_id>/delete/', methods = ['GET', 'POST'])
def deleteGenre(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    genreToDelete = session.query(Genre).filter_by(id = genre_id).one()
    if genreToDelete.user_id != login_session['user_id']:
        return """<script>(function() {alert("not authorized");})();</script>"""
    if request.method == 'POST':
        session.delete(genreToDelete)
        flash('%s successfully deleted' % genreToDelete.name)
        session.commit()
        return redirect(url_for('showGenres', genre_id = genre_id))
    else:
        return render_template('delete-genre.html', genre = genreToDelete)

# Show songs from a genre
@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/songs/')
def showSongs(genre_id):
    genre = session.query(Genre).filter_by(id = genre_id).one()
    genres = session.query(Genre).order_by(asc(Genre.name))
    creator = getUserInfo(genre.user_id)
    songs = session.query(Song).filter_by(genre_id = genre_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicsongs.html', songs = songs,
            genre = genre, genres = genres, creator = creator)
    else:
        return render_template('songs.html', songs = songs,
             genre = genre, genres = genres, creator = creator)

# Create a new song for a genre
@app.route('/genre/<int:genre_id>/songs/new/', methods = ['GET', 'POST'])
def newSong(genre_id):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id = genre_id).one()
    if request.method == 'POST':
        newSong = Song(name = request.form['name'],
                       genre_id = genre_id,
                       band_name = request.form['band_name'],
                       country = request.form['country'],
                       youtube_url = request.form['youtube_url'],
                       user_id = login_session['user_id'])
        session.add(newSong)
        session.commit()
        flash('New song %s successfully created' % (newSong.name))
        return redirect(url_for('showSongs', genre_id = genre_id))
    else:
        return render_template('new-song.html', genre_id = genre_id)

# Edit a song
@app.route('/genre/<int:genre_id>/song/<int:song_id>/edit', methods = ['GET', 'POST'])
def editSong(genre_id, song_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedSong = session.query(Song).filter_by(id = song_id).one()
    genre = session.query(Genre).filter_by(id = genre_id).one()
    if editedSong.user_id != login_session['user_id']:
        return """<script>(function() {alert("not authorized");})();</script>"""
    if request.method == 'POST':
        if request.form['name']:
            editedSong.name = request.form['name']
        if request.form['band_name']:
            editedSong.band_name = request.form['band_name']
        if request.form['country']:
            editedSong.country = request.form['country']
        if request.form['youtube_url']:
            editedSong.youtube_url = request.form['youtube_url']
        session.add(editedSong)
        session.commit()
        flash('Song successfully edited')
        return redirect(url_for('showSongs', genre_id = genre_id))
    else:
        return render_template('edit-song.html', genre_id = genre_id, song_id = song_id, item = editedSong)

# Delete a song
@app.route('/genre/<int:genre_id>/songs/<int:song_id>/delete', methods = ['GET', 'POST'])
def deleteSong(genre_id, song_id):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(id = genre_id).one()
    songToDelete = session.query(Song).filter_by(id = song_id).one()
    if songToDelete.user_id != login_session['user_id']:
        return """<script>(function() {alert("not authorized");})();</script>"""
    if request.method == 'POST':
        session.delete(songToDelete)
        session.commit()
        flash('Song successfully deleted')
        return redirect(url_for('showSong', genre_id = genre_id))
    else:
        return render_template('delete-song.html', item = songToDelete)


if __name__ == '__main__':
    app.secret_key = "secret key"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
