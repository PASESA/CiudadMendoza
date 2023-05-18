from pathlib import Path
import pandas as pd
from tkinter import messagebox
from tkinter import *
from docx import Document
from fpdf import FPDF
import os
import sys

window =Tk()
window.geometry("300x400")
window.title("Export data")

data = {'Name': ['Sean','Nancy','Mary','Michael','Kevin','Frank','Joe'],
        'Age' : ['21','22','23','24','25','26','27'],
        'Gender' :['Male','Female','Female','Male','Male','Male','Male'],
        'DOB' :['11/12/1998','12/12/1994','18/03/1946','25/07/2001','29/06/1975','01/04/2015','04/11/1982']}

#Create the dataframe and tell where to get its values from
df = pd.DataFrame(data,columns=['Name','Age','Gender','DOB'])

f = open('C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/excelexport.txt', 'r')
file_contents = f.read()

for col in file_contents:
    Label(window, text = file_contents,background='white',fg='black', width=50,anchor='w').grid(row=0, column=5)



def exportexcel():
    #Create a Pandas excel writer using XLSXwriter  as the negine
    excelwriter = pd.ExcelWriter(r"C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/excelexport.xlsx")
    ######## excelwriter can only create new files, it cannot read or modify existing files #######
    ####position the dataframes in the worksheet, and names the sheet analysis ###
    df.to_excel(excelwriter,sheet_name="Analysis")
    #close the pandas excel writer and output the excel file
    excelwriter.save()
    excelwriter.close()

    messagebox.showinfo("Excel Export","Export completed")

def exporttxt():
    txtfile = open("C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/excelexport.xlsx",'w') # (w = write)
    txtfile.write(str(df))
    txtfile.close()
    messagebox.showinfo("TXT Export","Export Completed")

def exportdocx():
    document = Document()
    wordfile = open("C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/excelexport.xlsx",'r')
    for xword in wordfile:
        document.add_paragraph(xword)
    document.save("C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/docxexport.docx")
    messagebox.showinfo("DOCX Export","Export completed")

pdf = FPDF()
pdf.add_page()
pdf.set_font('arial','B',13.0)

def exportpdf():
    my_file1 = Path("C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/excelexport.txt")
    #Check no 1 verifying the file exists
    if my_file1.is_file():
        messagebox.showinfo("PDF Export","Txt file exists")
    else:
        messagebox.showinfo("PDF Export","Txt file does not exist, please check")

    #Check no 2, verifying the files are not empty

    if os.path.getsize(my_file1) > 0:
        messagebox.showinfo("PDf Export", "TXT File populated")
    else:
        print("The txt file is empty,please check abd retry")
        sys.exit()

    ## put in the code to see if the file exists already
    txtfile = open("C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/excelexport.txt", 'w') # w= write
    txtfile.write(str(df))
    txtfile.close()
    ##Opens the txt file and reads its contents to a variable and then  populates to a PDF file
    txtfile = open("C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/excelexport.txt",'r')
    for x in txtfile:
        pdf.cell(200,10,txt=x,ln=1,align='c')
    pdf.output("C:/Users/haugh/OneDrive/dataanalyticsireland/YOUTUBE/TKINTER/EXPORTING_DATA_TO_A_FILE/pdfexport.pdf")
    messagebox.showinfo("PDF Export","Export Completed")

def closescreen():
    window.destroy()

## Create button position and assign function to them

excelexp = Button(window,text="Export to excel", command=exportexcel)
excelexp.place(relx=0.2,rely=0.5,anchor=CENTER)

pdfexp = Button(window,text="Export to PDF", command=exportpdf)
pdfexp.place(relx=0.2,rely=0.6,anchor=CENTER)

exceltxt = Button(window,text="Export to txt", command=exporttxt)
exceltxt.place(relx=0.2,rely=0.7,anchor=CENTER)

exceldocx = Button(window,text="Export to docx", command=exportdocx)
exceldocx.place(relx=0.2,rely=0.8,anchor=CENTER)

closescr = Button(window, text="Close window", command=closescreen)
closescr.place(relx=0.5,rely=0.9,anchor=CENTER,width="200")

t1 = Text(window,fg='black',height=8.5,width=45)
t1.pack

class PrintTOT1(object):
    def write(self,s):
        t1.insert(END,s)

sys.stdout = PrintTOT1()

print(df)

window.mainloop()
