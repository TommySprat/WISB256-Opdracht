from webpage import Webpage
from barrel import Barrel

class Database :
    count      = 0
    urlTable   = {}
    docIDTable = []
    prTable    = []
    refTable   = []
    outgoing   = []
    incoming   = []
    webpages   = []
    barrels    = []
    words      = {}

    def __init__(self, n):
        self.count = n
        self.prTable    = [1/n  for x in range(n)]
        self.refTable   = [[0 for x in range(n)] for x in range(n)] 
        self.outgoing   = [0  for x in range(n)]
        self.incoming   = [0  for x in range(n)]

    def getDocID(self, url) :
        return self.urlTable[url]

    def discoverLinks(self):
        for webpage in self.webpages:
            docID = self.getDocID(webpage.URL)
            for url in webpage.links:
                if not url in self.urlTable.keys():
                    continue
                otherDocID = self.getDocID(url)
                self.addLink(docID, otherDocID)

    def calcPageRank(self, d, i) :
        v = 0
        for j in range(0, self.count) :
            if j != i :
                # use + 1 here, to avoid dividing by zero
                v += self.prTable[j]/(self.outgoing[j] + 1)
        pr = (1-d)+(d*v)

    def processRefTable(self) :
        for i in range(0, self.count) :
            incoming = 0
            for j in range(0, self.count) :
                incoming += self.refTable[i][j]
                self.outgoing[j] = self.refTable[i][j]
            self.incoming[i] = incoming

    def fillBarrels(self) :
        # fill barrels
        for webpage in self.webpages :
            b = Barrel(self.urlTable[webpage.URL])
            for word in webpage.Keywords :
                b.addWord(word)
            self.barrels.append(b)
        # fill words
        for barrel in self.barrels :
            for word in barrel.words :
                if word in self.words.keys() :
                    self.words[word].append(barrel.docID)
                else :
                    self.words[word] = [barrel.docID]
    
    def pageRank(self) :
        # find links
        self.discoverLinks()
        
        # use constant 0.85 from the original PageRank paper
        d = 0.85
        self.processRefTable()
        self.fillBarrels()
        for i in range(0, len(self.prTable)) :
            self.prTable[i] = self.calcPageRank(d, i)
        print('pagerank done')

    def addURL(self, url) :
        self.docIDTable.append(url)
        self.urlTable[url] = len(self.urlTable)

    def addWebpage(self, webpage):
        self.webpages.append(webpage)

    def containsURL(self, url):
        return url in self.urlTable.keys()

    def getURL(self, docID) :
        return self.docIDTable[docID]

    def addLink(self, docID1, docID2) :
        self.refTable[docID1][docID2] += 1

    def search(self, words) :
        # aantal hits:
        for word in words.keys :
            urls = []
            wordHits = 0
            for barrel in barrels :
                wordHits += barrel.search(word)
            if wordHits > 0 :
                urls.append(barrel.docID)

            # alternatief kan direct met de docIDs gezocht worden met de values.
            # misschien nog een andere value nemen dan >0 voor de gevonden urls.

            # sort alle urls op self.prTable[docID],
            # waar docID te verkrijgen is uit de docIDs met wordHits > 0
