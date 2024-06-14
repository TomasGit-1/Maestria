from PGenetica import PGenetica
from binarytree import Node,build
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
sie = comm.Get_size()


