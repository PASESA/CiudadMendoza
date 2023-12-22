import pymysql

class Operacion:
    def __init__(self):
        self.host = "169.254.70.94"
        self.user = "Aurelio"
        self.password = "RG980320"
        self.database = "Parqueadero1"
    def abrir(self):
        conexion=pymysql.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.password,
                                 database=self.database)

        return conexion

    def consulta(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select Entrada, Salida, Placas from Entradas where id=%s"
       #sql="select descripcion, precio from articulos where codigo=%s"
        cursor.execute(sql, datos)
        cone.close()
        return cursor.fetchall()

    def ActualizaSalida(self,estatus):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="update Entradas set Placas = %s where id=%s;"
        #colocamos en entradas "Afuera" en campo Placas, para no permitir re-uso de boletos de salida
        cursor.execute(sql,estatus)
        cone.commit()
        cone.close()

 ####PENSIONADOS###### Actualizo el 16Julio22
    def ValidarPen(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="SELECT id_cliente FROM Pensionados WHERE Num_tarjeta=%s"
        cursor.execute(sql,datos)
        cone.close()
        return cursor.fetchall()
      
    def ConsultaPensionado(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="SELECT Fecha_vigencia, Estatus, Vigencia, Tolerancia FROM Pensionados where id_cliente=%s"
        cursor.execute(sql,datos)
        cone.close()
        return cursor.fetchall()

    def UpdMovsPens(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="UPDATE MovimientosPens SET Salida=%s, TiempoTotal =%s, Estatus=%s WHERE idcliente=%s and Salida is null"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()

    def UpdPens2(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="UPDATE Pensionados SET Estatus=%s WHERE id_cliente=%s"
        #sql = "update Entradas set CorteInc = %s, vobo = %s where TiempoTotal is not null and CorteInc=0;"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()


    def consultar_UpdMovsPens(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="SELECT	Entrada FROM MovimientosPens WHERE idcliente=%s and Salida is null"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()
        return cursor.fetchall()[0][0]


