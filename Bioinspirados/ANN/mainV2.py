
from colorlog import ColoredFormatter
from utils import generateSample
import logging
from RedNeuronalModel import RedNeuronalModel
import numpy as np
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


if __name__ == '__main__':
    logger.info("Hello World")
    logger.info("Datasets")
    n_features = 5
    n_classes = 2
    X, y = generateSample(n_features=n_features, n_classes=n_classes)
    # Datos de entrenamiento (XOR)
    X = np.array([[0, 0],
                [0, 1],
                [1, 0],
                [1, 1]])

    Y = np.array([[0],
                [1],
                [1],
                [0]])

    # Hiperparámetros
    input_size = 2
    hidden_size = 3
    output_size = 1
    connectivity = 0.5  # 50% de conectividad
    learning_rate = 0.1
    epochs = 10000

    # Crear y entrenar la red neuronal
    nn = RedNeuronalModel(input_size, hidden_size, output_size, connectivity, learning_rate)
    nn.train(X, Y, epochs)

    # Predicción
    predictions = nn.predict(X)
    print("Predicciones:")
    print(predictions)
  


