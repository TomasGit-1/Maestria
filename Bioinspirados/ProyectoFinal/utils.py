from colorlog import ColoredFormatter
from ucimlrepo import fetch_ucirepo 
import pandas as pd
import logging
import numpy as np

def configrationLogger():
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
    return logger

def downloadDatasets(log, key):  
    datasets = {
        "balance":12,    #1 Tomy
        "glass":42,      #2 Mirim
        "ionosphere":52, #3 Miriam
        "irisplant":53,  #4 Aide
        "wine":109,      #5 Aide
        "BCW": 15        #6 Tomy
    }
    log.warning("Espera un momento estamos descargando")
    data = fetch_ucirepo(id = datasets[key]) 
    X = data.data.features 
    y = data.data.targets 
    columClass = y.columns.tolist()
    if y[columClass[0]].dtype == 'object':
        y["classification"] = pd.Categorical(y[columClass[0]])
        y["classification"] = y["classification"].cat.codes
    else:
        y['classification'] = y[columClass[0]]
    log.warning("Terminamos la descargar")
    if isinstance(X, pd.DataFrame):
        X =X.to_numpy()
    if isinstance(y, pd.DataFrame):
        y =np.array(y["classification"].tolist())
    return X, y

