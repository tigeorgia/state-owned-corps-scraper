import urllib2
from BeautifulSoup import BeautifulSoup
import re
import time
import codecs
import html5lib
from html5lib import treebuilders

#lang = u'eng'
#lang = u'geo'
lang = u'rus'
filename=u'results-'+lang+u'.csv'
# Clobber existing file
f = codecs.open(filename, 'w', 'utf-8')
f.write(u'Name\tID\tOfficial Address\tActual Address\tPhone\tFax\tE-Mail\tWebsite\tForm\tStatus\tNo. Employees\tAuthorized Capital\tState share\tDir. FName\tDir. LName\tDir. Title\tDir. Phone\tDir. Mobile\tURL\n')
f.close()
f = codecs.open(filename, 'a', 'utf-8')

prefix = u"http://www.ema.gov.ge/"
firstURL = u"content.php?id=94&lang="+lang+u"&s=1&form=&name=&idcode=&phone=&fax=&email=&status=&employee=&capital=&share=&juraddress=&address=&x=51&y=4"
page = urllib2.urlopen(prefix+firstURL)

soup = html5lib.parse(page, treebuilder="beautifulsoup", encoding="utf-8")

# Count the number of pages of results
pgDivs = soup.findAll('div', attrs={"class": "page-noactive"})
pgURLs = [d.a['href'] for d in pgDivs] #Get the href attribute of every <a> tag in pgDivs
pgURLs.insert(0, firstURL) # So that pgURLs truly contains all pages

#print soup.prettify()

count = 0
# For each result page, visit every result listing
for url in pgURLs: # Loop over all pages of results
    print u"loading result page"
    resultPg = urllib2.urlopen(prefix+url)
    print u"parsing"
    soup = html5lib.parse(resultPg, treebuilder="beautifulsoup", encoding="utf-8")
   
    entDivs = soup.findAll('div', attrs={"class": "productions-content-name"})
    entURLs = [d.a['href'] for d in entDivs] # See above.
    
    # For each enterprise, output its data on one line.
    for eDiv in entDivs: # Loop over all enterprises on a page
#        print "enterprise div loop"
        time.sleep(1) # Self-limit so we don't hammer the server
        
        entPg = urllib2.urlopen(prefix+eDiv.a['href']) # Follow the link to the enterprise page
        soup = html5lib.parse(entPg, treebuilder="beautifulsoup", encoding="utf-8")
        
        infoDivs = soup.findAll('div', attrs={"class": "productions-content-description"})
        
# Construct each line of the output file, tab-delimited
        count += 1
        print count
        infoLn = eDiv(text=True)[0]+u"\t" # Start with the name of the company
        for iDiv in infoDivs: # Loop over all info items in an enterprise
#            print "info div loop"
            text = iDiv(text=True)
            if len(text) == 1:
                info = u"\t"
            else:
                info = text.pop()+u"\t" # Assumes that the last item is the text we want
            infoLn = infoLn+info
        infoLn = infoLn+prefix+eDiv.a['href']+u"\n"
        #print infoLn.encode("utf-8")
        print infoLn
        f.write(infoLn)

f.close()
