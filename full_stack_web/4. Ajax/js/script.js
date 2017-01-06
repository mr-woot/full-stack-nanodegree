function titleCase(str) {
    str = str.toLowerCase().split(' ');
    for (var i = 0; i < str.length; i++) {
        str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
    }
    return str.join(' ');
};

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
    var address = streetStr + ', ' + cityStr;
    $greeting.text('So, you wanna live at ' + titleCase(address) + '?')
    var searchUrl = 'http://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + address + '';
    console.log(address + ' ' + searchUrl);
    $body.append('<img class="bgimg" src="' + searchUrl + '">');
    $('h5, h6').css({ 'color': '#f7f7f7' });

    // $.getJSON(nytimesurl, function(data) {
    //     var items = [];
    //     $.each
    //     console.log(data);
    // });

    var url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?sort=newest&api-key=f924134a4a044a419033fdbb835f5ea5&q=" + cityStr;
    // url += '?' + $.param({
    //     'sort': 'newest',
    //     'q': streetStr,
    //     'api-key': "f924134a4a044a419033fdbb835f5ea5"
    // });
    $.getJSON(url, function(data) {
        $nytHeaderElem.text('New York Times Articles About ' + titleCase(cityStr));
        articles = data.response.docs;
        for (var i = 0; i < articles.length; i++) {
            var article = articles[i];
            $nytElem.append('<div class="card-panel"><li class="article">' +
                '<a href="' + article.web_url + '">' + article.headline.main +
                '</a>' + '<p>' + article.snippet + '</p>' + '</li></div>');
        };
    }).error(function() {
        $nytHeaderElem.text('New York Times Articles About ' + titleCase(cityStr) + ' Couldn\'t be Loaded.');
    });
    // $.ajax({
    //     url: url,
    //     method: 'GET',
    // }).done(function(result) {
    //     console.log(result);

    // }).fail(function(err) {
    //     throw err;
    // });

    //load wiki links
    var wikiRequestTimeout = setTimeout(function() {
        $wikiHeaderElem.text("failed to load wikipedia resources");
    }, 8000);
    // var wikiLink = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + cityStr + '&format=json';
    // console.log("wikiLink: " + wikiLink);
    // $.ajax(wikiLink, {
    //     dataType: 'jsonp'
    // }).done(function(response) {
    //     console.log(response);
    //     var responseLength = response.length;
    //     var headerList = response[1];
    //     var urlList = response[3];
    //     for (i = 0; i < responseLength; i++) {
    //         //console.log(i+": "+response[i]);
    //         wikiLinkURL = urlList[i];
    //         wikiLinkHead = headerList[i];
    //         $wikiElem.append('<div class="card-panel"><li><a href="' + wikiLinkURL + '">' + '<span style="color: black !important;"><h6>' + wikiLinkHead + '</h6></span>' + '</a></li></div>');
    //     };
    //     clearTimeout(wikiRequestTimeout);
    // });

    var wikiUrl = 'http://en.widadskipedia.org/w/api.php?action=opensearch&search=' + cityStr + '&format=json&callback=wikiCallback';
    $.ajax({
        url: wikiUrl,
        dataType: 'jsonp',
        // jsonp: 'callback',
        success: function(response) {
            var articleList = response[1];
            for (var i = 0; i < articleList.length; i++) {
                articleStr = articleList[i];
                var url = 'http://en.wikipedia.org/wiki/' + articleStr;
                $wikiElem.append('<div class="card-panel"><li><a href="'+url+'">'+articleStr+'</a></li></div>');
            };
            clearTimeout(wikiRequestTimeout);
        }
    });

    return false;
};

$('#form-container').submit(loadData);
