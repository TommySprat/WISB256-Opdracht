from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import os, re, random

# Geinspireerd door
# http://www.netinstructions.com/2011/09/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/

def main():
    startUrl = "http://lyrics.wikia.com/Category:Language/English"
    global genres
    genres = ('Metal', 'Rock', 'Pop', 'Rap', 'Hip Hop')

    # Create directories to store results
    for g in genres:
        if os.path.exists(g):
            # Empty the directory before we can remove it
            for root, dirs, files in os.walk(g, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            # Now the directory is empty; remove it
            os.rmdir(g)
        # Make the directory
        os.mkdir(g)

    spider(startUrl, 6, 2000000000)

class LyricExtractor():
    def __init__(self):
        self.artistPattern = re.compile(r'This song is performed by <b><a href=.* title=\"(.*)\">.*and appears on the album <i><a href=\"(.*?)\" title=\".*\">(.*)<\/a>', re.IGNORECASE)
        self.genrePattern = re.compile( r'Genre:.*<a href=\".*\" title=\".*\">(.*)<\/a><\/td>', re.IGNORECASE)
        self.h = HTMLParser()
        self.lyricsPattern = re.compile(r"<\/a><span class='adNotice'>Ad<\/span><\/div>(.*)<!--", re.IGNORECASE)

    def ExtractLyrics(self, url, genreCount):
        # Remember the base URL which will be important when creating
        # absolute URLs
        baseUrl = url

        # Retrieve the page and make it into a string
        try:
            response = urlopen(url, None, 2)
        except:
            print("An error occured while opening an URL, skipping to the next one")
            return 0, genreCount

        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        result = self.artistPattern.findall(htmlString)

        # discard song if the page does not have enough information
        if result == []:
            print("Discarding song: can't read genre")
            return 0, genreCount

        artistName = result[0][0]
        albumUrl = parse.urljoin(baseUrl, result[0][1])
        albumName = result[0][2]

        genre = self.getGenre(albumUrl)

        # discard song if the genre is missing
        if genre == "":
            print("Discarding song: can't read genre")
            return 0, genreCount

        # We place Hard Rock songs with the Rock songs and Black Metal with the Metal songs
        if genre not in genres:
            for g in genres:
                if genre.find(g) > -1:
                    print("Reading genre " + genre + " as " + g)
                    genre = g

        if genre not in genres:
            print("Discarding song: wrong genre: " + genre)
            return 0, genreCount

        lyricsText = self.lyricsPattern.findall(htmlString)

        # discard song if we can't extract the lyrics
        if lyricsText == []:
            print("Discarding song: can't read lyrics")
            return 0, genreCount

        # The actual lyrics are stored per character as HTML entity... HTMLParser.unescape can fix that
        lyricsText = lyricsText[0].replace('<br />', '\n')
        lyricsText = self.h.unescape(lyricsText)

        genreCount[genre] += 1

        print('writing ' + genre + str(genreCount[genre]) + ".txt")

        f = open(genre+"/" + genre + str(genreCount[genre]) + ".txt", "w")
        try:
            f.write(lyricsText)
        except UnicodeEncodeError: # Hij crashte hier een keer bij schrijven van "ś"
            print("Discarding song: Unicode error")
            f.close()
            # roll back what we did
            os.remove(genre+"/" + genre + str(genreCount[genre]) + ".txt")
            genreCount[genre] -= 1
            return 0, genreCount
        f.close()

        return 1, genreCount

    def getGenre(self, url):
        # Retrieve the page and make it into a string
        response = urlopen(url)
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        result = self.genrePattern.findall(htmlString)

        if result == []:
            return ""

        return result[0]

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.linkDivDepth = 0
        #self.hrefPattern = re.compile(r'\"(.+)\"', re.IGNORECASE)
        self.nextPagelinkPattern = re.compile(r'.*\?pagefrom=.*', re.IGNORECASE)

    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):

        if tag == 'div':
            #handle this case first so we don't increment twice on discovery
            if self.linkDivDepth > 0:
                self.linkDivDepth += 1
            for (key, value) in attrs:
                if key == 'id' and value == 'mw-pages':
                    self.linkDivDepth += 1

        # only process links when we are inside the right div
        if(self.linkDivDepth <= 0):
            return

        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    nextPagelinkmatch = self.nextPagelinkPattern.match(value)

                    if(nextPagelinkmatch):
                        # We are grabbing the new URL. We are also adding the
                        # base URL to it. For example:
                        # www.netinstructions.com is the base and
                        # somepage.html is the new URL (a relative URL)
                        #
                        # We combine a relative URL with the base URL to create
                        # an absolute URL like:
                        # www.netinstructions.com/somepage.html
                        newUrl = parse.urljoin(self.baseUrl, nextPagelinkmatch.string)
                        self.nextLink = newUrl
                        return

                    # If it's not a nextpage link then it's a link to a song
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links += [newUrl]

    def handle_endtag(self, tag):
        # To detect when we leave the desired div
        if tag == 'div':
            if self.linkDivDepth > 0:
                self.linkDivDepth -= 1

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.links = []
        self.nextLink = ""
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)

        htmlBytes = response.read()
        # Note that feed() handles Strings well, but not bytes
        # (A change from Python 2.x to Python 3.x)
        htmlString = htmlBytes.decode("utf-8")
        self.feed(htmlString)
        return htmlString, self.links, self.nextLink


# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, jumpsize, resultsize):
    pagesToVisit = [url]
    numberVisited = 0
    resultCount = 0
    genreCount = {}
    for g in genres:
        genreCount[g] = 0
    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the word or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the word)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    while resultCount < resultsize and pagesToVisit != []:
        numberVisited = numberVisited + 1
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        print(numberVisited, "Visiting:", url)
        parser = LinkParser()
        data, links, nextLink = parser.getLinks(url)
        LE = LyricExtractor()
        for link in links:
            if 1/jumpsize > random.random(): # Skip some of the links we retrieve
                # Pokemon exception handling, gotta catch em all
                try:
                    newResults, newGenreCount = LE.ExtractLyrics(link, genreCount)
                    resultCount += newResults
                    genreCount = newGenreCount
                except:
                    continue
        pagesToVisit = pagesToVisit + [nextLink]
    print('Resultcount: ' + str(resultCount))

if __name__ == "__main__":
    main()