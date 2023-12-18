from datetime import datetime, time, timedelta
formato = "%H:%M:%S"
from escpos.printer import *
import qrcode
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import operacion
import time

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
io.output(barrera,1)
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
        self.cuaderno1.config(cursor="")

        self.ExpedirRfid()
        self.check_inputs()
        self.IntBoton()
        self.Intloop()

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

    def Intloop(self): #Detecta presencia de automovil
        global BanLoop
        if io.input(loop):
            print('hay auto') 
            io.output(out1,0)#con un "1" se apaga el led
            BanLoop = 1
        else:
            io.output(out1,1)                              
            BanLoop = 0

    def IntBoton(self): #Detecta presencia de automovil
        global BanBoton
        if io.input(boton):
            print('Presiono boton')
            io.output(out2,0)
            BanBoton = 1
        else:
            io.output(out2,1)
            BanBoton = 0

    io.add_event_detect(loop, io.BOTH, callback = Intloop)
    io.add_event_detect(boton, io.BOTH, callback = IntBoton)


    def check_inputs(self):
        global BanBoton, BanLoop, BanImpresion
    
        if BanLoop == 1:
            self.loopDet.config(text = "Hay auto", font=('Arial', 15), background = 'green')
            tarjeta=str(self.entryNumTarjeta4.get(),)
            #BanImpresion = 1
            if len(tarjeta) == 10:
                self.Pensionados(self)
        else:
            self.loopDet.config(text = ".", font=('Arial', 15), background = '#CCC') #'#CCC'
            self.SenBol2.config(text = ".", font=('Arial', 15), background='#CCC')
            self.SenBol.config(text = ".", font=('Arial', 15), background='#CCC')
            self.labelMensaje.config(text= "Sin Tarjeta para acceder")
            self.NumTarjeta4.set("")               
            self.entryNumTarjeta4.focus()
            BanImpresion = 1

        if BanBoton == 1:
            self.BotDet.config(text = "presiono btn", font=('Arial', 15), background='#CCC') #'#CCC'
            if BanImpresion == 1:# and BanSenBoleto == 0:# mando a imprimir y ya no tiene boleto en la boquilla
                #self.SenBol.config(text = "AVANCE", font=('Arial', 15), background= "green") #'#CCC'
                print('mando abrir barrera')
                io.output(barrera,0)#con un "0" abre la barrera
                time.sleep (1)
                io.output(barrera,1)
                self.agregarRegistroRFID()                
                BanImpresion = 0
            else:   
                self.SenBol.config(text = "press btn sin impresion", font=('Arial', 15), background= "red") 

        else: 
            self.BotDet.config(text = "solto btn", font=('Arial', 15), background='#CCC') #'#CCC'       
            self.SenBol.config(text = "", font=('Arial', 15), background="#CCC")
            #if BanBoton == 1 and BanLoop==1:
           

            #BanImpresion = 1

        now =datetime.now() 
        fecha1= now.strftime("%d-%b-%y")
        hora1= now.strftime("%H:%M:%S")    
        self.Reloj.config(text=fecha1)            
        self.mi_reloj.config(text=hora1)    
        self.ventana1.after(60, self.check_inputs)          # activa un timer de 50mSeg.

     
    def agregarRegistroRFID(self):
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$impresion    $$$$$$$$$$$$$$$$$$$
        fechaEntro = datetime.today()
        fSTR=str(fechaEntro)
        corteNum = 0
        placa=str(self.Placa.get(), )                 
        datos=(fechaEntro, corteNum, placa)
        time.sleep(1)                            
        self.operacion1.altaRegistroRFID(datos) 
        MaxFolio=str(self.operacion1.MaxfolioEntrada())
        print("MaxFolio 1 ", MaxFolio)
        MaxFolio = MaxFolio.strip("[(,)]")
        print("MaxFolio 2 ", MaxFolio)
        n1 = MaxFolio
        print("n1 ", n1)
#        n2 = "1"
#        masuno = int(n1)+int(n2)
        masuno=n1
        print("masuno 1 ", masuno)
        masuno = str(masuno)
        print("masuno 2 ", masuno)
        self.MaxId.set(masuno)
        
        #folio_cifrado = self.operacion1.cifrar_folio(folio = masuno)
        
        #Generar QR
        #self.operacion1.generar_QR(folio_cifrado)


        imgqr=(fSTR + masuno) 
        horaentrada = str(fechaEntro)
        horaentrada=horaentrada[:16]
        #self.labelhr.configure(text=(horaentrada, "Entró"))
        fSTR=str(fechaEntro)
        print("fSTR ", fSTR)
        imgqr=(fSTR + masuno)
        print("imgqr ",imgqr)
        img = qrcode.make(fechaEntro)
        img = qrcode.make(imgqr)
        #Obtener imagen con el tamaño indicado
        reducida = img #.resize((100, 25))
        # Mostrar imagen reducida.show()
        # Guardar imagen obtenida con el formato JPEG
        reducida.save("reducida.png")
        f = open("reducida.png", "wb")
        img.save(f)
        f.close()
        #reducida2 =img2.resize((100, 75))
        #reducida2.save("reducida2.png")
        print("horaentrada",horaentrada)
        print("imgqr",imgqr)
        
        
        #p = Usb(0x04b8, 0x0202, 0)#0202 04b8:
        p = Usb(0x04b8, 0x0e28, 0)
        #p.set("center")
        #p.text("BOLETO DE ENTRADA\n")
        p.set("center")
        p.image("LOGO1.jpg")
        #p.set(font='b', height=4, align='right')
        p.set("center")
        p.text("\n")
        p.text("BOLETO DE ENTRADA\n")
        p.set(height=2, align='center')
        folioZZ=('FOLIO 000' + masuno)
        p.text(folioZZ+'\n')
        p.set("center")        
        p.text('Entro: '+horaentrada+'\n')
        #p.text('Monterrey No. 75'+placa+'\n')
        #p.text('Entrada (Durango)'+placa+'\n')
        p.set(align="center")
        #p.image("LOGO1.jpg")
        p.image("reducida.png")
        #p.image("AutoA.png")
        #p.text("            Le Atiende:               \n")
        p.text("--------------------------------------\n")
        p.text("--------------------------------------\n")
        p.text("--------------------------------------\n")
        p.text("                                      \n")
        p.text("                                      \n")
        p.text("                                      \n")
        p.text("                                      \n")
        p.cut()        
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$impresion fin$$$$$$$$$$$$$$$$               
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
                    io.output(barrera,0)#con un "0" abre la barrera
                    time.sleep (1)
                    io.output(barrera,1)
                    #io.output(out3,1)#con un "1" se apaga el led
                    self.NumTarjeta4.set("")               
                    self.entryNumTarjeta4.focus()
                




aplicacion1=FormularioOperacion()


