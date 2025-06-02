import logging
import os

def configurar_logger(nombre='sensor_logger', archivo='logs/sensores.log'):
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(archivo)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(fh)

    return logger