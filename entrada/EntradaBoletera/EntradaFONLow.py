#programa de entrada en tenayuca
from datetime import datetime, date, time, timedelta
import random
formato = "%H:%M:%S"
from escpos.printer import *
import qrcode
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from tkinter import font 
#from tkinter import label
# para impresion con  custom
import os
#import cups
#import time, pprint, cups
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas
import re
import operacion
import time
import serial

# libreria de I/O (entradas / salidas)
import RPi.GPIO as io

# Pines
pin_sensor_autos = 4
pin_boton = 18
pin_sensor_boletos = 23

#Entrada
loop = pin_sensor_autos                      #gpio16,pin36,entrada loop                    
boton = pin_boton                     #gpio12,pin32,entrada boton
SenBoleto = pin_sensor_boletos                 #gpio20,pin38,sensor boleto

#salidas
barrera = 13                  #gpio13,pin33,Salida barrera
out1 = 19                     #gpio19,pin35,Salida indicador loop
out2 = 6                     #gpio6,pin31,Salida indicador boton
out3 = 26                     #gpio26,pin37,Salida indicador barrera
io.setmode(io.BCM)              # modo in/out pin del micro
io.setwarnings(False)           # no señala advertencias de pin ya usados
io.setup(loop,io.IN)             # configura en el micro las entradas
io.setup(boton,io.IN)             # configura en el micro las entradas
# io.setup(SenBoleto,io.IN)             # configura en el micro las entradas
io.setup(barrera,io.OUT)           # configura en el micro las salidas
io.setup(out1,io.OUT)           # configura en el micro las salidas
io.setup(out2,io.OUT)
io.setup(out3,io.OUT)  
line=''
io.output(barrera,0)
io.output(out1,0)
io.output(out2,0)
io.output(out3,0)
BanLoop =0
BanBoton=0
# BanSenBoleto=0
BanImpresion=0 #No ha impreso
# Configuracion de las entradas y las salidas del micro
# -----------------------------------------------------
class FormularioOperacion:
    def __init__(self):
        #creamos un objeto que esta en el archivo operacion dentro la clase Operacion
        self.operacion1=operacion.Operacion()
        self.ventana1=tk.Tk()
        self.ventana1.title("BOLETERA DE ENTRADA")
        self.ventana1.configure(bg = 'blue')
        self.cuaderno1 = ttk.Notebook(self.ventana1)
        self.cuaderno1.config(cursor="")         # Tipo de cursor
        self.ExpedirRfid()
        self.consulta_por_folio()
        self.check_inputs()
        #self.botonpImprimir()
        #self.calcular_cambio()
        self.IntBoton()
        self.Intloop()
        self.listado_completo()
        self.cuaderno1.grid(column=0, row=0, padx=5, pady=5)
        self.ventana1.mainloop()
    ###########################Inicia Pagina1##########################
