class Database :
    count      = 0
    urlTable   = {}
    docIDTable = []
    prTable    = []
    refTable   = []
    outgoing   = []
    incoming   = []
    webpages   = []

    def __init__(self, n):
        self.count = n
        self.urlTable   = {}
        self.docIDTable = []
        self.prTable    = [0  for x in range(n)]
        self.refTable   = [[0 for x in range(n)] for x in range(n)] 
        self.outgoing   = [0  for x in range(n)]
        self.incoming   = [0  for x in range(n)]
        self.webpages   = []

    def calcPageRank(self, i, search) :
        #TODO: add pagerank
        return

    def pageRank(self, search) :
        for i in range(0, self.count) :
            self.prTable[i] = self.calcPageRank(i, search)

    def addURL(self, url) :
        self.docIDTable.append(url)
        self.urlTable[url] = len(self.urlTable)
        self.count += 1

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
