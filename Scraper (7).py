import urllib2
from bs4 import BeautifulSoup
import unicodedata
import csv
base_url = 'URL HERE'
response = urllib2.urlopen("URL HERE")
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
first_url = soup.find_all(class_="noTrigger")[0].get('href')
first_url = unicodedata.normalize('NFKD', first_url).encode('ascii','ignore')

pic_div = soup.find_all('div',{"class":'scrollableHolder tw3-profile__photosHolder mb--loose tw3-profile__photosHolder--large jsScrollableHolderLarge'})
pics = pic_div[0].find_all('div',{"class":"tw3-profile__photo__img tw3-thumb__link__image"})
pic_urls = []
for e in pics:
    u = e["style"].split('\'')[1].encode()
    pic_urls.append(u)

data = soup.find_all('p',class_ = 'tw3-field-value')
bio= []
for e in data:
    d = e.text
    d = unicodedata.normalize('NFKD', d).encode('ascii','ignore')
    bio.append(d)
pic_links = ""
for e in pic_urls:
    pic_links = pic_links+e+"\n"

    
f = open('scrapingdata.csv','wb')
csvwriter = csv.writer(f)
csvwriter.writerow(["CityURL","Firstname","Gender","Birthdate","City","Preffered Language","I also speak","Relationship Status","Sexual Orientation","Pictures URLS"])
csvwriter.writerow([base_url+first_url,bio[0],bio[1],bio[2],bio[3],bio[4],bio[5],bio[6],pic_links])

f.close()
