# Documentation for Project-1

## API
The public API used in the project was [TheMovieDb API](http://docs.themoviedb.apiary.io/)

## Modules Description
1. `movie_model.py`: Class model that is used as a **Data Object**, consisting of _```movie_title, release_date, poster_url, overview, average_vote```_.
2. `movie_parser.py`: Parses **JSON Data** into _readable format_. Web App starts here.
3. `tmdb.py`: Generates **HTML** content.

## How to Run on Windows?
###GUI
1. Open **IDLE-Python** from Windows.
2. Locate `movie_parser.py` file.
3. Select `Run as module` in `Run` tab. Or you can also press `F5`.

###Command Line
1. `cd [movie_parser.py directory]`
2. `python movie_parser.py` 

License [MIT](LICENSE.md)
