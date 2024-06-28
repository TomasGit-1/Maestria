
from RedNeuronalModel import RedNeuronalModel
from utils import generateSample, paintXYPlot, downloadDatasets

from colorlog import ColoredFormatter
from sklearn.model_selection import train_test_split
import logging
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

    epochs =100
    nameDataset = "balance"
    X, y = downloadDatasets(logger, nameDataset)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    nameDataset = "balance"
    X, y = downloadDatasets(logger, nameDataset)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    nn = RedNeuronalModel(logger,X_train, y_train)
    nn.train(epochs)

    predictions = nn.predict()
    print("Predicciones:")
    print(predictions)
  


