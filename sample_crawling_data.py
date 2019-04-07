import requests, json
from bs4 import BeautifulSoup
from advanced_expiry_caching import Cache

# "crawling" -- generally -- going to all links from a link ... like a spiderweb
# its specific def'n varies, but this is approximately the case in all situations
# and is like what you may want to do in many cases when scraping

######

# A "simple" example (without much fancy functionality or data processing)

# Constants
START_URL = "https://www.data.gov/"
FILENAME = "sample_secondprog_cache.json"

# So I can use 1 (one) instance of the Cache tool -- just one for my whole program, even though I'll get data from multiple places
PROGRAM_CACHE = Cache(FILENAME)

# assuming constants exist as such
# use a tool to build functionality here
def access_page_data(url):
    data = PROGRAM_CACHE.get(url)
    if not data:
        data = requests.get(url).text
        PROGRAM_CACHE.set(url, data) # default here with the Cache.set tool is that it will expire in 7 days, which is probs fine, but something to explore
    return data

#######

main_page = access_page_data(START_URL)

# explore... find that there's a <ul> with class 'topics' and I want the links at each list item...

# I've cached this so I can do work on it a bunch
main_soup = BeautifulSoup(main_page, features="html.parser")
list_of_topics = main_soup.find('ul',{'class':'topics'})
# print(list_of_topics) # cool

# for each list item in the unordered list, I want to capture -- and CACHE so I only get it 1 time this week --
# the data at each URL in the list...
all_links = list_of_topics.find_all('a')
# print(all_links) # cool
# now need each one's href attr

# # Debugging/thinking code:
#
# for link in all_links:
#     print(link['href'])
#
#     # Just text! I'm not going back to the internet at all anymore since I cached the main page the first time

# This is stuff ^ I'd eventually clean up, but probably not at first as I work through this problem.

topics_pages = [] # gotta get all the data in BeautifulSoup objects to work with...
for l in all_links:
    page_data = access_page_data(l['href'])
    soup_of_page = BeautifulSoup(page_data, features="html.parser")
    # print(soup_of_page)
    topics_pages.append(soup_of_page)

# Now I can do some investigation on just one of those BeautifulSoup instances, and thus decide what I want to do with each one...
# Each time I run the program, I'm not going to the internet at all sometimes unless some page is new or it's -- in this case -- been more than 7 days since storing data.
# After the first time, it'll run much faster! (On a certain scale, anyway)

# Just for example --
# print(topics_pages[0].prettify())
