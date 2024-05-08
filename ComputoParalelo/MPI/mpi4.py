from mpi4 import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
sie = comm.Get_size()