# Funcion de lectura de las entradas
# -----------------------------------
    def ExpedirRfid(self):    
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text="Expedir Boleto")
        #enmarca los controles LabelFrame
        self.labelframe1=ttk.LabelFrame(self.pagina1, text=" ")
        self.labelframe1.grid(column=0, row=0, padx=0, pady=0)
        self.Adentroframe=ttk.LabelFrame(self.pagina1, text=" ")
        self.Adentroframe.grid(column=1, row=0, padx=0, pady=0)
        self.MaxId=tk.StringVar()
        self.entryMaxId=ttk.Entry(self.labelframe1, width=10, textvariable=self.MaxId, state="readonly")
        self.entryMaxId.grid(column=1, row=0, padx=4, pady=4)
        #self.lbltitulo=ttk.Label(self.labelframe1, text="FOLIO")
        #self.lbltitulo.grid(column=0, row=0, padx=0, pady=0)
        #self.presenciaAuto = ttk.Label(self.labelframe1, text="TIPO DE ENTRADA", width = 17)#, background = '#CCC')
        #self.presenciaAuto.grid(column=0, row=6, padx=0, pady=0)
        self.Bienvenida = ttk.Label(self.Adentroframe, text="BIENVENIDOS", width = 20, font=('Arial', 30))#, background = '#FD6')
        #self.Bienvenida.config(font=('Arial', 40))
        self.Bienvenida.grid(column=2, row=2, padx=0, pady=0)
        self.SenBol2 = ttk.Label(self.Adentroframe, text=".", width = 20, font=('Arial', 15))#, background = '#CCC') , background = 'green'
        self.SenBol2.grid(column=1, row=12, padx=0, pady=0)
        self.loopDet = ttk.Label(self.Adentroframe, text="1) OPRIMA EL BOTON ", width = 20, font=('Arial', 15), background = '#CCC') #, background = '#FD6')
        self.loopDet.grid(column=1, row=8, padx=0, pady=0)
        self.BotDet = ttk.Label(self.Adentroframe, text="Boton", width = 20, font=('Arial', 15), background = '#CCC')#, background = '#CCC')
        self.BotDet.grid(column=1, row=6, padx=0, pady=0)
        self.SenBol = ttk.Label(self.Adentroframe, text=".", width = 20, font=('Arial', 15))#, background = '#CCC') , background = 'green'
        self.SenBol.grid(column=1, row=10, padx=0, pady=0)
        
        #self.Reloj = ttk.Label(self.pagina1, text="Hora y fecha", width = 10, background = '#FD6')
        #self.Reloj.grid(column=0, row=6, padx=0, pady=0)

        self.Reloj = ttk.Label(self.pagina1, text="Reloj") #Creación del Label
        self.Reloj.config(width =10)
        self.Reloj.config(background="white") #Cambiar color de fondo
        self.Reloj.config(font=('Arial', 60)) #Cambiar tipo y tamaño de fuente 80
        self.Reloj.grid(column=1, row=12, padx=0, pady=0)  #4 
        
        self.mi_reloj = ttk.Label(self.pagina1, text="Reloj") #Creación del Label
        self.mi_reloj.config(width =10)
        self.mi_reloj.config(background="white") #Cambiar color de fondo
        self.mi_reloj.config(font=('Arial', 60)) #Cambiar tipo y tamaño de fuente 80
        self.mi_reloj.grid(column=1, row=14, padx=0, pady=0)       #6 
        self.boton2=tk.Button(self.pagina1, text="Salir del programa", command=quit, width=15, height=1, anchor="center", background="blue")
        self.boton2.grid(column=1, row=16, padx=4, pady=4)  
        #####tomar placas del auto
        self.Placa=tk.StringVar()
        self.entryPlaca=tk.Entry(self.labelframe1, width=15, textvariable=self.Placa)
        self.entryPlaca.grid(column=1, row=1, padx=4, pady=4)
        #self.lblPlaca=ttk.Label(self.labelframe1, text="COLOCAR PLACAS")
        #self.lblPlaca.grid(column=0, row=1, padx=0, pady=0)

        #self.labelhr=ttk.Label(self.labelframe1, text="HORA ENTRADA")
        #self.labelhr.grid(column=0, row=2, padx=0, pady=0)

        #self.scrolledtext=st.ScrolledText(self.Adentroframe, width=20, height=3)
        #self.scrolledtext.grid(column=1,row=0, padx=4, pady=4)
        #self.Autdentro=tk.Button(self.Adentroframe, text="Boletos sin Cobro", command=self.Autdentro, width=15, height=1, anchor="center")
        #self.Autdentro.grid(column=2, row=0, padx=4, pady=4)
        #self.labeRFID=ttk.Label(self.Adentroframe, text="LECTURA RFID")
        #self.labeRFID.grid(column=1, row=3, padx=0, pady=0)
        #self.RFID=tk.StringVar()
        #self.entryRFID=tk.Entry(self.Adentroframe, width=20, textvariable=self.RFID)
        #self.entryRFID.grid(column=1, row=1, padx=4, pady=4)
        #self.botonPent=tk.Button(self.Adentroframe, text="DeclararlaEnt", command= self.check_inputs, width=15, height=1, anchor="center")
        #self.botonPent.grid(column=2, row=1, padx=4, pady=4)            
 
        self.boton1=tk.Button(self.labelframe1, text="Generar Entrada", command=self.agregarRegistroRFID, width=13, height=3, anchor="center", background="blue")
        self.boton1.grid(column=1, row=4, padx=4, pady=4)

        ###Pensionados
        self.labelframe3=ttk.LabelFrame(self.pagina1, text="PENSIONADOS")
        self.labelframe3.grid(column=1, row=2, padx=0, pady=0)        
        self.labelTarjeta=ttk.Label(self.labelframe3, text="Tarjeta:")
        self.labelTarjeta.grid(column=0, row=2, padx=0, pady=0)
        self.NumTarjeta4=tk.StringVar()
        self.entryNumTarjeta4=tk.Entry(self.labelframe3, width=20, textvariable=self.NumTarjeta4)
        #self.entryNumTarjeta4.bind('Return', self.Pensionados)
        self.entryNumTarjeta4.grid(column=1, row=2, padx=4, pady=4)
        self.entryNumTarjeta4.focus()
        self.labelMensaje=ttk.Label(self.labelframe3, text="")
        self.labelMensaje.grid(column=2, row=2, padx=0, pady=0)

        #self.botonPensinados=tk.Button(self.labelframe3, text="Entrada", command=self.Pensionados, width=10, height=1, anchor="center")
        #self.botonPensinados.grid(column=2, row=2, padx=4, pady=4)  
    # def SenBoleto(self): #Detecta presencia de automovil
    #     global BanSenBoleto
    #     if io.input(SenBoleto):
                 
    #             io.output(out3,1)#con un "1" se apaga el led
    #             #self.loopDet.config(text = "Inicio", background = '#CCC')                
    #             BanSenBoleto = 1
    #             print('siente boleto '+str(BanSenBoleto))
    #             #self.check_inputs()
    #     else:                
                 
    #             io.output(out3,0)                              
    #             #self.loopDet.config(text = "Auto", background = 'red')
    #             BanSenBoleto = 0
    #             print('No siente boleto '+str(BanSenBoleto))
    #             #self.check_inputs()

    def Intloop(self): #Detecta presencia de automovil
        global BanLoop
        if io.input(loop):
                print('hay auto') 
                io.output(out1,1)#con un "1" se apaga el led
                #self.loopDet.config(text = "Inicio", background = '#CCC')                
                BanLoop = 1
                #self.check_inputs()
        else:                
                #print('No hay auto') 
                io.output(out1,0)                              
                #self.loopDet.config(text = "Auto", background = 'red')
                BanLoop = 0
                #self.check_inputs()
    def IntBoton(self): #Detecta presencia de automovil
        global BanBoton
        if io.input(boton):
                        #self.BotDet.config(text = "Presione Boton",background="#CCC")
                        print('Presiono boton')
                        io.output(out2,1)
                        BanBoton = 1
        else:
                        #print('Solto boton')            
                        io.output(out2,0)
                        #self.BotDet.config(text = "Imprimiendo",background="red")
                        BanBoton = 0
                        #self.agregarRegistroRFID()
    io.add_event_detect(loop, io.BOTH, callback = Intloop)
 
    io.add_event_detect(boton, io.BOTH, callback = IntBoton)
    
    # io.add_event_detect(pin_sensor_boletos, io.BOTH, callback = SenBoleto)


    def check_inputs(self):
        global BanBoton
        global BanLoop
        global BanImpresion
    
        if BanLoop == 1:
                self.loopDet.config(text = "OPRIMA BOTON", font=('Arial', 15), background = 'green')
                tarjeta=str(self.entryNumTarjeta4.get(),)
                if len(tarjeta) == 10:
                    #mb.showwarning("IMPORTANTE", "ENTRO")
                    self.Pensionados(self)
        else:
                self.loopDet.config(text = ".", font=('Arial', 15), background = '#CCC') #'#CCC'
                self.SenBol2.config(text = ".", font=('Arial', 15), background='#CCC')
                self.SenBol.config(text = ".", font=('Arial', 15), background='#CCC')
                self.labelMensaje.config(text= "Sin Tarjeta para acceder")
                self.NumTarjeta4.set("")               
                self.entryNumTarjeta4.focus()
               
        if (BanBoton == 0):#BanBoton == 1 no esta oprimido el boton
            self.BotDet.config(text = ".", font=('Arial', 15), background='#CCC') #'#CCC'
            #print(str(BanSenBoleto))
            if BanImpresion == 1:# and BanSenBoleto == 0:# mando a imprimir y ya no tiene boleto en la boquilla
                self.SenBol.config(text = "AVANCE", font=('Arial', 15), background= "green") #'#CCC'
                self.SenBol2.config(text = ".", font=('Arial', 15), background='#CCC') #Se desactiva Sensor Boleto y abre barrera  
                # print("En BanSenBoleto="+str(BanSenBoleto))
                #io.output(out3,1)#con un "1" se apaga el led
                io.output(barrera,1)#con un "0" abre la barrera
                time.sleep (1)
                io.output(barrera,0)
                BanImpresion = 0
                
                print('mando abrir barrera')
                                    #io.output(out2,1)
        else:    
                self.SenBol.config(text = "TOMAR BOLETO ", font=('Arial', 15), background="green")
                # print("BanSenBoleto ",str(BanSenBoleto))
                print("BanImpresion ",str(BanImpresion))
                print("BamLoop ",str(BanLoop))
                if BanLoop==1 and BanImpresion == 0:
                    #io.output(out2,0)             
                   print('imprimir')
                   #print(str(BanSenBoleto))
                   self.agregarRegistroRFID()
                   BanImpresion = 1
                #    if BanSenBoleto == 1:
                #       self.SenBol2.config(text = "Sensor Boleto", font=('Arial', 15), background="green") ##Se activa Sensor Boleto   
                #       print("En BanSenBoleto= 1 "+str(BanSenBoleto))
                #       # self.SenBol.config(text = "No siente boleto ")
                #       # io.output(out3,1)#con un "1" se apaga el led
                #        #io.output(barrera,0)#con un "0" abre la barrera
                #        #time.sleep (1)
                #        #io.output(barrera,1)
                #    else:                   
                #       self.SenBol.config(text = ".", font=('Arial', 15), background='#CCC')
                
                else:
                   print ('no puede imprimir ')
                   #print(str(BanSenBoleto))
                   if BanLoop == 1:
                        pass
                        # self.BotDet.config(text = "Boleto Impreso",background="orange")
                   else:
                        self.BotDet.config(text = "No hay Auto",background="orange")

        now =datetime.now() 
        fecha1= now.strftime("%d-%b-%y")
        hora1= now.strftime("%H:%M:%S")    
        self.Reloj.config(text=fecha1)            
        self.mi_reloj.config(text=hora1)    
        self.ventana1.after(60, self.check_inputs)          # activa un timer de 50mSeg.
   
    def Autdentro(self):
        respuesta=self.operacion1.Autos_dentro()
        self.scrolledtext.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtext.insert(tk.END, "Entrada num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\n\n")
     
    def agregarRegistroRFID(self):
        placa=self.Placa.get()
        
        MaxFolio=self.operacion1.MaxfolioEntrada()
        folio_boleto = int(MaxFolio) + 1
        self.MaxId.set(folio_boleto)

        folio_cifrado = self.cifrar_folio(folio = folio_boleto)
        # print(f"QR entrada: {folio_cifrado}")  

        #Generar QR
        self.generar_QR(folio_cifrado)

        fechaEntro = datetime.today()

        horaentrada = str(fechaEntro)
        horaentrada=horaentrada[:19]
        # self.labelhr.configure(text=(horaentrada[:-3], "Entro"))
        corteNum = 0
        datos=(fechaEntro, corteNum, placa)

        printer = Usb(0x04b8, 0x0e28, 0)

        printer.image("LOGO1.jpg")
        printer.text("--------------------------------------\n")
        printer.set(align="center")
        printer.text("BOLETO DE ENTRADA\n")
        printer.text('Entro: '+horaentrada[:-3]+'\n')
        printer.text('Placas '+placa+'\n')
        printer.text(f'Folio 000{folio_boleto}\n')

        printer.set(align = "center")
        printer.image("reducida.png")

        printer.text("--------------------------------------\n")
        printer.cut()

        printer.close()

        self.operacion1.altaRegistroRFID(datos)
        self.Placa.set('')

    def Pensionados(self,event):
        numtarjeta=str(self.NumTarjeta4.get(), )
        tarjeta=int(numtarjeta)
        print(tarjeta)
        Existe=self.operacion1.ValidarPen(tarjeta)
        #mb.showwarning("IMPORTANTE", str(Existe))
        if len(Existe) == 0 :
            #mb.showwarning("IMPORTANTE", "No existe Pensionado para ese Num de Tarjeta")
            self.labelMensaje.config(text= "No existe Pensionado"+ str(Existe)+str(tarjeta))
            self.NumTarjeta4.set("")               
            self.entryNumTarjeta4.focus()
            return False
        else:        
            respuesta=self.operacion1.ConsultaPensionado(Existe)
            #Fecha_vigencia, Estatus, Vigencia
            for fila in respuesta:                
                VigAct=fila[0]
                Estatus=fila[1]
                Vigencia =fila[2]
                Tolerancia=int(fila[3])
                #print("Tolerancia: ",str(Tolerancia))
                if Estatus == 'Adentro' :
                    self.labelMensaje.config(text= "Ya está Adentro")
                    #mb.showwarning("IMPORTANTE", "NO PUEDE ACCEDER: Ya existe un auto adentro registrado")
                    self.NumTarjeta4.set("")               
                    self.entryNumTarjeta4.focus()
                    return False
                elif VigAct == 'Inactiva' :
                    self.labelMensaje.config(text= "Sin Vigencia Activa")
                    #mb.showwarning("IMPORTANTE", "SIN VIGENCIA ACTIVA: Pensionado sin pago, favor de realizar pago")
                    self.NumTarjeta4.set("")               
                    self.entryNumTarjeta4.focus()
                    return False                        
                elif VigAct <= datetime.today()+timedelta(days = Tolerancia):
                    datos1=('Afuera','VENCIDA', Existe)
                    self.labelMensaje.config(text= "Vigencia VENCIDA")
                    self.operacion1.UpdPensionado(datos1)
                    #mb.showwarning("IMPORTANTE", "NO PUEDE ACCEDER: La Vigencia esta vencida")
                    self.NumTarjeta4.set("")               
                    self.entryNumTarjeta4.focus()
                    return False
                else:
                    Entrada=datetime.today()
                    datos=(Existe, tarjeta, Entrada, 'Adentro')
                    datos1=('Adentro', Vigencia, Existe)
                    #mb.showinfo("Pago de Pension",'BIENVENIDO')
                    #sql="INSERT INTO PagosPens(id_cliente, num_tarjeta, Fecha_pago, Fecha_vigencia, Mensualidad, Monto) values (%s,%s,%s,%s,%s,%s)"
                    self.operacion1.MovsPensionado(datos)
                    self.operacion1.UpdPensionado(datos1)
                    self.NumTarjeta4.set("")               
                    self.entryNumTarjeta4.focus()
                    #io.output(out3,1)#con un "1" se apaga el led
                    io.output(barrera,1)#con un "0" abre la barrera
                    time.sleep (1)
                    io.output(barrera,0)
                    #io.output(out3,1)#con un "1" se apaga el led
                    self.NumTarjeta4.set("")               
                    self.entryNumTarjeta4.focus()
                


