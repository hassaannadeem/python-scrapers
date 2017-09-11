from bs4 import BeautifulSoup
import requests

r = requests.get("URL HERE")
html = r.text
soup = BeautifulSoup(html,'html.parser')
table = soup.find_all('td', attrs={'class': 'itm col-md-5'})
e = 0
lst = []
for w in table:
    if e%2==0:
        lst.append(w.text)
    e=e+1
newlist = [n.strip()[:-1].split("(") for n in lst]
for a in newlist:
    if len(a)==3:
        a[0] = a[0]+a[1]
        a.remove(a[1])
n = [nq[1].split(":") for nq in newlist]
print "Company,Exchange,Ticker"
e = 0
for i,j in zip(newlist,n):
    print "%s,%s,%s"%(i[0],j[0],j[1])
    e = e+1

