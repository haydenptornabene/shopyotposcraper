# This HTML Scraper is designed to take the website, www.wemakewebsites.com/blog/90-....
# and take the names and urls of the 90 listed websites that use Shopify and put them
# into a list that can then be turned into a csv or JSON object.

# First we want to start with imports (http://docs.python-guide.org/en/latest/scenarios/scrape/)

from lxml import html
import requests
import re
import csv

# This is necessary to avoid the following error: 
# UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0' in position 20: ordinal not in range(128)

import sys
reload(sys)
sys.setdefaultencoding("utf8")



################################################ PREAMBLE ABOVE #############################



# requests.get will retrieve the web page with our data, parse it, and save it into 'tree'

page = requests.get('https://wemakewebsites.com/blog/90-best-shopify-stores-for-ecommerce-inspiration')
tree = html.fromstring(page.content)

# 'tree' contians the whole HTML file which allows us to use XPath or CSSSelect to parse the file.
# This scraper uses XPath

# To find the correct data: 
# Look under <div class ="field field-name-body field-type-text-with-summary field-label-hidden">
# Hit all the drop down menus until you get to <div class+"field-item even">
# You will see 90 header pairs, the data we want is within that.

# The above XPaths are found in the following div:

# <div class="field-item even">


# In order to build the correct XPath, we want to be able to grab every line of HTML 
# that has an 'http://' string in it. To do that, we use this documentation:
# http://www.zvon.org/comp/r/tut-XPath_1.html#Pages~Playing_with_names_of_selected_elements
# We can trim the strings later, lets just get a list of these elements

# This is a list of companies 

companies = tree.xpath('//h2/descendant::*/text()')

# The numbers for each company are nested in each individual string. 
# The following will remove the numbers as unique strings in the list. 

del companies[1]
del companies[82]
del companies[88]

# The following will remove the numbers at the beginning of each string. 

# The following is a regex command. The complex part is the r'^\d+\. '
# The r in front of it means raw string (make sure /characters work well) 
# The digit \d means repeated at least one or more times +
# The \. focuses on the period after the number
# It substitues that substring with an empty null string '' and boom it works

cleaned_companies = [re.sub(r'^\d+\. ', '', company) for company in companies]





# This is a list of all the urls associated with the companies

urllist = tree.xpath("//a[contains(@href,'http')]/@href")

# Based on the XPath form above, there are a number of repeated urls. 
# To eliminate them, we create a small for loop to remove redundancies

seen = set()
urls = []
for item in urllist:
    if item not in seen:
        seen.add(item)
        urls.append(item)

# There are a number of extraneous urls, one at the beginning of the list and nine
# at the end. We want to trim these values out. We delete the first one:

del urls[0]

# And now the remaining nine:

urls[107:116] = []

# There are a few repetitive urls in the mix, http vs https, .com vs. .uk, etc. 
# I will remove them manually.
# The XPath command could have been made more rigorously, will do that in future.  
 
del urls[4]
del urls[22]
del urls[26]
del urls[27]
del urls[37]
del urls[38]
del urls[40]
del urls[42]
del urls[43]
del urls[47]
del urls[48]
del urls[50]
del urls[55]
del urls[56]
del urls[59]
del urls[77]
del urls[79]


# Our final products! 

#print 'URLs: ', urls
#print 'Companies: ', cleaned_companies

# Export to a CSV (Companies First)

# Open File
resultFyle = open("scrapednames.csv",'wb')

# Create Writer Object
wr = csv.writer(resultFyle, dialect='excel')

# Write Data to File
for item in cleaned_companies:
    wr.writerow([item])

# Notice the square bracket above in ([item]) which forces each string to be 
# placed in a cell, not to have each letter it's own unique cell


# Export to a CSV (Urls Second)

resultFyle = open("scrapedurls.csv",'wb')
wr = csv.writer(resultFyle, dialect='excel')
for item in urls:
    wr.writerow([item])


print 'Printed to files'



