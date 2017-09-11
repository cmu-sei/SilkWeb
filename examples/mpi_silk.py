#! /usr/bin/python
import os
import sys
from mpi4py import MPI
comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()
os.environ["SILK_DATA_ROOTDIR"]="/data/silk/"
sys.path.append("/usr/lib/cgi-bin/silk")
import silkapi
a=silkapi.SilkAPI()
a.setup_args(None)
f_start = a.istart
f_end = a.iend
each = (f_end-f_start)/nprocs
for node in range(nprocs):
    if node == rank-1:
        a.istart = f_start + node*each
        a.iend = a.istart + each
        if node == nprocs:
            a.iend = f_end
        a.args.update({"mpi_node": rank, "istart": a.istart, "iend": a.iend})
        a.execute_query()
