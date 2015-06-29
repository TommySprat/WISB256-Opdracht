class Barrel :
    
    def __init__(self, docID):
        self.docID = docID
        self.words = {}

    def addWord(self, word) :
        if word in self.words :
            self.words[word] += 1
        else :
            self.words[word] = 1

    def search(self, word) :
        if word in self.words.keys() :
            return self.words[word]
        else :
            return 0

    def __str__(self) :
        return 'barrel: docID:%s, words:%s' % (self.docID, self.words)

    def __repr__(self) :
        return 'barrel: docID:%s, words:%s' % (self.docID, self.words)
