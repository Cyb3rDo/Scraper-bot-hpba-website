# Scraper bot for gathering data from www.hpba.org website.

This documents is to document usage and experience from developing source code for the
Scraper bot to gather data from www.hpba.org website.

The project has been somewhat challenging due to the structure of the data provided at the
www.hpba.org website.

There has been the 2 hidden servers - first the overall search page and details pages, and the
second is the NFI certified staff information.

One other challenge was how to get the Organization Type. There were no links to be found for
the different codes so I had to get the data extracted from the JavaScript code.

The data seems also to be quite unstructured: phone number might be missing, there are
maybe more address lines for each organization.

But the overall research and testing has led me to write a code structure that can handle the
data gathering for this website.

Minor changes to the website can be handled well, in case of bigger structural changes on the
website might require more research.

In future - other tools might be better to be used - ie to handle JavaScript.

The code is documented with comments to explain what it does.

Overall it was a fun project to work with.

**Requirement**

You will need the following libraries installed:

* Python Requests
* BeautifulSoup4

I wrote the source code with Python 3.5 installed , from the Anaconda distribution . Any
distribution above that would be fine.

**Usage**

Before you start executing the script you need to update the start_url variable in the beginning
of the code.

_See this line (line number 9) in source code:_

start_url =
urlopen("http://secure.hpba.org/cvweb/cgi-bin/utilities.dll/CustomList?ORGNAME_field=&ORGTYPE=&CITY_field=&STATECD=&ZIP_field=&DISTANCE=5000&COUNTRY_field=&_MULTIPLE_PRODUCT_TYPELIST=&_MULTIPLE_PRODUCT_CLASSLIST=&EMAIL=&ORGNAME=&CITY=&ZIPSEARCH=&ZIPDISTSEARCH=&COUNTRYSEARCH=&RANGE=1%2F2266&NOWEBFLG=%3C%3EY&ISMEMBERFLG=Y&SHOWSQL=N&SORT=ORGNAME&SQLNAME=ORGSEARCH&WHP=organization.htm&WBP=organizationList.htm")

Go to the search box on the website and get the maximum number of records.
Then got to the source code and change the highlighted part of the start_url with the
maximum number of records found. At the time being it was 2266 (See the part of url that has this part in it "&RANGE=1%2F2266&NOWEBFLG", F2266 is the number you need to change)

Go to the command line, navigate to the desired folder and execute this line: python
final_scrape_hpba.py

I assume you have Python installed to PATH. Google how to do that for your OS.

Allow the bot to run for about 40 - 60 minutes. The loop sleeps for 1 second to not overload the
servers and not ban the bot.

It will create a file called "hpba_pitts_and_spitts.csv" in your current working directory (the folder
you moved to)

