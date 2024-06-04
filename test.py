class a:
    def __init__(self):
        
        self.minutos_dentro = 23
        self.horas_dentro = 5

        importe = 0

        # Calcula la tarifa y el importe a pagar
        if self.minutos_dentro == 0:
            cuarto_hora = 0
        elif self.minutos_dentro < 16 and self.minutos_dentro >= 1:
            cuarto_hora = 1
        elif self.minutos_dentro < 31 and self.minutos_dentro >= 16:
            cuarto_hora = 2
        elif self.minutos_dentro < 46 and self.minutos_dentro >= 31:
            cuarto_hora = 3
        elif self.minutos_dentro <= 59 and self.minutos_dentro >= 46:
            cuarto_hora = 4

        if self.horas_dentro <= 2:
            if self.horas_dentro == 2 and cuarto_hora == 0:
                importe = 5
            elif self.horas_dentro == 2 and cuarto_hora >= 0:
                importe = 10
            else:
                importe = 5

        # Calcula el importe a pagar según la tabla de precios
        elif 2 <= self.horas_dentro <= 4:
            if self.horas_dentro == 4 and cuarto_hora == 0:
                importe = 10
            elif self.horas_dentro == 4 and cuarto_hora >= 0:
                importe = 15
            else:
                importe = 10

        elif 4 < self.horas_dentro <= 6:
            if self.horas_dentro == 6 and cuarto_hora == 0:
                importe = 15
            elif self.horas_dentro == 6 and cuarto_hora >= 0:
                importe = 20
            else:
                importe = 15

        elif 6 < self.horas_dentro <= 8:
            if self.horas_dentro == 8 and cuarto_hora == 0:
                importe = 20
            elif self.horas_dentro == 8 and cuarto_hora >= 0:
                importe = 25
            else:
                importe = 20

        elif 8 < self.horas_dentro <= 10:
            if self.horas_dentro == 10 and cuarto_hora == 0:
                importe = 25
            elif self.horas_dentro == 10 and cuarto_hora >= 0:
                importe = 30
            else:
                importe = 25

        elif 10 < self.horas_dentro <= 12:
            if self.horas_dentro == 12 and cuarto_hora == 0:
                importe = 30
            elif self.horas_dentro == 12 and cuarto_hora >= 0:
                importe = 500
            else:
                importe = 30

        else:
            if self.horas_dentro == 12 and cuarto_hora == 0:
                importe = 30
            else:
                importe = 500

        print(importe)

a()