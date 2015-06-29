class Webpage :

    def __init__(self, URL, titletext, linkText, links, linkTexts):
        self.URL = URL
        self.Titletext = titletext
        self.linkText = linkText

        # building keywords like makes it safe to have an empty string keyword
        self.Keywords = (titletext + " " + linkText).split()
        # Store all keyword in lower case
        self.Keywords = [word.lower() for word in self.Keywords]

        self.links = links
        self.linkTexts = linkTexts