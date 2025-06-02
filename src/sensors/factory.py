from .sensor_ph import SensorPH
from .sensor_oxigeno import SensorOxigeno

class SensorFactory:
    TIPOS_SENSORES = [SensorPH, SensorOxigeno]

    @classmethod
    def crear_sensor(cls, linea: str):
        for sensor_class in cls.TIPOS_SENSORES:
            if sensor_class.detectar_sensor(linea):
                codigo_sensor = cls.extraer_codigo_sensor(linea)
                return sensor_class(codigo_sensor)
        return None

    @staticmethod
    def extraer_codigo_sensor(linea: str):
        partes = linea.strip().split(';')
        # print(partes[-2].strip())
        return partes[-2].strip()  # Último valor como código del sensor