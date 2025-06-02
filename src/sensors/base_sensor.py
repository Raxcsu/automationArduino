class BaseSensor:
    def __init__(self, codigo_sensor: str):
        self.codigo_sensor = codigo_sensor

    @classmethod
    def detectar_sensor(cls, linea: str):
        raise NotImplementedError

    def parsear_linea(self, linea: str):
        raise NotImplementedError