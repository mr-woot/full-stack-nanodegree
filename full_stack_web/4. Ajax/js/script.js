function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview
    var streetStr = $('#street').val();
    var cityStr = $('#city').val();
    var searchUrl = "http://maps.googleapis.com/maps/api/streetview?size=600x400&location=" + streetStr + ", " + cityStr+'';
    console.log(streetStr + " " + cityStr + " " + searchUrl);
    $body.append('<img class="bgimg" src="' + searchUrl + '">').append();
    // $('#form-container').attr("autofill", "off");
: f924134a4a044a419033fdbb835f5ea5
    // YOUR CODE GOES HERE!

    return false;
};

$('#form-container').submit(loadData);
