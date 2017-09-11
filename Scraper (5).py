__author__ = 'shawn'
import mechanize
import cookielib
import xlrd
import sys
from xml.sax import saxutils, parse
from xml.sax import handler

class ExcelHandler(handler.ContentHandler):
    def __init__(self):
        self.chars = [  ]
        self.cells = [  ]
        self.rows = [  ]
        self.tables = [  ]
    def characters(self, content):
        self.chars.append(content)
    def startElement(self, name, atts):
        if name=="Cell":
            self.chars = [  ]
        elif name=="Row":
            self.cells=[  ]
        elif name=="Table":
            self.rows = [  ]
    def endElement(self, name):
        if name=="Cell":
            self.cells.append(''.join(self.chars))
        elif name=="Row":
            self.rows.append(self.cells)
        elif name=="Table":
            self.tables.append(self.rows)


br= mechanize.Browser()
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Set the page to open
url='URL HERE'
response = br.open(url)
print br.response().read()


#uncomment to print forms
for form in br.forms():
    print "Form name:", form.name
    print form
br.form = list(br.forms())[2]
br.form.set_all_readonly(False)
br.select_form(nr=2)
br.form['portfolios']='239832-239727-239837-239491-239420-239493-239485-239496-239624-239836-239843-239422-239839-239840-239834-239495-239848-251422-251421-239858-239828-239490-239492-239697-239486-239488-239846-239476-239433-272269-239487-239625-262831-239569-239489-239548-239743-239857-275749-239851-239439-239636-239711-239845-239441-239416-239478-239418-239863-262832-239694-251423-239556-239558-239859-239860-239852-239435-239842-271493-239838-239698-269105-239414-239604-239844-239576-239532-239755-239640-239449-241528-239470-272108-239498-272102-239841-239732-251242-239497-239554-239474-239616-272952-239847-239447-239573-272104-239442-239574-239481-251243-240642-275742-277692-272106-277693-239483-239562-275746-239611-239549-272110-277689-275744-277690-277691'
br.submit()
with open("excel.xml", "w") as f1:
    f1.write(br.response().read())
f1.close()

replacements = {'ss:Workbook':'Workbook', 'ss:Styles':'Styles', 'ss:Style':'Style', 'ss:Alignment':'Alignment', 'ss:Font':'Font', 'ss:NumberFormat':'NumberFormat','ss:Worksheet':'Worksheet','ss:Table':'Table','ss:Row':'Row','ss:Cell':'Cell','&':' and '}

with open('excel.xml') as infile, open('output.xml', 'w') as outfile:
    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        outfile.write(line)
        
excelHandler = ExcelHandler( )
parse("output.xml", excelHandler)
for e in excelHandler.rows:
    if  e[0] != None:
        print "%s,%s,%s,%s \n" %(e[0].replace("\n", ""),e[2].replace("\n", ""),e[4].replace("\n", ""),e[13].replace("\n", ""))
