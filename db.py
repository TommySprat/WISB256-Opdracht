from webpage import Webpage
from barrel import Barrel

class Database :
    # use just one iteration normally
    limit      = 1
    # use constant value 0.85 from the original PageRank paper
    d          = 0.85

    def __init__(self, n):
        self.urlTable   = {}
        self.wordURL    = {}
        self.words      = {}
        self.docIDTable = []
        self.webpages   = []
        self.barrels    = []
        self.count      = n
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

    def calcPageRank(self, i) :
        v = 0
        for j in range(0, self.count) :
            if j != i :
                # use + 1 here, to avoid dividing by zero
                v += self.prTable[j]/(self.outgoing[j] + 1)
        return (1 - self.d) + (self.d * v)

    def processRefTable(self) :
        for i in range(0, self.count) :
            outgoing = 0
            for j in range(0, self.count) :
                outgoing += self.refTable[i][j]
                self.incoming[j] += self.refTable[i][j]
            self.outgoing[i] = outgoing

    def fillBarrels(self) :
        # fill barrels
        self.barrels = {}
        for webpage in self.webpages :
            barrel = Barrel(self.urlTable[webpage.URL])
            for word in webpage.Keywords :
                barrel.addWord(word)
            self.barrels[barrel.docID] = barrel
        # fill words
        for barrel in self.barrels.values() :
            for word in barrel.words :
                if word in self.words.keys() :
                    self.words[word].append(barrel.docID)
                else :
                    self.words[word] = [barrel.docID]
    
    def pageRank(self, callbackOnFinish) :
        # find links
        self.discoverLinks()
        self.processRefTable()
        self.fillBarrels()

        for _ in range(0, self.limit) :
            for i in range(0, len(self.prTable)) :
                self.prTable[i] = self.calcPageRank(i)
        callbackOnFinish()

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

    def sort(self, docID) :
        return self.wordURL[docID]

    def search(self, words) :
        # aantal hits:
        self.wordURL = {}
        wordIdToHits = {}
        for word in words :
            wordHits = 0
            for barrel in self.barrels.values() :
                hits = barrel.search(word)
                wordHits += hits
                if hits > 0 :
                    if barrel.docID in wordIdToHits.keys() :
                        wordIdToHits[barrel.docID] += wordHits
                    else :
                        wordIdToHits[barrel.docID] = wordHits
        for docID in wordIdToHits :
            self.wordURL[docID] = (wordIdToHits[docID], self.prTable[docID])
        sortList = sorted(self.wordURL, key=self.sort)
        sortList = [self.getURL(docID) for docID in sortList]
        sortList.reverse()
        return sortList
