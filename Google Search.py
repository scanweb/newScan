from googlesearch import search
from bs4 import BeautifulSoup
import requests
def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))

    gs = search("quick and dirty")
    gs.results_per_page = 50
    results = gs.get_results()
    for res in results:
    print(res.title.encode("utf8"))
    print(res.desc.encode("utf8"))
    print(res.url.encode("utf8"))

except SearchError, e:
  print "Search failed: %s" % e
