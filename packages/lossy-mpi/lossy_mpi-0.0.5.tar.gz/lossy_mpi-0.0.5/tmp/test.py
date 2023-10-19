from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
 
x = list()

x.append((0, 1))

x = comm.reduce(x)

if rank == 0:
    print(x)
    x=[1]
    import numpy as np
    print(np.zeros_like(x)+0.4)