#########################fin de pagina1 inicio pagina2#########################
    def consulta_por_folio(self):
        self.pagina2 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina2, text=" NO SE COBRA NORMALMENTE AQUI")
        #en el frame
        self.labelframe2=ttk.LabelFrame(self.pagina2, text="Autos")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)
        self.label1=ttk.Label(self.labelframe2, text="Lector QR")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.label3=ttk.Label(self.labelframe2, text="Entro:")
        self.label3.grid(column=0, row=1, padx=4, pady=4)
        self.label4=ttk.Label(self.labelframe2, text="Salio:")
        self.label4.grid(column=0, row=2, padx=4, pady=4)
        #en otro frame
        self.labelframe3=ttk.LabelFrame(self.pagina2, text="Datos del COBRO")
        self.labelframe3.grid(column=1, row=0, padx=5, pady=10)
        self.lbl1=ttk.Label(self.labelframe3, text="Hr Salida")
        self.lbl1.grid(column=0, row=1, padx=4, pady=4)
        self.lbl2=ttk.Label(self.labelframe3, text="TiempoTotal")
        self.lbl2.grid(column=0, row=2, padx=4, pady=4)
        self.lbl3=ttk.Label(self.labelframe3, text="Importe")
        self.lbl3.grid(column=0, row=3, padx=4, pady=4)

        self.labelPerdido=ttk.LabelFrame(self.pagina2, text="Perdido")
        self.labelPerdido.grid(column=2,row=1,padx=5, pady=10)
        self.lblFOLIO=ttk.Label(self.labelPerdido, text=" FOLIO PERDIDO")
        self.lblFOLIO.grid(column=0, row=1, padx=4, pady=4)
        self.PonerFOLIO=tk.StringVar()
        self.entryPonerFOLIO=tk.Entry(self.labelPerdido, width=15, textvariable=self.PonerFOLIO)
        self.entryPonerFOLIO.grid(column=1, row=1)
        self.boton2=tk.Button(self.labelPerdido, text="B./SIN cobro", command=self.BoletoDentro, width=10, height=2, anchor="center")
        self.boton2.grid(column=0, row=0)
        self.boton3=tk.Button(self.labelPerdido, text="Boleto Perdido", command=self.BoletoPerdido, width=10, height=2, anchor="center")
        self.boton3.grid(column=0, row=2)
        self.scrolledtxt=st.ScrolledText(self.labelPerdido, width=28, height=7)
        self.scrolledtxt.grid(column=1,row=0, padx=10, pady=10)
        self.labelpromo=ttk.LabelFrame(self.pagina2, text="Promociones")
        self.labelpromo.grid(column=2, row=0, padx=5, pady=10)
        self.promolbl=ttk.Label(self.labelpromo, text="Leer el  QR de Promocion")
        self.promolbl.grid(column=0, row=0, padx=4, pady=4)
        self.promolbl1=ttk.Label(self.labelpromo, text="Codigo QR")
        self.promolbl1.grid(column=0, row=1, padx=4, pady=4)
        self.promolbl2=ttk.Label(self.labelpromo, text="Tipo Prom")
        self.promolbl2.grid(column=0, row=2, padx=4, pady=4)
        self.labelcuantopagas=ttk.LabelFrame(self.pagina2, text='cual es el pago')
        self.labelcuantopagas.grid(column=0,row=1, padx=5, pady=10)
        self.cuantopagas=ttk.Label(self.labelcuantopagas, text="la cantidad entregada")
        self.cuantopagas.grid(column=0, row=0, padx=4, pady=4)
        self.importees=ttk.Label(self.labelcuantopagas, text="el importe es")
        self.importees.grid(column=0, row=1, padx=4, pady=4)
        self.cambio=ttk.Label(self.labelcuantopagas, text="el cambio es")
        self.cambio.grid(column=0, row=2, padx=4, pady=4)
        self.cuantopagasen=tk.StringVar()
        self.entrycuantopagasen=tk.Entry(self.labelcuantopagas, width=15, textvariable=self.cuantopagasen)
        #self.entrycuantopagasen.bind('<Return>',self.calcular_cambio)
        self.entrycuantopagasen.grid(column=1, row=0)
        self.elimportees=tk.StringVar()
        self.entryelimportees=tk.Entry(self.labelcuantopagas, width=15, textvariable=self.elimportees, state="readonly")
        self.entryelimportees.grid(column=1, row=1)
        self.elcambioes=tk.StringVar()
        self.entryelcambioes=tk.Entry(self.labelcuantopagas, width=15, textvariable=self.elcambioes, state="readonly")
        self.entryelcambioes.grid(column=1, row=2)
        self.label11=ttk.Label(self.labelframe3, text="DIAS")
        self.label11.grid(column=1, row=4, padx=1, pady=1)
        self.label12=ttk.Label(self.labelframe3, text="HORAS")
        self.label12.grid(column=1, row=5, padx=1, pady=1)
        self.label7=ttk.Label(self.labelframe3, text="MINUTOS")
        self.label7.grid(column=1, row=6, padx=1, pady=1)
        self.label8=ttk.Label(self.labelframe3, text="SEGUNDOS")
        self.label8.grid(column=1, row=7, padx=1, pady=1)
        self.label9=ttk.Label(self.labelframe3, text="TOTAL COBRO")
        self.label9.grid(column=1, row=8, padx=1, pady=1)
        self.label15=ttk.Label(self.pagina2, text="Viabilidad de COBRO")
        self.label15.grid(column=1, row=2, padx=0, pady=0)
        #se crea objeto para ver pedir el folio la etiqueta con texto
        self.folio=tk.StringVar()
        self.entryfolio=tk.Entry(self.labelframe2, textvariable=self.folio)
        self.entryfolio.bind('<Return>',self.consultar)#con esto se lee automatico y se va a consultar
        self.entryfolio.grid(column=1, row=0, padx=4, pady=4)
        #se crea objeto para mostrar el dato de la  Entrada solo lectura
        self.descripcion=tk.StringVar()
        self.entrydescripcion=ttk.Entry(self.labelframe2, textvariable=self.descripcion, state="readonly")
        self.entrydescripcion.grid(column=1, row=1, padx=4, pady=4)
        #se crea objeto para mostrar el dato la Salida solo lectura
        self.precio=tk.StringVar()
        self.entryprecio=ttk.Entry(self.labelframe2, textvariable=self.precio, state="readonly")
        self.entryprecio.grid(column=1, row=2, padx=4, pady=4)
        #se crea objeto para MOSTRAR LA HORA DEL CALCULO
        self.copia=tk.StringVar()
        self.entrycopia=tk.Entry(self.labelframe3, width=20, textvariable=self.copia, state = "readonly")
        self.entrycopia.grid(column=1, row=1)
        #SE CREA UN OBJETO caja de texto IGUAL A LOS DEMAS Y MUESTRA EL TOTAL DEL TIEMPO
        self.ffeecha=tk.StringVar()
        self.entryffeecha=tk.Entry(self.labelframe3, width=20, textvariable=self.ffeecha, state= "readonly")
        self.entryffeecha.grid(column=1, row=2)
        #SE CREA UN OBJETO caja de texto IGUAL A LOS DEMAS para mostrar el importe y llevarlo a guardar en BD
        self.importe=tk.StringVar()
        self.entryimporte=tk.Entry(self.labelframe3, width=20, textvariable=self.importe, state= "readonly")
        self.entryimporte.grid(column=1, row=3)
        #creamos un objeto para obtener la lectura de la PROMOCION
        self.promo=tk.StringVar()
        self.entrypromo=tk.Entry(self.labelpromo, width=20, textvariable=self.promo)
        self.entrypromo.grid(column=1, row=1)
        #este es donde pongo el tipo de PROMOCION
        self.PrTi=tk.StringVar()
        self.entryPrTi=tk.Entry(self.labelpromo, width=20, textvariable=self.PrTi, state= "readonly")
        self.entryPrTi.grid(column=1, row=2)
        #botones
        #self.boton1=tk.Button(self.labelframe2, text="Consultar", command=self.consultar, width=20, height=5, anchor="center")
        #self.boton1.grid(column=1, row=4)
        self.boton2=tk.Button(self.labelpromo, text="PROMOCION", command=self.CalculaPromocion, width=20, height=5, anchor="center")
        self.boton2.grid(column=1, row=4)
        #self.boton3=tk.Button(self.pagina2, text="COBRAR ", command=self.GuardarCobro, width=20, height=5, anchor="center", background="Cadetblue")
        #self.boton3.grid(column=1, row=1)
        #self.boton4=tk.Button(self.labelframe3, text="IMPRIMIR", command=self.Comprobante, width=10, height=2, anchor="center", background="Cadetblue")
        #self.boton4.grid(column=0, row=4)
        self.bcambio=tk.Button(self.labelcuantopagas, text="cambio", command=self.calcular_cambio, width=10, height=2, anchor="center", background="blue")
        self.bcambio.grid(column=0, row=4)
    def BoletoDentro(self):
        respuesta=self.operacion1.Autos_dentro()
        self.scrolledtxt.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtxt.insert(tk.END, "Folio num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nPlacas: "+str(fila[2])+"\n\n")
    def BoletoPerdido(self):
       datos=str(self.PonerFOLIO.get(), )
       datos=int(datos)
       datos=str(datos)
       self.folio.set(datos)
       datos=(self.folio.get(), )
       respuesta=self.operacion1.consulta(datos)
       if len(respuesta)>0:
           self.descripcion.set(respuesta[0][0])
           self.precio.set(respuesta[0][1])
           self.CalculaPermanencia()#nos vamos a la funcion de calcular permanencia
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2
            #self.label11.configure(text=(ffeecha.days, "dias"))
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
        #    self.label12.configure(text=(horas_dentro, "horas"))
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if horas_dentro <= 24:
                importe = 200
           if horas_dentro > 24 or ffeecha.days >= 1:
                importe = 200+((ffeecha.days)*720 + (horas_dentro * 30))
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("Per")
           self.Comprobante()
           #p = Usb(0x04b8, 0x0202, 0)
           p = Usb(0x04b8, 0x0e28, 0)#esta es la impresora con sus valores que se obtienen con lsusb
           p.text('Boleto Perdido\n')
           FoliodelPerdido = str(self.PonerFOLIO.get(),)
           p.text('Folio boleto cancelado: '+FoliodelPerdido+'\n')
           fecha = datetime.today()
           fechaNota = datetime.today()
           fechaNota= fechaNota.strftime("%b-%d-%A-%Y %H:%M:%S")
           horaNota = str(fechaNota)
           p.set(align="left")
           p.set('Big line\n', font='b')
           p.text('Fecha: '+horaNota+'\n')
           EntradaCompro = str(self.descripcion.get(),)
           p.text('El auto entro: '+EntradaCompro+'\n')
           SalioCompro = str(self.copia.get(),)
           p.text('El auto salio: '+SalioCompro+'\n')
           self.GuardarCobro()
           self.PonerFOLIO.set("")
           p.cut()
           self.promo.set("")
           self.PonerFOLIO.set("")
           #p = Usb(0x04b8, 0x0e15, 0)#esta es la impresora con sus valores que se obtienen con lsusb
           #p.text('Entrega de Automovil Boleto Perdido\n')
           #p.text('Original Empresa\n')
           #p.image("LOGO.jpg")
           #p.set(align="center")
           #p.set('Big line\n', font='b')
           #p.text('PASE, S.A. DE C.V. R.F.C.PAS-780209-I24\n')
           #p.text('P.De la Reforma no 300-05\n')
           #p.text('Col. Juarez Deleg. Cuauhtemoc\n')
           #p.text('C.P. 06600, CDMX, TEL 5525-0108\n')
           #p.text('SUCURSAL Durango No.205 Col.Roma Norte\n')
           #p.text('Alcaldia Cuauhtemoc C.P. 06700,CDMX\n')
           #fecha = datetime.today()
           #fechaNota = datetime.today()
           #fechaNota= fechaNota.strftime("%b-%d-%A-%Y %H:%M:%S")
           #horaNota = str(fechaNota)
           #p.set(align="left")
           #p.set('Big line\n', font='b')
           #p.text('Fecha: '+horaNota+'\n')
           #p.text('__________________________________________________________\n')
           #p.text('Nombre del cliente:\n')
           #p.text('                   _______________________________________\n')
           #p.text('Direccion:\n')
           #p.text('                   _______________________________________\n')
           #p.text('Tel:\n')
           #p.text('                   _______________________________________\n')
           #p.text('Licencia no.:               Lugar:\n')
           #p.text('             _______________      ________________________\n')
           #p.text('Marca:         Modelo:             Color:        Placas:\n')
           #p.text('\n')
           #p.text('_____________  __________        __________   ____________\n')
           #p.text('Registrado a nombre de:\n')
           #p.text('                   _______________________________________\n')
           #p.text('El auto lo recibio:\n')
           #p.text('                   _______________________________________\n')
           #EntradaCompro = str(self.descripcion.get(),)
           #p.text('El auto entro: '+EntradaCompro+'\n')
           #SalioCompro = str(self.copia.get(),)
           #p.text('El auto salio: '+SalioCompro+'\n')
           #p.cut()

       else:
           self.descripcion.set('')
           self.precio.set('')
           mb.showinfo("Información", "No existe un auto con dicho código")
    def consultar(self,event):
        self.descripcion.set('')
        self.precio.set('')
        datos=str(self.folio.get(), )
        #print(len(datos))
        print(datos)
        #mb.showwarning(datos)
        if len(datos) > 20:#con esto revisamos si lee el folio o la promocion
            datos=datos[26:]
            datos=int(datos)
            datos=str(datos)
            print(datos)
            self.folio.set(datos)
            datos=(self.folio.get(), )
            respuesta=self.operacion1.consulta(datos)
            if len(respuesta)>0:
                #self.descripcion.set(respuesta[0][0])
                #self.precio.set(respuesta[0][1])
                #self.CalculaPermanencia()#nos vamos a la funcion de calcular permanencia
                fechaActual = datetime.today()
                fechaActual = datetime.strftime(fechaActual,'%Y-%m-%d %H:%M:%S' ) 
                fecha_salida = respuesta[0][1]      
                fecha_salida = datetime.strftime(fecha_salida,'%Y-%m-%d %H:%M:%S' )
                tolerancia = fechaActual - fecha_salida
                #segundos_vividos = ffeecha.seconds
                tolerancia_segundos = tolerancia.seconds
                #minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
                tolerancia_minutos, tolerancia_segundos = divmod(tolerancia_segundos, 60)    
                if tolerancia_minutos < 15 and tolerancia_minutos >= 0:
                   ###Abrimos Barrera
                   print("Abre Barrera")
                   #io.output(barrera,1)#abre la barrera
                   #time.sleep (1)
                   #io.output(barrera,0)
                   #self.descripcion.set(respuesta[0][0])
                   #self.precio.set(respuesta[0][1])
                   #self.CalculaPermanencia()#nos vamos a la funcion de calcular permanencia
                   self.descripcion.set('')
                   self.precio.set('')
                else:
                   print("Boleto Vencido")
                   ### Label con mensaje de Tolerancia Vencida
                   self.descripcion.set('Boleto Vencido')
                   self.precio.set('')
                   self.folio.set("")
                   self.entryfolio.focus()
                   #mb.showinfo("Información", "No existe un auto con dicho código")                               
            else:
                self.descripcion.set('No existe un auto con dicho código')
                self.precio.set('')
                self.folio.set("")
                self.entryfolio.focus()
                #mb.showinfo("Información", "No existe un auto con dicho código")
            #####Validamos QR para Salida con Tolerncia de 15 minutos para Orizaba.    
        elif len(tarjeta) == 10:
            self.PensionadosOut(self)        
        else:
            #mb.showinfo("Promocion", "leer primero el folio")
            self.folio.set("")
            self.entryfolio.focus()

    def PensionadosOut(self,event):
        numtarjeta=str(self.folio.get(), )
        tarjeta=int(numtarjeta)
        print(tarjeta)
        Existe=self.operacion1.ValidarPen(tarjeta)
        #mb.showwarning("IMPORTANTE", str(Existe))
        if len(Existe) == 0 :
            #mb.showwarning("IMPORTANTE", "No existe Pensionado para ese Num de Tarjeta")
            self.descripcion.set('No existe Pensionado')
            self.folio.set("")
            self.entryfolio.focus()
        else:        
            respuesta=self.operacion1.ConsultaPensionado(Existe)
            #Fecha_vigencia, Estatus, Vigencia
            for fila in respuesta:
                VigAct=fila[0]
                Estatus=fila[1]
                if Estatus == None:
                    self.descripcion.set('Pensionado sin registro de Entrada')
                    self.folio.set("")
                    self.entryfolio.focus()
                    return False               
                elif Estatus == 'Afuera' :
                    self.descripcion.set('Ese Pensionado ya salio')
                    self.folio.set("")
                    self.entryfolio.focus()
                    return False
                elif VigAct == None :
                    self.descripcion.set('Sin Vigencia Activa')
                    self.folio.set("")
                    self.entryfolio.focus()
                    return False                                               
                elif VigAct <= datetime.today()+timedelta(days = 5):
                    self.descripcion.set('Vigencia Vencida')
                    self.folio.set("")
                    self.entryfolio.focus()
                    return False                                                       
                else:
                    Salida=datetime.today()
                    datos=(Salida, 'Afuera', Existe)
                    datos1=('Afuera', Existe)                       
                    self.operacion1.UpdMovsPens(datos)
                    self.operacion1.UpdPens2(datos1)
                    self.folio.set("")
                    self.entryfolio.focus()
                    #io.output(barrera,1)#abre la barrera
                    #time.sleep (1)
                    #io.output(barrera,0)
                         
            
    def CalculaPermanencia(self):# funcion que  CALCULA LA PERMANENCIA DEL FOLIO SELECCIONADO
        salida = str(self.precio.get(), )#deveria ser salida en lugar de precio pero asi estaba el base

        if len(salida)>5:#None tiene 4 letras si es mayor a 5 es que tiene ya la fecha
            self.label15.configure(text=("Este Boleto ya Tiene cobro"))
            self.elcambioes.set("")
            self.elimportees.set("")
            self.cuantopagasen.set("")
            self.descripcion.set('')
            self.precio.set('')
            self.copia.set("")
            self.importe.set("")
            self.ffeecha.set("")
            self.folio.set("")
            self.label7.configure(text=(""))
            self.label8.configure(text =(""))
            self.label9.configure(text =(""))
