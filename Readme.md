# Final Project Setup

## Hosts Lists:

| Node | hostname  | IP | CPU | 
| --- | --- | --- | --- | 
| Master+Worker | MPI-00 | 10.21.0.10 | 2 |
| Worker | MPI-01 | 10.21.0.107 | 2 |
| Worker | MPI-02 | 10.21.0.108 | 2 |
| Worker | MPI-03 | 10.21.0.109 | 2 |
| Worker | MPI-04 | 10.21.0.104 | 2 |
| Worker | MPI-05 | 10.21.0.105 | 2 |

## RepromMPI

> **Ubuntu 20.04**
> - Install Cmake >  v3.22.0
> - Install `libgsl-dev`
 

1. Test Mpirun

	```bash
	mpirun bin/mpibenchmark -np 32 --msizes-list=800 --calls-list=MPI_Allgather --nrep 1
	```


2. Bash script `scripts/runner/sh` will generate the model data
3. Python script `scripts/plot-multi.py` will generate the extra-p data
