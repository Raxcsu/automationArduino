from sensors.sensor_ph import SensorPH
from sensors.sensor_oxigeno import SensorOxigeno
from manager import Manager

sensores = [
    SensorPH("C212631040"),
    SensorPH("C212631035"),
    SensorOxigeno("11151020"),
    SensorOxigeno("18481464"),
]

manager = Manager(sensores)
manager.run()


