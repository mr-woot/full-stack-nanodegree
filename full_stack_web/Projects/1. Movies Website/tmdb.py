import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Project 1!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #movieinfo .modal-dialog {
            margin-top: 50px;
            padding: 20px;
            text-align: center;
            width: 640px;
            height: auto;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #movie-info {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media div {
            border: none;
            padding: 20px;
            position: absolute;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        //// Whenever the info modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var title_data          = $(this).attr('data-title')
            var vote_average_data   = $(this).attr('data-vote')
            var release_date_data   = $(this).attr('data-date')
            var overview_data       = $(this).attr('data-overview')
            var image_url           = $(this).attr('data-image-url')
            $("#movie-info-container").empty().append($("<div>" +
                "<img src="             + image_url         + "</img>"  +
                "<h3>Title: "           + title_data        + "</h3>"   +
                "<h4>Rating: "          + vote_average_data + "</h3>"   +
                "<h4>Release Date: "    + release_date_data + "</h3>"   +
                "<p><b>Storyline:</b> " + overview_data     + "</p>"   +
                "</div>", {
              'id': 'movie-info',
              'type': 'text-html'
            }));
        });
        //// Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("slow", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Movie Info Modal -->
    <div class="modal" id="movieinfo">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="movie-info-container"></div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-default navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" style="color: #32cd32" href="#">Check this</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
        <div class="row">
          {movie_tiles}
        </div>
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-4 movie-tile text-center"
        data-image-url="{poster_path}"
        data-title="{original_title}"
        data-vote="{vote_average}"
        data-date="{release_date}"
        data-overview="{overview}"
        data-toggle="modal"
        data-target="#movieinfo">
    <img src="{poster_path}" width="220" height="342">
    <h4>{original_title}</h4>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            original_title=movie.original_title, 
            poster_path=movie.poster_path, 
            overview=movie.overview, 
            release_date=movie.release_date, 
            vote_average=movie.vote_average
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('tmdb.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
