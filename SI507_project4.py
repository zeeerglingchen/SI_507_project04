import requests
import json
import csv
from bs4 import BeautifulSoup
from advanced_expiry_caching import Cache
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

FILENAME = "nps_cache.json"
PROGRAM_CACHE = Cache(FILENAME)

START_URL = "https://www.nps.gov/index.htm"


def access_page_data(url):
    data = PROGRAM_CACHE.get(url)
    if not data:
        data = requests.get(url).text
        PROGRAM_CACHE.set(url, data)
    return data

main_page = access_page_data(START_URL)
main_soup = BeautifulSoup(main_page, features="html.parser")
find_data = main_soup.find("ul",{"class":"dropdown-menu SearchBar-keywordSearch"})

state = find_data.find_all("a")

state_list = []
for a in state:
    state_add = "https://www.nps.gov" + a['href']
    state_list.append(state_add)
# print (state_list)

state_data = []
for li in state_list:
    state_page = access_page_data(li)
    state_soup = BeautifulSoup(state_page, features="html.parser")
    state_data.append(state_soup)

# print (state_data[0].find_all("ul"))

head = ["Name","Type","Description","Location"]
with open('NationalSites.csv', 'w', newline = '') as csv_file:
    line = csv.writer(csv_file)
    line.writerow(head)

    for each_state in state_data:
        tag = each_state.find("ul",{"id":"list_parks"})
        SiteName = tag.find_all("h3")
        AllNames = []
        for name in SiteName:
            AllNames.append(name.text)

        SiteType = tag.find_all("h2")
        AllTypes = []
        for site in SiteType:
            AllTypes.append(site.text)


        Des = tag.find_all("p")
        AllDes = []
        for destext in Des:
            AllDes.append(destext.text)


        SiteLo = tag.find_all("h4")
        AllLo = []
        for lo in SiteLo:
            AllLo.append(lo.text)

        length = len(AllNames)
        for i in range(length - 1):
            row = [AllNames[i],AllTypes[i],AllDes[i],AllLo[i]]
            if AllNames[i] == " ":
                AllNames[i] = "NONE"

            if AllTypes[i] == " ":
                AllTypes[i] = "NONE"

            if AllDes[i] == " ":
                AllDes[i] = "NONE"

            if AllLo[i] == " ":
                AllLo[i] = "NONE"
            line.writerow(row)
