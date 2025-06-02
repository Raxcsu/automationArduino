from .base_sensor import BaseSensor

class SensorPH(BaseSensor):
    PH_MIN = 7.4
    PH_MAX = 7.5

    @classmethod
    def detectar_sensor(cls, linea: str):
        return ";pH;" in linea

    def parsear_linea(self, linea: str):
        partes = linea.strip().split(';')
        return {
            'ph': float(partes[4]),
            'temp': float(partes[7])
        }
