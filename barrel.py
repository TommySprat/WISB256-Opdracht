class Barrel :
    docID       = -1
    words       = {}
    count       = -1

    def __init__(self, docID):
        self.docID = docID
        self.count = 0

    def addWord(self, word) :
        if word in self.words :
            self.words[word] += 1
        else :
            self.words[word] = 1

    def search(self, word) :
        if word in self.words.keys :
            return self.words[word]
        else :
            return 0
