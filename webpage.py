class Webpage :

    def __init__(self, URL, titletext, linkText, links):
        self.URL = URL
        self.Titletext = titletext

        # building keywords like makes it safe to have an empty string keyword
        self.Keywords = (titletext + " " + linkText).split()

        self.links = links
