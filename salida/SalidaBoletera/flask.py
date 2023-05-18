# import packages
import PyPDF2
import re

# open the pdf file
object = PyPDF2.PdfFileReader("ag.pdf")

# get number of pages
NumPages = object.getNumPages()
print(NumPages)
# define keyterms
String = "Social"

# extract text and do the search
for i in range(0, NumPages):
    PageObj = object.getPage(i)
    print("en la pagina " + str(i)) 
    Text = PageObj.extractText() 
    print(Text)
    ResSearch = re.search(String, Text)
    print(ResSearch)
