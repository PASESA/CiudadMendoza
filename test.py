class a:
    def __init__(self, horas_dentro, minutos_dentro):
        self.horas_dentro = horas_dentro
        self.minutos_dentro = minutos_dentro

    def calcular_importe(self):
        # Determina el cuarto de hora
        if self.minutos_dentro == 0:
            cuarto_hora = 0
        elif 1 <= self.minutos_dentro < 16:
            cuarto_hora = 1
        elif 16 <= self.minutos_dentro < 31:
            cuarto_hora = 2
        elif 31 <= self.minutos_dentro < 46:
            cuarto_hora = 3
        elif 46 <= self.minutos_dentro <= 59:
            cuarto_hora = 4

        # Determina el importe base según las horas y cuartos de hora
        if self.horas_dentro < 2 or (self.horas_dentro == 2 and cuarto_hora == 0):
            importe = 5
        else:
            horas_completas = self.horas_dentro
            if cuarto_hora > 0:
                horas_completas += 1
            
            if horas_completas % 2 == 0:
                horas_completas -= 1

            importe = 5 + ((horas_completas - 1) // 2) * 5
        
        return importe

file = open('TestTarifa.py', "w", encoding="UTF-8")
code = """import unittest
from test import a

class TestCobroController(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)\n"""
file.write(code)

for hour in range(25):  # Incluye 24 horas completas
    for minutos_dentro in range(0, 60):
        importe = 0

        if minutos_dentro == 0:
            cuarto_hora = 0
        elif 1 <= minutos_dentro < 16:
            cuarto_hora = 1
        elif 16 <= minutos_dentro < 31:
            cuarto_hora = 2
        elif 31 <= minutos_dentro < 46:
            cuarto_hora = 3
        elif 46 <= minutos_dentro <= 59:
            cuarto_hora = 4

        # Determina el importe base según las horas y cuartos de hora
        if hour < 2 or (hour == 2 and cuarto_hora == 0):
            importe = 5
        else:
            horas_completas = hour
            if cuarto_hora > 0:
                horas_completas += 1
            
            if horas_completas % 2 == 0:
                horas_completas -= 1

            importe = 5 + ((horas_completas - 1) // 2) * 5

        if hour > 24:
            importe = 65

        code = f"""
    def test_{hour}_horas_{minutos_dentro}_minutos(self):
        instancia = a({hour}, {minutos_dentro})
        self.assertEqual(instancia.calcular_importe(), {importe})\n"""

        file.write(code)

code = """
def run_code():
    unittest.main()\n\n    
"""
file.write(code)

code = """
if __name__ == '__main__':
    run_code()\n\n"""
file.write(code)

file.close()
