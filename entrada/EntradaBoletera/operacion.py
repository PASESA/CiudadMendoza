import pymysql
import random
import qrcode

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
        
    def altaRegistroRFID(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="insert into Entradas(Entrada, CorteInc, Placas) values (%s,%s,%s)"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()

    def MaxfolioEntrada(self):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="select max(id) from Entradas;"
        cursor.execute(sql)
        cone.close()
        return cursor.fetchall()[0][0]


 ####PENSIONADOS######
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

    def UpdPensionado(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="UPDATE Pensionados SET Estatus=%s WHERE id_cliente=%s"
        cursor.execute(sql, datos)
        cone.commit()
        cone.close()

    def MovsPensionado(self, datos):
        cone=self.abrir()
        cursor=cone.cursor()
        sql="INSERT INTO MovimientosPens(idcliente, num_tarjeta, Entrada, Estatus, Corte) values (%s,%s,%s,%s,%s)"
        cursor.execute(sql,datos)
        cone.commit()
        cone.close()

### Herramientas
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

        # # Imprime el número de folio cifrado (sólo para propósitos de depuración).
        # print(folio)

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


