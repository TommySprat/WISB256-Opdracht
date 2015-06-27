from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from webpage import Webpage
import re
from db import Database

class LinkParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.convert_charrefs = True # get rid of HTML entities
        self.charsetPattern = re.compile(r'.*charset=(.*)', re.IGNORECASE)

    def handle_starttag(self, tag, attrs):

        if tag == 'a':
            self.inATag = True
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

        if tag == 'title':
            self.inTitle = True

        if tag == 'frame':
            for (key, value) in attrs:
                if key == 'src':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

    def handle_endtag(self, tag):
        if tag == 'title':
            self.inTitle = False
        if tag == 'a':
            self.inATag = False

    def handle_data(self, data):
        if self.inTitle:
            self.title = data.strip()
        if self.inATag:
            self.linkTexts[self.links[-1]] = data.strip()
            # Not all A tags are ended properly, this is to prevent parsing the entire document as the linktext
            self.inATag = False

    def processPage(self, url, linkText):
        self.links = []
        self.linkTexts = {}
        self.title = -1
        self.baseUrl = url

        response = urlopen(url)
        # To keep track of inside which elements we are
        # This is needed to understand how to interpret data (raw text) when we encounter it
        self.inTitle = False
        self.inATag = False

        # Ignore things like PDF files, images, scripts etc.. Only parse HTML pages
        if 'text/html' in response.getheader('Content-Type'):
            # Not all sites use the same character set, we need to decode the bytes so check which set to use
            charset = "utf-8"
            m = re.findall(self.charsetPattern, response.getheader('Content-Type'))
            if(m):
                charset = m[0].strip()

            htmlBytes = response.read()
            htmlString = htmlBytes.decode(charset) # Need to prepare the data for the parser this way
            self.feed(htmlString)
            return Webpage(url, self.title, linkText, self.links, self.linkTexts)
        else:
            return None

def crawl(url, maxpages):
    pageQueue = [url]
    npagesVisited = 0
    db = Database(maxpages)
    parser = LinkParser()
    # Set up a "previous" webpage which we came from (we really didn't) but it's needed to start up the process
    webpage = Webpage("No URL", "No Title", "No linktext", [], {})

    while npagesVisited < maxpages and pageQueue != []:
        # Don't visit the same webpage again
        while pageQueue != [] and db.containsURL(pageQueue[0]):
            pageQueue = pageQueue[1:]
        if pageQueue == []:
            break
        currentUrl = pageQueue[0]
        print(npagesVisited, "Visiting:", currentUrl)

        webpage = parser.processPage(currentUrl, webpage.linkText)
        db.addURL(currentUrl)
        db.addWebpage(webpage)
        pageQueue += webpage.links
        print(webpage.URL, webpage.Titletext, webpage.Keywords, webpage.links)

        npagesVisited += 1

    print(db.refTable)
    db.discoverLinks()
    print(db.refTable)

crawl("http://www.uu.nl/", 5)

#db = Database(8)
#lp = LinkParser()
#wp = lp.processPage("http://www.cs.uu.nl/education/vak.php?stijl=2&vak=INFOFP&jaar=2014", "UU")
#print(wp.URL, wp.Titletext, wp.Keywords, wp.links)