from bs4 import BeautifulSoup
import requests
import codecs




r = requests.get("URL HERE")
html = r.text
soup = BeautifulSoup(html,'html.parser')
table = soup.find_all('tr')

e = 0
lst = []
for w in table:
    lst.append(w.text)

l=[]
print "FilingDate,TransactionDate,InsiderName,OwnershipType,Securities,Nature of transaction,Volume or Value,Price"
lst = lst[5:]
for e in lst:
    s = e.encode("utf-8")
    s = s.replace(" ","")
    s = s.replace("\t\t","\t")
    s = s.replace("\xc2\xa0","--")
    s = s.split('\t')
    s = s[1:]
    l.append(s)
    #if s[6] and e[7]:
    print "%s,%s,%s,%s,%s,%s,%s,%s" %(s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7])
    