#            self.label10.configure(text=(""))
            self.label11.configure(text=(""))
            self.label12.configure(text=(""))
           # self.elimportees.configure(text=(""))
            self.entryfolio.focus()
        else:
            self.PrTi.set("Normal")    
            self.label15.configure(text="Lo puedes COBRAR")
            fecha = datetime.today()
            fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
            fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
            self.copia.set(fechaActual)
            date_time_str=str(self.descripcion.get())
            date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
            date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
            ffeecha = fechaActual - date_time_mod2
            self.label11.configure(text=(ffeecha.days, "dias"))
            segundos_vividos = ffeecha.seconds
            horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
            self.label12.configure(text=(horas_dentro, "horas"))
            minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
            self.label7.configure(text=(minutos_dentro, "minutos"))
            #calcular la diferencia de segundos
            seg1 = ffeecha.seconds
            #print ("dif = seg1 = ", seg1)
            seg2 = ffeecha.seconds/60
            #print ("dif/60 = seg2 = ", seg2)
            seg3 = int(seg2)
            #print ("entero y redondear seg3 = ", seg3)
            seg4 = seg2-seg3
            #print ("seg2 - seg 3 = seg4 = ", seg4)
            seg5 = seg4*60
            #print ("seg5 =", seg5)
            seg6 = round(seg5)
            #print  ("segundos dentro ===> ", seg6)
            self.label8.configure(text =(seg6, "segundos"))
            #self.label9.configure(text =(ffeecha, "tiempo dentro"))
            self.ffeecha.set(ffeecha)
            if minutos_dentro < 15 and minutos_dentro  >= 0:
                minutos = 1
            if minutos_dentro < 30 and minutos_dentro  >= 15:
                minutos = 2
            if minutos_dentro < 45 and minutos_dentro  >= 30:
                minutos = 3
            if minutos_dentro <= 59 and minutos_dentro  >= 45:
                minutos = 4
            if ffeecha.days == 0 and horas_dentro == 0:
               importe = 30
               self.importe.set(importe)
               #self.elimportees.set(importe)
               self.label9.configure(text =(importe, "cobro"))
               self.entrypromo.focus()
            else:
                importe = ((ffeecha.days)*720 + (horas_dentro * 30)+(minutos)*7.5)
                self.importe.set(importe)
                self.label9.configure(text =(importe, "Cobrar"))
                #self.calcular_cambio()
                self.entrypromo.focus()
    def calcular_cambio(self):
        elimporte=str(self.importe.get(), )
        self.elimportees.set(elimporte)
        valorescrito=str(self.cuantopagasen.get(),)
        elimporte=float(elimporte)
        valorescrito=int(valorescrito)
        mb.showinfo("Imp", elimporte)
        cambio=valorescrito-elimporte
        cambio=str(cambio)
        mb.showinfo("CMbn", cambio)
        self.elcambioes.set(cambio)
        self.Comprobante()#manda a llamar el comprobante y lo imprime
        self.GuardarCobro()#manda a llamar guardar cobro para cobrarlo y guardar registro
        io.output(out1,0)
        time.sleep(1)
        io.output(out1,1)

    def Comprobante(self):
        #p = Usb(0x04b8, 0x0202, 0)
        p = Usb(0x04b8, 0x0e28, 0)#esta es la impresora con sus valores que se obtienen con lsusb
        p.text("Comprobante de pago\n")
        p.image("LOGO1.jpg")
        #Compro de comprobante
        ImporteCompro=str(self.importe.get(),)
        p.text("El importe es $"+ImporteCompro+"\n")
        EntradaCompro = str(self.descripcion.get(),)
        p.text('El auto entro: '+EntradaCompro+'\n')
        SalioCompro = str(self.copia.get(),)
        p.text('El auto salio: '+SalioCompro+'\n')
        TiempoCompro = str(self.ffeecha.get(),)
        p.text('El auto permanecio: '+TiempoCompro+'\n')
        folioactual=str(self.folio.get(), )
        p.text('El folio del boleto es: '+folioactual+'\n')
        p.text('Le atendio: ')
        p.cut()
    def GuardarCobro(self):
        salida = str(self.precio.get(), )#deveria ser salida en lugar de precio pero asi estaba el base

        if len(salida)>5:
            self.label15.configure(text=("con salida, INMODIFICABLE"))
            mb.showinfo("Información", "Ya Tiene Salida")
            self.descripcion.set('')
            self.precio.set('')
            self.copia.set("")
            self.importe.set("")
            self.ffeecha.set("")
            self.folio.set("")
            self.label7.configure(text=(""))
            self.label8.configure(text =(""))
            self.label9.configure(text =(""))
            self.label11.configure(text=(""))
            self.label12.configure(text=(""))
            self.label15.configure(text=(""))
            self.entryfolio.focus()
        else:
            #self.Comprobante()
            self.label15.configure(text=(salida, "SI se debe modificar"))
            importe1 =str(self.importe.get(),)
            mb.showinfo("impte1", importe1)
            folio1= str(self.folio.get(),)
            valorhoy = str(self.copia.get(),)
            fechaActual1 = datetime.strptime(valorhoy, '%Y-%m-%d %H:%M:%S' )
            fechaActual= datetime.strftime(fechaActual1,'%Y-%m-%d %H:%M:%S' )
            ffeecha1= str(self.ffeecha.get(),)
            valor=str(self.descripcion.get(),)
            fechaOrigen = datetime.strptime(valor, '%Y-%m-%d %H:%M:%S')
            promoTipo = str(self.PrTi.get(),)
            vobo = "lmf"#este
            datos=(vobo, importe1, ffeecha1, fechaOrigen, fechaActual, promoTipo, folio1)
            self.operacion1.guardacobro(datos)
            self.descripcion.set('')
            self.precio.set('')
            self.copia.set("")
            self.label7.configure(text=(""))
            self.label8.configure(text =(""))
            self.label9.configure(text =(""))
            self.label11.configure(text=(""))
            self.label12.configure(text=(""))
            self.label15.configure(text=(""))
            self.importe.set("")
            self.ffeecha.set("")
            self.folio.set("")
            self.PrTi.set("")
            #self.elcambioes.set("")
            #self.elimportees.set("")
            #self.cuantopagasen.set("")
            self.entryfolio.focus()#se posiciona en leer qr
    def CalculaPromocion(self):
        TipoPromocion = str(self.promo.get(), )#se recibe el codigo
        TipoProIni=TipoPromocion[:8]
        if TipoProIni==("AM ADMIN"):
           NumP=TipoPromocion[10:]
           self.importe.set(0)
           self.label9.configure(text =(0, "cobro"))
           self.PrTi.set("ADMIN")
