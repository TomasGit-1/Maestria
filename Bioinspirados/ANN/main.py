from ANNC import ANNC
from utils import configrationLogger, downloadDatasets

if __name__ == "__main__":
    log = configrationLogger()
    nameDataset = "balance"
    X, y = downloadDatasets(log, nameDataset)
    objANNC = ANNC(log)
    objANNC.train()
