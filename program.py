from tkinter import *
from tkinter import ttk, messagebox
from tkinter import font
from crawler import crawl
import urllib.parse
from urllib.request import urlopen
import webbrowser
from db import Database
import threading

global resultContentFrame
global database
database = None

def open_url(url):
    webbrowser.open_new(url)

def crawlButtonClicked():
    url = str(urlentry.get())
    try:
        urlopen(url)
    except:
        messagebox.showerror(message='Please enter a valid URL such as http://www.google.com', title='Invalid URL')
        return

    maxpages = int(pagelimitbox.get())
    global database
    database = Database(maxpages)
    pbarcrawler.configure(value=0, maximum=maxpages)
    # Crawl in a thread to keep the interface mainloop going (which allows the progress bar to be redrawn)
    global crawler_thread
    crawler_thread = threading.Thread(target=crawl, args=(url, maxpages, database, crawlerPageCallback, crawlerFinishedCallback))
    crawler_thread.start()
    lblcurrentDomain.configure(text=urllib.parse.urlparse(url).netloc, foreground='purple')
    lblstatus.configure(text="Crawling the web, please wait...")

def crawlerPageCallback():
    pbarcrawler.step()

def crawlerFinishedCallback():
    print("Done crawling the internet")
    maxpages = int(pagelimitbox.get())
    pbarcrawler.configure(value=maxpages)

    pbarpagerank.start()
    global database
    global pagerank_thread
    pagerank_thread = threading.Thread(target=database.pageRank, kwargs={'callbackOnFinish' : pageRankFinishedCallback})
    pagerank_thread.start()
    lblstatus.configure(text="Running the PageRank algorithm")
    lblcurrentDomain.configure(foreground='green')

def pageRankFinishedCallback():
    pbarpagerank.stop()
    lblstatus.configure(text="Search engine is ready. Enter your search terms")
    searchbutton.configure(state=NORMAL)

def searchButtonClicked():
    global database
    global resultContentFrame
    resultContentFrame.grid_forget()
    resultContentFrame = ttk.Frame(resultframe)
    resultContentFrame.grid(row=0, column=0)

    searchterms = str(keywordentry.get()).split()
    # Use the special python casefold function to prepare the string independent of upper/lower case
    searchterms = [word.casefold() for word in searchterms]

    webpages = database.search(searchterms)
    # Return a maximum of 10 results
    if len(webpages) > 10:
        webpages = webpages[:10]
    for i in range(len(webpages)):
        resultLabel = ttk.Label(resultContentFrame, text=str(i+1) + " " + webpages[i].Titletext, cursor="hand2")
        urlLabel = ttk.Label(resultContentFrame, text=webpages[i].URL, cursor="hand2")
        spacerLabel = ttk.Label(resultContentFrame, text=" ")
        resultLabel.grid(column=0, row=3*i)
        urlLabel.grid(column=0, row=3*i+1)
        spacerLabel.grid(column=0, row=3*i+2)
        resultLabel.bind('<Button-1>', lambda e, url=webpages[i].URL: open_url(url))
        urlLabel.bind('<Button-1>', lambda e, url=webpages[i].URL: open_url(url))
        title_style_label(resultLabel)
        url_style_label(urlLabel)

def title_style_label(label):
    titleFont = font.Font(family='Helvetica', size=12, underline=1)
    label.configure(font=titleFont, foreground='blue')

def url_style_label(label):
    urlFont = font.Font(family='Helvetica', size=9, underline=1)
    label.configure(font=urlFont, foreground='blue')

root = Tk()
root.title("Gel Goo")

# These 3 lines distribute the vertical space between the three main frames
root.rowconfigure(0, weight =1)
root.rowconfigure(1, weight =1)
root.rowconfigure(2, weight =1)
root.rowconfigure(3, weight =4)
root.columnconfigure(0, weight=1)

### STATUS frame
statusframe = ttk.LabelFrame(root, text='Status')
statusframe.grid(column=0, row=0, sticky=(N,W,S))
statusframe.columnconfigure(1, weight=1)
statusframe.rowconfigure(1, weight=1)

statusTitleFont = font.Font(family='Helvetica', size=16, weight='bold')
lblstatusText = ttk.Label(statusframe, text='Status:', font=statusTitleFont)
lblstatusText.grid(column=0, row=0)

statusFont = font.Font(family='Helvetica', size=14, weight='bold')
lblstatus = ttk.Label(statusframe, text='Crawl a page before you can search', font=statusFont)
lblstatus.grid(column=0, row=1)

### CRAWLER frame
crawlerframe = ttk.LabelFrame(root, text="Crawler")
crawlerframe.grid(column=0, row =1, sticky=(N, W, S))
crawlerframe.columnconfigure(1, weight=1)

domainFrame = ttk.Frame(crawlerframe)
domainFrame.grid(column=0, row=0, sticky=(N, W))

lblcurrentDomainText = ttk.Label(domainFrame, text="Current domain:")
lblcurrentDomainText.grid(column=0, row =0)

lblcurrentDomain = ttk.Label(domainFrame, text="None", foreground='red')
lblcurrentDomain.grid(column=1, row =0)

### NEW CRAWL
crawlseparator = ttk.Separator(crawlerframe)
crawlseparator.grid(row=1, column=0, columnspan=2, sticky=(W, E), pady=12)

urlAndButtonFrame = ttk.Frame(crawlerframe)
urlAndButtonFrame.grid(column=0, row = 2, sticky=W)

lblurl = ttk.Label(urlAndButtonFrame, text="URL")
lblurl.grid(column=0, row =0)

urlentry = ttk.Entry(urlAndButtonFrame)
urlentry.grid(column=1, row =0)

crawlbutton = ttk.Button(urlAndButtonFrame, text="Crawl", command=crawlButtonClicked)
crawlbutton.grid(column=2, row=0, sticky=(W))

pagelimitFrame = ttk.Frame(crawlerframe)
pagelimitFrame.grid(column=0, row=3)

lblpagelimit = ttk.Label(pagelimitFrame, text="Maximum pages to visit")
lblpagelimit.grid(column=1, row =1)

pagelimitbox = ttk.Combobox(pagelimitFrame, values=("5", "10", "25", "50", "100", "150", "200", "250", "300", "500", "1000"))
pagelimitbox.current(0)
pagelimitbox.grid(column=2, row=1)
pagelimitbox.state(['readonly'])

pbarcrawler = ttk.Progressbar(crawlerframe, length=400)
pbarcrawler.grid(column=0, row=4, columnspan=2)

pbarpagerank = ttk.Progressbar(crawlerframe, length=400, mode='indeterminate')
pbarpagerank.grid(column=0, row=5, columnspan=2)

### SEARCH frame
searchframe = ttk.LabelFrame(root, text="Search")
searchframe.grid(column=0, row=2, sticky=(N, W, E, S))

keywordentry = ttk.Entry(searchframe)
keywordentry.grid(column=1, row =0)

searchbutton = ttk.Button(searchframe, text="Search", command=searchButtonClicked, state=DISABLED)
searchbutton.grid(column=2, row=0)

### RESULTS frame
resultframe = ttk.LabelFrame(root, text="Results")
resultframe.grid(column=0, row =3, sticky=(N, W, E, S))

# To contain the results but it will be a new object every time
resultContentFrame = ttk.Frame(resultframe)
resultContentFrame.grid(row=0, column=0)

root.mainloop()
