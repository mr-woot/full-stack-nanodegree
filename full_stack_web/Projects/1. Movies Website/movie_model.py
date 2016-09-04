# Base image url for the TMDB API
base_image_url = "http://image.tmdb.org/t/p/w185/"

# Movie Model
class MovieModel():
    def __init__(self, 
                 movie_id,
                 poster_path,
                 overview,
                 release_date,
                 original_title, 
                 vote_average):
        self.movie_id = movie_id
        self.poster_path = base_image_url + poster_path
        self.overview = overview
        self.release_date = release_date
        self.original_title = original_title
        self.vote_average = vote_average
