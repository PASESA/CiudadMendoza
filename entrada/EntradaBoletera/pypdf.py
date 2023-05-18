import PyPDF2
#import PyPDF2
import re

sample_pdf = open(r'ag.pdf', mode='rb')
pdfdoc = PyPDF2.PdfFileReader(sample_pdf)
print(pdfdoc.documentInfo)
print(pdfdoc.numPages)
# import packages

# open the pdf file
#object = PyPDF2.PdfFileReader("ag.pdf")

# get number of pages
NumPages = pdfdoc.getNumPages()
print(NumPages)
# define keyterms
String = "Frecuencia"

# extract text and do the search
for i in range(0, NumPages):
    PageObj = pdfdoc.getPage(i)
    print("this is page " + str(i)) 
    Text = PageObj.extractText() 
    print(Text)
    ResSearch = re.search(String, Text)
    print(ResSearch)
