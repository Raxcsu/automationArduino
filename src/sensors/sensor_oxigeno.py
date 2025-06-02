from .base_sensor import BaseSensor

class SensorOxigeno(BaseSensor):
    OX_MIN = 20.0
    OX_MAX = 25.0

    @classmethod
    def detectar_sensor(cls, linea: str):
        return any(tag in linea for tag in [';Ox;', ';Ox', 'Ox;'])

    def parsear_linea(self, linea: str):
        partes = linea.strip().split(';')
        return {
            'oxigeno': float(partes[4]),
            # 'temp': float(partes[7]),
            'salinidad': self.extraer_salinidad(linea)
        }

    def extraer_salinidad(self, linea: str):
        if "Sal = " in linea:
            inicio = linea.find("Sal = ") + len("Sal = ")
            fin = linea.find(" ", inicio)
            return float(linea[inicio:fin])
        return None