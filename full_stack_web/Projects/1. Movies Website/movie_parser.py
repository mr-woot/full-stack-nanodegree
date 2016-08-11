import json, urllib
import movie_model
import tmdb

# API used is The Movie Db

# API Key Credential
api_key = "2d270c9059a83eb54959e027b57a696a"

# API end-point for getting json data
url = "http://api.themoviedb.org/3/movie/popular?api_key=" + api_key

# list that will contain the data in unicode format
movies = []

# getting data upto 5 pages of the end-point
for i in range(1, 6):
    # api-page link
    link = url + "&page=" + str(i)
    
    # getting response data from link-url
    response = urllib.urlopen(link)

    # converting into readable format
    content = json.loads(response.read())

    # parsing json data and appending to the list
    for item in content['results']:
        movies.append(movie_model.MovieModel(item[u'id'], 
                               item[u'poster_path'], 
                               item[u'overview'].encode('utf8'), 
                               item[u'release_date'], 
                               item[u'original_title'], 
                               item[u'vote_average']))

# run app
tmdb.open_movies_page(movies)