from webpage import Webpage
from barrel import Barrel

class Database :
    # use 10 iterations, so the pagerank value stabilises a bit
    limit = 10
    # use constant value 0.85 from the original PageRank paper
    d     = 0.85
    # set debug value to True, so we can see statistics in the corresponding files
    debug = True

    def __init__(self, n):
        self.urlTable   = {}
        self.wordURL    = {}
        self.words      = {}
        self.pageDict   = {}
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
            if j != i and self.outgoing[j] != 0 :
                v += self.prTable[j]/(self.outgoing[j])
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
        self.pageDict[webpage.URL] = webpage

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
        docIdToHits = {}
        for word in words :
            for barrel in self.barrels.values() :
                hits = barrel.search(word)
                if hits > 0 :
                    if barrel.docID in docIdToHits.keys() :
                        docIdToHits[barrel.docID] += hits
                    else :
                        docIdToHits[barrel.docID] = hits
        
        if self.debug :
            file = open('results.txt', 'w')
            print('search: %s' % words, file=file)
        for docID in docIdToHits :
            self.wordURL[docID] = (docIdToHits[docID], self.prTable[docID])
            if self.debug :
                print('%s : %s' % (self.getURL(docID), self.wordURL[docID]), file=file)
        if self.debug :
            file.close()
            file2 = open('prTable.txt', 'w')
            for i in range(0, len(self.prTable)) :
                print('%s, %s' % (self.getURL(i), self.prTable[i]), '\n', file=file2)
            file2.close()
            file3 = open('barrels.txt', 'w')
            for barrel in self.barrels.values() :
                print(barrel, sep='\n', file=file3)
            file3.close()
            file4 = open('words.txt', 'w')
            for word in self.words :
                print(word, sep='\n', file=file4)
            file4.close()
            file5 = open('urls.txt', 'w')
            for url in self.urlTable :
                print(url, sep='\n', file=file5)
            file5.close()
        sortList = sorted(self.wordURL, key=self.sort)
        sortList = [self.pageDict[self.getURL(docID)] for docID in sortList]
        sortList.reverse()
        return sortList
