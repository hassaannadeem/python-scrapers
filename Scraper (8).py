

# to download html data
import urllib
import urllib2
from bs4 import BeautifulSoup
import unicodedata
import csv

# connect mysql
import MySQLdb
# for sleep
import time

# for cronjob
import datetime

# Converts provided xlsx file to list of sites
def readSitesFromExcel():
    import zipfile
    from xml.etree.ElementTree import iterparse
    z = zipfile.ZipFile("Trip.xlsx")
    strings = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
    rows = []
    row = {}
    value = ''
    for e, el in iterparse(z.open('xl/worksheets/sheet1.xml')):
        if el.tag.endswith('}v'): # <v>84</v>
            value = el.text
        if el.tag.endswith('}c'): # <c r="A3" t="s"><v>84</v></c>
            if el.attrib.get('t') == 's':
                value = strings[int(value)]
            letter = el.attrib['r'] # AZ22
            while letter[-1].isdigit():
                letter = letter[:-1]
            row[letter] = value
            value = ''
        if el.tag.endswith('}row'):
            rows.append(row)
            row = {}

    sites = []
    restaurantids = []
    rownr = 1
    skipRows = 2

    for row in rows:
        #print(len(row))
        if rownr > skipRows and len(row) > 1:
            site = str(row['A'])
            res = str(row['B'])

            if len(site) >= 2:
                print(site)
                sites.append(site)
                restaurantids.append(res)
        rownr = rownr + 1


    return sites, restaurantids
def insertIntoMySQL(data):

    conn = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="root",  # your password
                         db="flintxsy_BAWrestaurant")        # name of the data base

    x = conn.cursor()

    query = "INSERT INTO hotel_tripadvisor(date,page_url,average,excellent,poor,reviews,terrible,very_good,score,hotel_id) VALUES (NOW(),'" + str(data[7]) + "','" + str(data[2]) + "','" + str(data[0]) + "','"+ str(data[3]) + "','"+ str(data[5])+ "','" + str(data[4]) + "','" + str(data[1]) + "','" + str(data[6]) + "','"+ str(data[8]) + "');";
    print(query)



    try:
       x.execute(query)
       conn.commit()
    except:
       conn.rollback()

    conn.close()

def header():
    print("===========================")
    print("tripadvisor hotel")
    print("===========================")

def scraper(url):
    response = urllib2.urlopen(url)
    html =   response.read()
    soup = BeautifulSoup(html, 'html.parser')

    rating_div = soup.find_all('div',{"id":'ratingFilter'})
    rating_div = str(rating_div[0])
    soup1 = BeautifulSoup(rating_div, 'html.parser')
    ratings_li = soup1.find_all('li',{"class":'filterItem'})
    data = []
    for li in ratings_li:
        temp_soup = BeautifulSoup(str(li), 'html.parser')
        spans = temp_soup.find_all('span')
        span_list = str(spans[-2]).split("<span>")
        data.append(span_list[1])
    reviews = soup.find_all('a',{"class":'seeAllReviews'})
    reviews_count = [int(s) for s in reviews[0].text.replace(",","").split() if s.isdigit()]    
    data.append(reviews_count[0])
    rating_value = soup.find_all('span',{"class":'overallRating'})
    rating_value = rating_value[0].text.encode().strip()
    data.append(rating_value)
    return data

header()
siteId = 0
sites, hotel_ids = readSitesFromExcel()

for site in sites:
    url = site
    print("--------------------------------------------")
    print(url)
    data = scraper(url)
    print("Excellent: "+data[0])
    print("Very Good: "+data[1])
    print("Average: "+data[2])
    print("Poor: "+data[3])
    print("Terrible: "+data[4])
    print("Reviews: "+str(data[5]))
    print("Rating: "+data[6])
    print("--------------------------------------------")
    data.append(site)
    data.append(hotel_ids[siteId])
    insertIntoMySQL(data)
    time.sleep(5)
    siteId = siteId + 1
    
