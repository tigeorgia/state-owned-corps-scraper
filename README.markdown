An extremely barebones scraper for the Georgian Enterprise Management Agency's [database of state-owned corporations in Georgia](http://www.ema.gov.ge/content.php?id=94&lang=geo).

Written in Python.

Usage
------------
`python scrape.py`

Results will appear in the file results-lang.tab

Dependencies
------------
[html5lib](http://code.google.com/p/html5lib/)
[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) -- should work with all BS 3.x

Languages
-----------
The database on the EMA website is in three different languages, and they may not all contain the same content. To scrape a different language, un-comment the appropriate value for the "lang" variable.
