from tkinter import *
from tkinter import ttk
from tkinter import font
from crawler import crawl
import webbrowser
from db import Database
import threading

#TODO: Styles maken voor de labelframes

database = None

def open_url(url):
    webbrowser.open_new(url)

def crawlButtonClicked():
    url = str(urlentry.get())
    maxpages = int(pagelimitbox.get())
    database = Database(maxpages)
    pbar.configure(value=0, maximum=maxpages)
    # Crawl in a thread to keep the interface mainloop going (which allows the progress bar to be redrawn)
    global crawler_thread
    crawler_thread = threading.Thread(target=crawl, args=(url, maxpages, database, crawlerPageCallback, crawlerFinishedCallback))
    crawler_thread.start()

def crawlerPageCallback():
    pbar.step()

def crawlerFinishedCallback():
    print("Done crawling the internet")
    maxpages = int(pagelimitbox.get())
    pbar.configure(value=maxpages)

def searchButtonClicked():
    resultList = []
    urls = ["www.google.nl", "www.wikipedia.com", "www.tweakers.net"]
    for i in range(3):
        resultList.append(ttk.Label(resultframe, text=urls[i], cursor="hand2"))
        resultList[i].grid(column=0, row=i)
        resultList[i].bind('<Button-1>', lambda e, url=urls[i]:open_url(url))
        print(resultList[i]['style'])
        print(resultList[i].winfo_class())
        url_style_label(resultList[i])

def url_style_label(label):
    urlFont = font.Font(family='Helvetica', size=14, underline=1)
    label.configure(font=urlFont, foreground='blue', padding=(1, 2))


root = Tk()
root.title("Gel Goo")

# These 3 lines distribute the vertical space between the three main frames
root.rowconfigure(0, weight =1)
root.rowconfigure(1, weight =1)
root.rowconfigure(2, weight =4)
root.columnconfigure(0, weight=1)

### CRAWLER frame
crawlerframe = ttk.LabelFrame(root, text="Crawler")
crawlerframe.grid(column=0, row =0, sticky=(N, W, S))
crawlerframe.columnconfigure(1, weight=1)

lblcurrentDomain = ttk.Label(crawlerframe, text="Current domain:")
lblcurrentDomain.grid(column=0, row =0)

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

pagelimitbox = ttk.Combobox(pagelimitFrame, values=("5", "10", "100", "1000"))
pagelimitbox.current(0)
pagelimitbox.grid(column=2, row=1)
pagelimitbox.state(['readonly'])

pbar = ttk.Progressbar(crawlerframe, length=400)
pbar.grid(column=0, row=4, columnspan=2)

### SEARCH frame
searchframe = ttk.LabelFrame(root, text="Search")
searchframe.grid(column=0, row=1, sticky=(N, W, E, S))

keywordentry = ttk.Entry(searchframe)
keywordentry.grid(column=1, row =0)

searchbutton = ttk.Button(searchframe, text="Search", command=searchButtonClicked, state=DISABLED)
searchbutton.grid(column=2, row=0)

### RESULTS frame
resultframe = ttk.LabelFrame(root, text="Results")
resultframe.grid(column=0, row =2, sticky=(N, W, E, S))


root.mainloop()