#           mb.showinfo("ADMIN",NumP)
           self.promo.set("")
###########starbucks
        if TipoProIni==("ST STARB"):
           NumP=TipoPromocion[12:]
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2            #self.label11.configure(text=(ffeecha.days, "dias"))
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if minutos_dentro >=0 and minutos_dentro<=15:
                importe = 0
           if minutos_dentro >15 and minutos_dentro < 60:
                importe = 20
           if horas_dentro == 1 and minutos_dentro <=30:
                importe = 20
           if horas_dentro == 1 and minutos_dentro <= 45 and minutos_dentro > 30:
                importe = 27.5
           if horas_dentro == 1 and minutos_dentro < 60 and minutos_dentro > 45:
                importe = 35
           if horas_dentro == 2 and minutos_dentro <=15:
                importe = 42.5
           if horas_dentro == 2 and minutos_dentro >15 and minutos_dentro <= 30:
                importe = 50
           if horas_dentro == 2 and minutos_dentro >30 and minutos_dentro <= 45:
                importe = 57.5
           if horas_dentro == 2 and minutos_dentro >45 and minutos_dentro < 60:
                importe = 65
           if horas_dentro == 3 and minutos_dentro <=15:
                importe = 72.5
           if horas_dentro == 3 and minutos_dentro >15 and minutos_dentro <= 30:
                importe = 80
           if horas_dentro == 3 and minutos_dentro >30 and minutos_dentro <= 45:
                importe = 87.5
           if horas_dentro == 3 and minutos_dentro >45 and minutos_dentro < 60:
                importe = 95
           if horas_dentro >= 4:
                importe = ((ffeecha.days)*720 + (horas_dentro * 30)+(minutos)*1)
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("StB")
           #mb.showinfo("STARBUCKS",NumP)
           self.promo.set("")
########## Promocion Sonora
        if TipoProIni==("SG SONOR"):
           NumP=TipoPromocion[15:]
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if minutos_dentro < 60:
               importe = 50
           if horas_dentro >= 1 and horas_dentro <= 3 :
                importe = 50
           if horas_dentro == 3 and minutos_dentro <=15:
                importe = 50
           if horas_dentro == 3 and minutos_dentro >= 16:
                importe = 70
           if horas_dentro >= 4 and horas_dentro < 8:
                importe = 70
           if horas_dentro == 8 and minutos_dentro <=15:
                importe = 77
           if horas_dentro == 8 and minutos_dentro >=16:
                importe = 85
           if horas_dentro == 9 and minutos_dentro <=15:
                importe = 100
           if horas_dentro == 9 and minutos_dentro >=16:
                importe = 115              
           if horas_dentro >= 10:
                importe = ((ffeecha.days)*720 + (horas_dentro * 30)+(minutos_dentro)*1)
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("SNR")
          # mb.showinfo("SONORA",NumP)
           self.promo.set("")
#############promocion at pote
        if TipoProIni==("AT APOTE"):
           NumP=TipoPromocion[10:]
           self.importe.set(70)
           self.label9.configure(text =(70, "cobro"))
           self.PrTi.set("APOTEK")
#           mb.showinfo("ADMIN",NumP)
           self.promo.set("")
