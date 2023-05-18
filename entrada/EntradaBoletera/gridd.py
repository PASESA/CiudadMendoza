texto = '''Lorem ipsum dolor sit amet consectetur, adipiscing elit ornare mollis feugiat natoque, tortor facilisis torquent mauris. Eleifend quis condimentum conubia auctor urna metus neque eget suspendisse, dictumst sagittis quisque gravida natoque nunc phasellus molestie tellus, donec platea dis pretium ad laoreet erat ornare. Tortor etiam varius class neque posuere eleifend mus risus donec, dis suspendisse aenean quam accumsan lectus ligula fermentum, a leo vel sociosqu pulvinar bibendum nunc sociis.
Dignissim vel massa faucibus senectus integer habitasse facilisi, consequat sem condimentum curae ut egestas lacus semper, sapien gravida platea tortor sagittis mattis. Aliquam lacus fusce ante laoreet mattis lobortis vestibulum a magnis, lectus feugiat est mi gravida dapibus tristique etiam orci nisi, rutrum pharetra elementum donec quam congue habitasse egestas. Habitasse congue torquent nascetur suscipit hendrerit sapien vivamus ante habitant senectus blandit, odio eget non etiam nibh ultricies dis nam elementum.''' 

import PyPDF2
file=open ("Reporte.pdf","rb")
reader=PyPDF2.PdfFileReader(file)
page1=reader.getPage(0)
print(reader.numPages)
pdfData=page1.extractText()
print(pdfData)
