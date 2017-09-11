import urllib2
from bs4 import BeautifulSoup
import unicodedata
import csv
response = urllib2.urlopen("URL HERE")
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

pic_url = soup.find_all('img',{"class":'ImageThumbnail-image'})[0]['src'].encode()
pic_url = "https:"+pic_url

name = soup.find_all('div',{"class":'PageProfile-info-username'})[0].text.strip().encode()

locality = soup.find_all('span',{"itemprop":'addressLocality'})[0].text.strip().encode()

country = soup.find_all('span',{"itemprop":'addressCountry'})[0].text.strip().encode()

recommendation = soup.find_all('span',{"data-target":'recommend-btn-val'})[0].text.encode()

price = soup.find_all('div',{"class":'PageProfile-info-rate-value'})[0].text.strip().encode()

rating = soup.find_all('div',{"class":'Rating Rating--labeled PageProfile-info-ratings-rating'})[0]['data-star_rating'].encode()

reviews = soup.find_all('span',{"class":'Rating-review'})[0].text.strip().encode()

jobs_completed = soup.find_all('div',{"class":'PageProfile-info-stat-value'})[0].text.strip().encode()

on_budget = soup.find_all('div',{"class":'PageProfile-info-stat-value'})[1].text.strip().encode()

on_time = soup.find_all('div',{"class":'PageProfile-info-stat-value'})[2].text.strip().encode()

repeat_hire = soup.find_all('div',{"class":'PageProfile-info-stat-value'})[3].text.strip().encode()

verification_list = soup.find_all('ul',{"class":'VerificationsList profile-side-list'})[0].findChildren('li')
ver_data = []
for e in verification_list:
    if "is-VerificationsList-verified" in e['class']:
        ver_data.append("True")
    else:
        ver_data.append("False")
top_skill = c = soup.find_all('ul',{"class":'VerificationsList profile-side-list'})[1].findChildren('li')
skill_name = ""
skill_value = ""
for e in top_skill:
    e = e.text.strip().split("\n\n")
    skill_name = skill_name+e[0]+","
    skill_value = skill_value+e[1]+","


    
f = open('scraping.csv','wb')
csvwriter = csv.writer(f)
csvwriter.writerow(["PicURL","name","locality","country","recommendation","price","rating","reviews","jobs completed","on budget","on time","repeat hire","Facebook","Preferred Freelancer","Payment Verified","Phone Verified","Identity verified","Email verified",skill_name])
csvwriter.writerow([pic_url,name,locality,country,recommendation,price,rating,reviews,jobs_completed,on_budget,on_time,repeat_hire,ver_data[0],ver_data[1],ver_data[2],ver_data[3],ver_data[4],ver_data[5],skill_value])
f.close()
