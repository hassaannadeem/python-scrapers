import urllib2
from bs4 import BeautifulSoup
import unicodedata
import csv
from selenium import webdriver
from time import sleep
d = webdriver.PhantomJS(executable_path=r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

response = urllib2.urlopen("URL HERE")
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

base_url="https://coinmarketcap.com"
table = soup.find("table",id="currencies-all")
soup2 = BeautifulSoup(str(table), 'html.parser')
trs = soup2.find_all("tr")
trs = trs[1:]
f = open('scraping.csv','wb')
csvwriter = csv.writer(f)
csvwriter.writerow(["Coin Name","1-Symbol","2-Website","3-Rank","4-Reddit"])
#

for a in trs:
    symbol = a.find_all(class_="text-left")[0].text.encode()
    soup4 = BeautifulSoup(str(a), 'html.parser')
    name_td = soup4.find_all(class_="currency-name")
    soup_a = BeautifulSoup(str(name_td), 'html.parser')
    link = soup_a.a.get("href")
    name = soup_a.a.string
    url = base_url+link
    d.get(url+"#social")
    html = d.page_source
    soup = BeautifulSoup(html, 'html.parser')
    website_ul = soup.find_all(class_="list-unstyled")
    soup3 = BeautifulSoup(str(website_ul), 'html.parser')
    lis = soup3.find_all("li")
    website = lis[0].find_all("a")
    if(len(website) > 0):
        website = website[0].get("href")
    else:
        website = ""
    rank = soup.find_all(class_ = 'label label-success')
    rank = rank[0].text.encode()
    
    reddit_head = soup.find_all('h4',class_ = 'reddit-title')
    if(len(reddit_head) > 0):
        reddit = reddit_head[0].find_all("a")[0].get("href")
    else:
        reddit = ""
    csvwriter.writerow([name,symbol,website,rank,reddit])
    print rank


    

print "done"
f.close()
