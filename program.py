from tkinter import *
from tkinter import ttk

#TODO: Styles maken voor de labelframes

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

lblcurrent = ttk.Label(crawlerframe, text="Current domain:")
lblcurrent.grid(column=0, row =0)

### NEW CRAWL
crawlseparator = ttk.Separator(crawlerframe)
crawlseparator.grid(row=1, column=0, columnspan=2, sticky=(W, E), pady=12)

lblurl = ttk.Label(crawlerframe, text="URL")
lblurl.grid(column=0, row =2)

urlentry = ttk.Entry(crawlerframe)
urlentry.grid(column=1, row =2)

crawlbutton = ttk.Button(crawlerframe, text="Crawl")
crawlbutton.grid(column=2, row=2, sticky=(W))

lblpagelimit = ttk.Label(crawlerframe, text="Process up to this many pages")
lblpagelimit.grid(column=0, row =3)

pagelimitbox = ttk.Combobox(crawlerframe, values=("10", "100", "1000"))
pagelimitbox.current(0)
pagelimitbox.grid(column=1, row=3)
pagelimitbox.state(['readonly'])

### SEARCH frame
searchframe = ttk.LabelFrame(root, text="Search")
searchframe.grid(column=0, row=1, sticky=(N, W, E, S))

keywordentry = ttk.Entry(searchframe)
keywordentry.grid(column=1, row =0)

searchbutton = ttk.Button(searchframe, text="Search")
searchbutton.grid(column=2, row=0)

### RESULTS frame
resultframe = ttk.LabelFrame(root, text="Results")
resultframe.grid(column=0, row =2, sticky=(N, W, E, S))


root.mainloop()