
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pdftotext
 
Tk().withdraw() # no queremos una GUI completa, así que evita que aparezca la ventana raíz
filelocation = askopenfilename() # abre el cuadro de diálogo GUI
 
with open(filelocation, "rb") as f:  # abre el archivo en modo lectura (rb) y llámalo f
    pdf = pdftotext.PDF(f)  # almacenar una versión de texto del archivo pdf f en la variable pdf
