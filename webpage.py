class Webpage :

    def __init__(self, URL, titletext, linkText, links, linkTexts):
        self.URL = URL
        self.Titletext = titletext
        self.linkText = linkText

        # building keywords like makes it safe to have an empty string keyword
        self.Keywords = (titletext + " " + linkText).split()
        # Use the special python casefold function to prepare the string independent of upper/lower case
        self.Keywords = [word.casefold() for word in self.Keywords]

        self.links = links
        self.linkTexts = linkTexts

    def __repr__(self) :
        toString = '%s' % self.linkText
        if toString != '' and self.Titletext != '' :
            toString += ' | '
        toString += self.Titletext
        if toString == '' :
            toString = self.URL
        return toString
