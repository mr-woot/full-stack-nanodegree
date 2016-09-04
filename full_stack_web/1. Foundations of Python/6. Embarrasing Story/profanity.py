import urllib

def read():
    qfile = open("movie_quotes.txt")
    content = qfile.read()
    
    print content
    qfile.close()
    check_prof(content)

def check_prof(check_text):
    connection = urllib.urlopen("http://www.wdylike.appspot.com/?q=" + check_text)
    output = connection.read()
    connection.close()
    if "true" in output:
        print "Profanity found."
    else:
        print "Fine text."
read()
