import itertools
from random import randint
from statistics import mean
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pymysql

############### CONFIGURAR ESTO ###################
# Open database connection
db = pymysql.connect("localhost","Aurelio","RG980320","Parqueadero1")
##################################################

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to READ a record into the database.
sql = "SELECT * FROM Entradas WHERE id > '19100'"

# Execute the SQL command
cursor.execute(sql)

# Fetch all the rows in a list of lists.
results = cursor.fetchall()
for row in results:
   id = row[0]
   placa = row[7]
   tiempo = row[4]
   # Now print fetched result
   print ("id = {0}, placa = {1}, tiempo = {2}".format(id,placa,tiempo))

# disconnect from server
db.close()


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)
def export_to_pdf(data):
	#Intervalo(self)
    c = canvas.Canvas("rojoss.pdf", pagesize=A4)
    w, h = A4
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 15
    
    xlist = [x + x_offset for x in [0, 200, 250, 300, 350, 400, 480]]
    ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]
    
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()
    
    c.save()
data = [("NOMBRE", "NOTA 1", "NOTA 2", "NOTA 3", "PROM.", "ESTADO")]
for i in range(0, 10):
for row in results:
   id = row[0]
   placa = row[7]
   tiempo = row[4]
   # Now print fetched result
   print ("id = {0}, placa = {1}, tiempo = {2}".format(id,placa,tiempo))
   data.append((f"Alumno ", *id,placa,tiempo))
# disconnect from server
db.close()

#for i in range(0, 10):#
	#results
	#exams = [(1,2,3) for _ in range(3)]
#    exams = [randint(0, 10) for _ in range(3)]
#    avg = 8#round(mean(9,8,7), 2)
    #avg = round(mean(exams), 2)
    #state = "Aprobado" 
#    state = "Aprobado" if avg >= 4 else "Desaprobado"
#    data.append((f"Alumno {i}", *exams, avg, state))
export_to_pdf(data)