############ promocion crepas and wafles
        if TipoProIni==("CW CREPE"):
           NumP=TipoPromocion[18:]
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if minutos_dentro >=0 and minutos_dentro<60:
                importe = 40
           if horas_dentro == 1 and minutos_dentro <= 45:
                importe = 40
           if horas_dentro == 1 and minutos_dentro >45 and minutos_dentro  < 60:
                importe = 45
           if horas_dentro == 2 and minutos_dentro >= 1:
                importe = 45
           if horas_dentro == 2 and minutos_dentro >15 and minutos_dentro  < 60:
                importe = 50
           if horas_dentro == 3 and minutos_dentro <=15:
                importe = 57.5
           if horas_dentro == 3 and minutos_dentro >15 and minutos_dentro <= 30:
                importe = 57.5
           if horas_dentro == 3 and minutos_dentro >30 and minutos_dentro <= 45:
                importe = 65
           if horas_dentro == 3 and minutos_dentro >45 and minutos_dentro < 60:
                importe = 65
           if horas_dentro >= 4:
                importe = ((ffeecha.days)*720 + (horas_dentro * 30)+(minutos)*1)
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("C&W")
          # mb.showinfo("CREPES&WAFLES",NumP)
           self.promo.set("")
###################### Fin de Pagina2 Inicio Pagina3 ###############################
    def listado_completo(self):
        self.pagina3 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina3, text="Módulo de Corte")
        self.labelframe1=ttk.LabelFrame(self.pagina3, text="Autos")
        self.labelframe1.grid(column=0, row=0, padx=1, pady=1)
        self.labelframe2=ttk.LabelFrame(self.pagina3, text="Generar Corte")
        self.labelframe2.grid(column=1, row=0, padx=0, pady=0)
        self.labelframe3=ttk.LabelFrame(self.pagina3, text="Consulta Cortes Anteriores")
        self.labelframe3.grid(column=0, row=1, padx=0, pady=0)

        self.labelframe4=ttk.LabelFrame(self.pagina3, text="Cuadro Comparativo")
        self.labelframe4.grid(column=1, row=1, padx=0, pady=0)
        self.lblSal=ttk.Label(self.labelframe4, text="Salida de Autos")
        self.lblSal.grid(column=3, row=1, padx=1, pady=1)
        self.lblS=ttk.Label(self.labelframe4, text="Entrada de Autos")
        self.lblS.grid(column=3, row=2, padx=1, pady=1)
        self.lblAnterior=ttk.Label(self.labelframe4, text="Autos del Turno anterior")
        self.lblAnterior.grid(column=3, row=3, padx=1, pady=1)
        self.lblEnEstac=ttk.Label(self.labelframe4, text="Autos en Estacionamiento")
        self.lblEnEstac.grid(column=3, row=4, padx=1, pady=1)
        self.lblC=ttk.Label(self.labelframe4, text="Boletos Cobrados:")
        self.lblC.grid(column=0, row=1, padx=1, pady=1)
        self.lblE=ttk.Label(self.labelframe4, text="Boletos Expedidos:")
        self.lblE.grid(column=0, row=2, padx=1, pady=1)
        self.lblA=ttk.Label(self.labelframe4, text="Boletos Turno Anterior:")
        self.lblA.grid(column=0, row=3, padx=1, pady=1)
        self.lblT=ttk.Label(self.labelframe4, text="Boletos Por Cobrar:")
        self.lblT.grid(column=0, row=4, padx=1, pady=1)
        self.BoletosCobrados=tk.StringVar()
        self.entryBoletosCobrados=tk.Entry(self.labelframe4, width=5, textvariable=self.BoletosCobrados, state= "readonly")
        self.entryBoletosCobrados.grid(column=1, row=1)
        self.BEDespuesCorte=tk.StringVar()
        self.entryBEDespuesCorte=tk.Entry(self.labelframe4, width=5, textvariable=self.BEDespuesCorte, state= "readonly")
        self.entryBEDespuesCorte.grid(column=1, row=2)
        self.BAnteriores=tk.StringVar()
        self.entryBAnteriores=tk.Entry(self.labelframe4, width=5, textvariable=self.BAnteriores, state= "readonly")
        self.entryBAnteriores.grid(column=1, row=3)
        self.BDentro=tk.StringVar()
        self.entryBDentro=tk.Entry(self.labelframe4, width=5, textvariable=self.BDentro, state= "readonly")
        self.entryBDentro.grid(column=1, row=4)
        self.SalidaAutos=tk.StringVar()
        self.entrySalidaAutos=tk.Entry(self.labelframe4, width=5, textvariable=self.SalidaAutos, state= "readonly")
        self.entrySalidaAutos.grid(column=2, row=1)
        self.SensorEntrada=tk.StringVar()
        self.entrySensorEntrada=tk.Entry(self.labelframe4, width=5, textvariable=self.SensorEntrada, state= "readonly", borderwidth=5)
        self.entrySensorEntrada.grid(column=2, row=2)
        self.Autos_Anteriores=tk.StringVar()
        self.entryAutos_Anteriores=tk.Entry(self.labelframe4, width=5, textvariable=self.Autos_Anteriores, state= "readonly")
        self.entryAutos_Anteriores.grid(column=2, row=3)
        self.AutosEnEstacionamiento=tk.StringVar()
        self.entryAutosEnEstacionamiento=tk.Entry(self.labelframe4, width=5, textvariable=self.AutosEnEstacionamiento, state= "readonly", borderwidth=5)
        self.entryAutosEnEstacionamiento.grid(column=2, row=4)
        self.boton6=tk.Button(self.labelframe4, text="Consulta Bol-Sensor", command=self.Puertoycontar, width=15, height=3, anchor="center")
        self.boton6.grid(column=1, row=0, padx=1, pady=1)

        self.FrmCancelado=ttk.LabelFrame(self.pagina3, text="Boleto Cancelado")
        self.FrmCancelado.grid(column=0, row=2, padx=0, pady=0)
        self.labelCorte=ttk.Label(self.labelframe2, text="El Total del CORTE es:")
        self.labelCorte.grid(column=0, row=1, padx=0, pady=0)
        self.label2=ttk.Label(self.labelframe2, text="La Fecha de CORTE es:")
        self.label2.grid(column=0, row=2, padx=1, pady=1)
        self.label3=ttk.Label(self.labelframe2, text="El CORTE Inicia ")
        self.label3.grid(column=0, row=3, padx=1, pady=1)
        self.label4=ttk.Label(self.labelframe2, text="El Numero de CORTE es:")
        self.label4.grid(column=0, row=4, padx=1, pady=1)
        self.label5=ttk.Label(self.labelframe3, text="CORTE a Consultar :")
        self.label5.grid(column=0, row=1, padx=1, pady=1)
        self.label6=ttk.Label(self.labelframe3, text="Fecha y hora del CORTE")
        self.label6.grid(column=0, row=2, padx=1, pady=1)

        self.lblCancelado=ttk.Label(self.FrmCancelado, text="COLOCAR FOLIO")
        self.lblCancelado.grid(column=0, row=1, padx=4, pady=4)
        self.FolioCancelado=tk.StringVar()
        self.entryFOLIOCancelado=tk.Entry(self.FrmCancelado, width=15, textvariable=self.FolioCancelado)
        self.entryFOLIOCancelado.grid(column=1, row=1)
        self.boton7=tk.Button(self.FrmCancelado, text="B./SIN cobro", command=self.BoletoDentro2, width=15, height=3, anchor="center")
        self.boton7.grid(column=0, row=0, padx=1, pady=1)
        #self.boton8=tk.Button(self.FrmCancelado, text="desglose", command=self.desglose_cobrados, width=15, height=3, anchor="center")
        #self.boton8.grid(column=1, row=3, padx=1, pady=1)

        self.btnCancelado=tk.Button(self.FrmCancelado, text="Cancelar Boleto ", command=self.BoletoCancelado, width=10, height=2, anchor="center")
        self.btnCancelado.grid(column=0, row=2)
        self.scrolledtxt2=st.ScrolledText(self.FrmCancelado, width=28, height=7)
        self.scrolledtxt2.grid(column=1,row=0, padx=1, pady=1)
        self.ImporteCorte=tk.StringVar()
        self.entryImporteCorte=tk.Entry(self.labelframe2, width=20, textvariable=self.ImporteCorte, state= "readonly", borderwidth=5)
        self.entryImporteCorte.grid(column=1, row=1)
        self.FechaCorte=tk.StringVar()
        self.entryFechaCorte=tk.Entry(self.labelframe2, width=20, textvariable=self.FechaCorte, state= "readonly")
        self.entryFechaCorte.grid(column=1, row=2)
        self.FechUCORTE=tk.StringVar()
        self.entryFechUCORTE=tk.Entry(self.labelframe2, width=20, textvariable=self.FechUCORTE, state= "readonly")
        self.entryFechUCORTE.grid(column=1, row=3)
        self.CortesAnteri=tk.StringVar()
        self.CortesAnteri=tk.Entry(self.labelframe3, width=20, textvariable=self.CortesAnteri)
        self.CortesAnteri.grid(column=1, row=1)
        self.boton1=ttk.Button(self.labelframe1, text="Todas las Entradas", command=self.listar)
        self.boton1.grid(column=0, row=0, padx=4, pady=4)
        self.boton2=ttk.Button(self.labelframe1, text="Entradas sin corte", command=self.listar1)
        self.boton2.grid(column=0, row=2, padx=4, pady=4)
        self.boton3=tk.Button(self.labelframe2, text="Calcular Corte", command=self.Calcular_Corte, width=15, height=1)
        self.boton3.grid(column=2, row=0, padx=4, pady=4)
        self.boton4=tk.Button(self.labelframe2, text="Guardar Corte", command=self.Guardar_Corte, width=15, height=1, anchor="center", background="blue")
        self.boton4.grid(column=2, row=4, padx=4, pady=4)
        self.boton5=tk.Button(self.labelframe3, text="Imprimir salidas  Corte", command=self.desglose_cobrados, width=15, height=3, anchor="center")
        self.boton5.grid(column=1, row=2, padx=4, pady=4)
        self.scrolledtext1=st.ScrolledText(self.labelframe1, width=30, height=4)
        self.scrolledtext1.grid(column=0,row=1, padx=1, pady=1)
    def BoletoDentro2(self):
        respuesta=self.operacion1.Autos_dentro()
        self.scrolledtxt2.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtxt2.insert(tk.END, "Folio num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nPlacas: "+str(fila[2])+"\n\n")
    def desglose_cobrados(self):
        Numcorte=str(self.CortesAnteri.get(), )
        Numcorte=int(Numcorte)
        Numcorte=str(Numcorte)
        io.output(out1,0)
        time.sleep(1)
        io.output(out1,1)
        respuesta=self.operacion1.desglose_cobrados(Numcorte)
        self.scrolledtxt2.delete("1.0", tk.END)
        #p = Usb(0x04b8, 0x0202, 0)
        p = Usb(0x04b8, 0x0e28, 0)#esta es la impresora con sus valores que se obtienen con lsusb
        p.text("El Numero de corte es "+Numcorte+'\n')
        for fila in respuesta:
            self.scrolledtxt2.insert(tk.END, "cobro: "+str(fila[0])+"\nImporte: $"+str(fila[1])+"\nCuantos: "+str(fila[2])+"\n\n")
            p.text('Tipo de cobro :')
            p.text(str(fila[0]))
            p.text('\n')
            p.text('Importe :')
            p.text(str(fila[1]))
            p.text('\n')
            p.text('Cuantos ')
            p.text(str(fila[2]))
            p.text('\n')
        else:
            p.cut()
    def BoletoCancelado(self):
       datos=str(self.FolioCancelado.get(), )
       datos=int(datos)
       datos=str(datos)
       self.folio.set(datos)
       datos=(self.folio.get(), )
       respuesta=self.operacion1.consulta(datos)
       if len(respuesta)>0:
           self.descripcion.set(respuesta[0][0])
           self.precio.set(respuesta[0][1])
           self.CalculaPermanencia()#nos vamos a la funcion de calcular permanencia
           fecha = datetime.today()
           fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
           fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
           date_time_str=str(self.descripcion.get())
           date_time_obj= datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
           date_time_mod = datetime.strftime(date_time_obj, '%Y/%m/%d/%H/%M/%S')
           date_time_mod2 = datetime.strptime(date_time_mod, '%Y/%m/%d/%H/%M/%S')
           ffeecha = fechaActual - date_time_mod2
            #self.label11.configure(text=(ffeecha.days, "dias"))
           segundos_vividos = ffeecha.seconds
           horas_dentro, segundos_vividos = divmod(segundos_vividos, 3600)
        #    self.label12.configure(text=(horas_dentro, "horas"))
           minutos_dentro, segundos_vividos = divmod(segundos_vividos, 60)
           if horas_dentro <= 24:
                importe = 0
           if horas_dentro > 24 or ffeecha.days >= 1:
                importe =0
           self.importe.set(importe)
           self.label9.configure(text =(importe, "cobro"))
           self.PrTi.set("CDO")
           self.promo.set("")
           #p = Usb(0x04b8, 0x0202, 0)
           p = Usb(0x04b8, 0x0e28, 0)#esta es la impresora con sus valores que se obtienen con lsusb
           p.text('Boleto Cancelado\n')
           FoliodelCancelado = str(self.FolioCancelado.get(),)
           p.text('Folio boleto cancelado: '+FoliodelCancelado+'\n')
           fecha = datetime.today()
           fechaNota = datetime.today()
           fechaNota= fechaNota.strftime("%b-%d-%A-%Y %H:%M:%S")
           horaNota = str(fechaNota)
           p.set(align="left")
           p.set('Big line\n', font='b')
           p.text('Fecha: '+horaNota+'\n')
           EntradaCompro = str(self.descripcion.get(),)
           p.text('El auto entro: '+EntradaCompro+'\n')
           SalioCompro = str(self.copia.get(),)
           p.text('El auto salio: '+SalioCompro+'\n')
           self.GuardarCobro()
           self.FolioCancelado.set("")
           p.cut()

       else:
           self.descripcion.set('')
           self.precio.set('')
           mb.showinfo("Información", "No existe un auto con dicho código")
    def listar(self):
        respuesta=self.operacion1.recuperar_todos()
        self.scrolledtext1.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, "Entrada num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nSalio: "+str(fila[2])+"\n\n")
    def listar1(self):
        respuesta=self.operacion1.recuperar_sincobro()
        self.scrolledtext1.delete("1.0", tk.END)
        #respuesta=str(respuesta)
        for fila in respuesta:
            self.scrolledtext1.insert(tk.END, "Entrada num: "+str(fila[0])+"\nEntro: "+str(fila[1])+"\nSalio: "+str(fila[2])+"\nImporte: "+str(fila[3])+"\n\n")
            #p = Usb(0x04b8, 0x0202, 0)
            p = Usb(0x04b8, 0x0e28, 0)#esta es la impresora con sus valores que se obtienen con lsusb
            p.text('Entrada Num :')
            p.text(str(fila[0]))
            p.text('\n')
            p.text('Entro :')
            p.text(str(fila[1]))
            p.text('\n')
            p.text('Salio :')
            p.text(str(fila[2]))
            p.text('\n')
            p.text('importe :')
            p.text(str(fila[3]))
            p.text('\n')
        else:
            p.cut()
    def Calcular_Corte(self):
        respuesta=self.operacion1.corte()
        self.ImporteCorte.set(respuesta)
        ##obtengamo la fechaFin del ultimo corte
        ultiCort1=str(self.operacion1.UltimoCorte())
        #mb.showinfo("msj uno",ultiCort1)
        startLoc = 20
        endLoc = 43
        ultiCort1=(ultiCort1)[startLoc: endLoc]
        ultiCort1 = ultiCort1.strip('),')
        if len(ultiCort1) <= 17:
                            # mb.showinfo("msj dos",ultiCort1)
                             ultiCort1= datetime.strptime(ultiCort1, '%Y, %m, %d, %H, %M')
        else:
            ultiCort1= datetime.strptime(ultiCort1, '%Y, %m, %d, %H, %M, %S')        
            #mb.showinfo("msj tres",ultiCort1)
        ultiCort1 = datetime.strftime(ultiCort1, '%Y/%m/%d/%H/%M/%S')
        ultiCort1 = datetime.strptime(ultiCort1, '%Y/%m/%d/%H/%M/%S')
        self.FechUCORTE.set(ultiCort1)# donde el label no esta bloqueada
        ###ahora obtenemos la fecha del corte ha realizar
        fecha = datetime.today()
        fecha1= fecha.strftime("%Y-%m-%d %H:%M:%S")
        fechaActual= datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
        self.FechaCorte.set(fechaActual)#donde el label esta bloqueado
    def Guardar_Corte(self):
        self.Puertoycontar()
        ##la fecha final de este corte que es la actual
        fechaDECorte = str(self.FechaCorte.get(),)
        fechaDECorte = datetime.strptime(fechaDECorte, '%Y-%m-%d %H:%M:%S' )
        ######la fecha del inicial obtiene de labase de datos
        fechaInicio1 = str(self.FechUCORTE.get(),)
        fechaInicio2 = datetime.strptime(fechaInicio1, '%Y-%m-%d %H:%M:%S')
        fechaInicio = fechaInicio2
        ######el importe se obtiene de la suma
        ImpCorte2 =str(self.ImporteCorte.get(),)
        #este quita lo que no sea numero esto de abajo
        #self.label2.configure(text ="".join([x for x in ImpCorte2 if x.isdigit()]) )
        Im38 = "".join([x for x in ImpCorte2 if x.isdigit()])
        #mete los valores a la base de datos
        AEE = 0#str(self.AutosEnEstacionamiento.get(),)
        maxnumid=str(self.operacion1.MaxfolioEntrada())
        maxnumid = "".join([x for x in maxnumid if x.isdigit()])#con esto solo obtenemos los numeros
        maxnumid=int(maxnumid)
        maxnumid=str(maxnumid)
        pasa = str(self.BDentro.get(),)
        NumBolQued = pasa.strip('(),')
        datos=(Im38, fechaInicio, fechaDECorte,AEE,maxnumid,NumBolQued)
        self.operacion1.GuarCorte(datos)
        maxnum1=str(self.operacion1.Maxfolio_Cortes())
        maxnum = "".join([x for x in maxnum1 if x.isdigit()])#con esto solo obtenemos los numeros
        maxnum=int(maxnum)
        maxnum=str(maxnum)
        vobo = "cor"#este es para que la instruccion no marque error
        ActEntradas = (maxnum, vobo )
        self.label4.configure(text=("Numero de corte",maxnum))
        #p = Usb(0x04b8, 0x0202, 0)
        p = Usb(0x04b8, 0x0e28, 0)#esta es la impresora con sus valores que se obtienen con lsusb
        p.text("CORTE Num "+maxnum+"\n")
        p.text('IMPORTE: $ '+Im38+'\n')
        ultiCort1=str(self.FechUCORTE.get(),)
        ultiCort4= datetime.strptime(ultiCort1, '%Y-%m-%d %H:%M:%S')
        ultiCort5 = datetime.strftime(ultiCort4, '%A %d %m %Y a las %H:%M:%S')
        p.text('Inicio:')
        p.text(ultiCort5)
        p.text('\n')
        valorFEsteCorte = str(self.FechaCorte.get(),)
        fechaDECorte = datetime.strptime(valorFEsteCorte, '%Y-%m-%d %H:%M:%S' )
        fechaDECorte = datetime.strftime(fechaDECorte, '%A %d %m %Y a las %H:%M:%S' )
        p.text('Final :')
        p.text(str(fechaDECorte))
        p.text('\n')
        BolCobrImpresion=str(self.BoletosCobrados.get(),)
        p.text("Boletos Cobrados: "+BolCobrImpresion+"\n")
        #SalidasSen =  int(self.SalidaAutos.get(),)
        #SalidasSen =  str(SalidasSen)
        #p.text("Salidas Sensor: "+SalidasSen+"\n")
        BEDespuesCorteImpre = str(self.BEDespuesCorte.get(),)
        p.text('Boletos Expedidos: '+BEDespuesCorteImpre+'\n')
        #EntradasSen = int(self.SensorEntrada.get(),)
        #EntradasSen =  str(EntradasSen)
        #p.text('Entradas Sensor: '+EntradasSen+'\n')
        BAnterioresImpr=str(self.BAnteriores.get(),)#######
        p.text("Boletos Turno Anterior: "+BAnterioresImpr+"\n")
        #AutosAnteriores = int(self.Autos_Anteriores.get(),)
        #AutosAnteriores = str(AutosAnteriores)
        #p.text('Sensor Turno Anterior: '+AutosAnteriores+'\n')
        BDentroImp = str(self.BDentro.get(),)
        p.text('Boletos por Cobrar: '+BDentroImp+'\n')
        AutosEnEstacImpre = str(self.AutosEnEstacionamiento.get(),)
        #p.text('Autos en estacionamiento por sensor: '+AutosEnEstacImpre+'\n')
        p.text('Le atendio: PASE S.A. de C.V.')
        #Bandera = o
        self.ImporteCorte.set("")
        p.cut()
        self.operacion1.ActualizarEntradasConcorte(ActEntradas)
        vobo='ant'
        self.operacion1.NocobradosAnt(vobo)
        #ser = serial.Serial('/dev/ttyAMA0', 9600)
        #Enviamos el caracter por serial, codificado en Unicode
        #entrada='c'
        #ser.write(str(entrada).encode())
    def Puertoycontar(self):
        #ser = serial.Serial('/dev/ttyAMA0', 9600)
        #Enviamos el caracter por serial, codificado en Unicode
        #entrada='e'
        #ser.write(str(entrada).encode())
        #Leemos lo que hay en el puerto y quitamos lo que no queremos
        #sArduino = str(ser.readline())
        #sArduino = "" .join([x for x in sArduino if x.isdigit()])#esto es para solo poner numeros
        #CuantosEntradas=str(self.operacion1.EntradasSensor())
        #sArduino = 1
        #CuantosEntradas = CuantosEntradas.strip('(),')
        #self.SensorEntrada.set(CuantosEntradas)
        #entrada='a'
        #ser.write(str(entrada).encode())
        #Leemos lo que hay en el puerto y quitamos lo que no queremos
        #sArduino = str(ser.readline())
        #sArduino = "" .join([x for x in sArduino if x.isdigit()])#esto es para solo poner num
        #CuantosSalidas=str(self.operacion1.SalidasSensor())
        #sArduino =1
        #CuantosSalidas = CuantosSalidas.strip('(),')
        #self.SalidaAutos.set(CuantosSalidas)
        #EntradasSen = int(self.SensorEntrada.get(),)
        #SalidasSen =  int(self.SalidaAutos.get(),)
        CuantosBoletosCobro=str(self.operacion1.CuantosBoletosCobro())
        CuantosBoletosCobro = CuantosBoletosCobro.strip('(),')
        self.BoletosCobrados.set(CuantosBoletosCobro)
        BEDCorte=str(self.operacion1.BEDCorte())
        BEDCorte = BEDCorte.strip('(),')
        self.BEDespuesCorte.set(BEDCorte)
        BAnteriores=str(self.operacion1.BAnteriores())
        BAnteriores = BAnteriores.strip('(),')
        self.BAnteriores.set(BAnteriores)
        MaxFolioCorte=str(self.operacion1.Maxfolio_Cortes())
        MaxFolioCorte=MaxFolioCorte.strip('(),')
        QuedadosBol=str(self.operacion1.Quedados_Sensor(MaxFolioCorte))
        QuedadosBol=QuedadosBol.strip('(),')
        self.BAnteriores.set(QuedadosBol)
        maxNumidIni=str(self.operacion1.MaxnumId())
        maxNumidIni = "".join([x for x in maxNumidIni if x.isdigit()])#con esto solo obtenemos los numeros
        maxNumidIni=int(maxNumidIni)
        maxFolioEntradas= str(self.operacion1.MaxfolioEntrada())
        maxFolioEntradas = "".join([x for x in maxFolioEntradas if x.isdigit()])#con esto solo obtenemos los numero
        maxFolioEntradas=int(maxFolioEntradas)
        BEDCorte=maxFolioEntradas-maxNumidIni
        BEDCorte=str(BEDCorte)
        self.BEDespuesCorte.set(BEDCorte)
        CuantosAutosdentro=str(self.operacion1.CuantosAutosdentro())
        MaxFolioCorte=str(self.operacion1.Maxfolio_Cortes())
        MaxFolioCorte=MaxFolioCorte.strip('(),')
        dentroCorte=str(self.operacion1.Quedados_Sensor(MaxFolioCorte))
        CuantosAutosdentro = CuantosAutosdentro.strip('(),')
        dentroCorte = dentroCorte.strip('(),')
        self.BDentro.set(CuantosAutosdentro)
        self.Autos_Anteriores.set(dentroCorte)
        #AutosAnteriores = int(self.Autos_Anteriores.get(),)
        #Cuantos_hay_dentro = ((AutosAnteriores + EntradasSen) - SalidasSen)
        #self.AutosEnEstacionamiento.set(Cuantos_hay_entro)


    def cifrar_folio(self, folio):
        """
        Cifra un número de folio utilizando una tabla de sustitución numérica.

        Args:
            folio (int): Número de folio a cifrar.

        Returns:
            str: Número de folio cifrado.
        """

        # Convierte el número de folio en una cadena de texto.
        folio = str(folio)

        # Genera un número aleatorio de 5 dígitos y lo convierte en una cadena de texto.
        num_random = random.randint(10000, 99999)
        numero_seguridad = str(num_random)

        # Concatena el número de seguridad al número de folio.
        folio = folio + numero_seguridad

        # Tabla de sustitución numérica.
        tabla = {'0': '5', '1': '3', '2': '9', '3': '1', '4': '7', '5': '0', '6': '8', '7': '4', '8': '6', '9': '2'}

        # Convierte el número de folio cifrado a una lista de dígitos.
        digitos = list(folio)

        # Sustituye cada dígito por el número correspondiente en la tabla de sustitución.
        cifrado = [tabla[digito] for digito in digitos]

        # Convierte la lista cifrada de vuelta a una cadena de texto.
        cifrado = ''.join(cifrado)

        # Devuelve el número de folio cifrado.
        return cifrado


    def descifrar_folio(self, folio_cifrado):
        """
        Descifra un número de folio cifrado utilizando una tabla de sustitución numérica.

        Args:
            folio_cifrado (str): Número de folio cifrado.

        Returns:
            str: Número de folio descifrado.
        """
        try:
            # Verifica si el número de folio es válido.
            if len(folio_cifrado) <= 5:
                raise ValueError("El folio no es válido, escanee nuevamente, si el error persiste contacte con un administrador.")

            # Verifica si el número de folio tiene caracteres inválidos.
            caracteres_invalidos = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '{', '}', '[', ']', '|', '\\', ':', ';', '<', '>', ',', '.', '/', '?']
            if any(caracter in folio_cifrado for caracter in caracteres_invalidos):
                raise TypeError("El folio no tiene un formato válido")

            # Tabla de sustitución numérica.
            tabla = {'0': '5', '1': '3', '2': '9', '3': '1', '4': '7', '5': '0', '6': '8', '7': '4', '8': '6', '9': '2'}

            # Convierte el número de folio cifrado a una lista de dígitos.
            digitos_cifrados = list(folio_cifrado)

            # Crea una tabla de sustitución inversa invirtiendo la tabla original.
            tabla_inversa = {valor: clave for clave, valor in tabla.items()}

            # Sustituye cada dígito cifrado por el número correspondiente en la tabla de sustitución inversa.
            descifrado = [tabla_inversa[digito] for digito in digitos_cifrados]

            # Convierte la lista descifrada de vuelta a una cadena de texto.
            descifrado = ''.join(descifrado)

            # Elimina los últimos 4 dígitos, que corresponden al número aleatorio generado en la función cifrar_folio.
            descifrado = descifrado[:-5]

            # Retorna el folio descifrado.
            return descifrado

        # Maneja el error si el formato del número de folio es incorrecto.
        except TypeError as error:
            print(error)
            mb.showerror("Error", f"El folio tiene un formato incorrecto, si el error persiste contacte a un administrador y muestre el siguiente error:\n{error}")
            return None

        # Maneja cualquier otro error que pueda ocurrir al descifrar el número de folio.
        except Exception as error:
            print(error)
            mb.showerror("Error", f"Ha ocurrido un error al descifrar el folio, intente nuevamente, si el error persiste contacte a un administrador y muestre el siguiente error:\n{error}")
            return None


    def generar_QR(self, QR_info: str, path: str = "reducida.png") -> None:
        """Genera un código QR a partir de la información dada y lo guarda en un archivo de imagen.

        Args:
            QR_info (str): La información para generar el código QR.
            path (str, optional): La ruta y el nombre del archivo de imagen donde se guardará el código QR, por defecto es "reducida.png".
        """
        # Generar el código QR
        img = qrcode.make(QR_info)

        # Redimensionar el código QR a un tamaño específico
        img = img.get_image().resize((320, 320))

        # Guardar la imagen redimensionada en un archivo
        img.save(path)


aplicacion1=FormularioOperacion()
