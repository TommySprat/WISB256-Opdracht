from webpage import Webpage
import barrel

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

    def calcPageRank(self, d, i) :
        v = 0
        for j in range(0, self.count) :
            if j != i :
                v += self.prTable[j]/self.outgoing[j]
        pr = (1-d)+(d*v)

    def pageRank(self) :
        # use constant 0.85 from the original PageRank paper
        d = 0.85
        processRefTable()
        fillBarrels()
        for i in range(0, self.count) :
            self.prTable[i] = self.calcPageRank(d, i)

    def getWords(self, webpage) :
        return [webpage.links, webpage.Titletext, webpage.Keywords, webpage.links]

    def fillBarrels(self) :
        for webpage in self.webpages :
            b = Barrel(urlTable[webpage.URL])
            for word in self.getWords(webpage) :
                b.addWord(word)
            self.barrels.append(b)
        for barrel in self.barrels :
            for word in barrel.words.keys :
                if word in self.words.keys :
                    self.words[word] = [barrel.docID]
                else :
                    self.words[word].append(barrel.docID)

    def addURL(self, url) :
        self.docIDTable.append(url)
        self.urlTable[url] = len(self.urlTable)

    def addWebpage(self, webpage):
        self.webpages.append(webpage)

    def containsURL(self, url):
        return url in self.urlTable.keys()

    def getDocID(self, url) :
        return self.urlTable[url]

    def getURL(self, docID) :
        return self.docIDTable[docID]

    def addLink(self, docID1, docID2) :
        self.refTable[docID1][docID2] += 1

    def discoverLinks(self):
        for webpage in self.webpages:
            docID = self.getDocID(webpage.URL)
            for url in webpage.links:
                if not url in self.urlTable.keys():
                    continue
                otherDocID = self.getDocID(url)
                self.addLink(docID, otherDocID)

    def processRefTable(self) :
        for i in range(0, self.count) :
            incoming = 0
            for j in range(0, self.count) :
                incoming += self.refTable[i][j]
                self.outgoing[j] = self.refTable[i][j]
            self.incoming[i] = incoming
