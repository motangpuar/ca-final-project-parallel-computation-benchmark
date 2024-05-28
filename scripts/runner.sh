#!/bin/bash

# Define the list of process numbers

# Define the number of repetitions
nrep=1000
totalCPU=48

# Iterate over the process numbers
function bmark_mpi() {
    for num in {001..48};
    do
        # Generate the output file name
        output_file="bmark_np${num}_nrep${nrep}.log"
    
        # Run the MPI benchmark
        mpirun -np $num -hostfile mpi_hosts.conf ~/mpi_shared/ca-final-project/reprompi/bin/mpibenchmark \
            --msizes-list=800 \
            --nrep=$nrep \
            --calls-list=MPI_Allgather,MPI_Allreduce,MPI_Barrier,MPI_Bcast,MPI_Reduce,MPI_Gather,MPI_Alltoall \
            --summary=mean,min,max >| data/$output_file
            #--output=data/$output_file
        echo -e "[*] Generated ${output_file}"
        sleep 1
    done
}

function bmark_cppmafia() {
    for num in {002..20};
    do
        # Generate the output file name
        output_file="cppmafia_np${num}.log"
        mpiexec -np 1 -hostfile mpi_hosts.conf \
            ~/mpi_shared/ca-final-project/gpumafia/cppmafia/bin/cppmafia --timing ~/mpi_shared/ca-final-project/gpumafia/utils/clugen/cluster-test/cluster-$num.dat | grep total >| data/$output_file
        echo -e "[*] Generated ${output_file}"
        #sleep 1
    done
    
}

function bmark_sort() {
    for num in {001..48};
    do
        # Generate the output file name
        output_file="sort_np${num}.log"
        mpiexec -np $num -hostfile mpi_hosts.conf \
            ~/mpi_shared/ca-final-project/MP-sort/main 100000 | grep time >| data/$output_file
        echo -e "[*] Generated ${output_file}"
        sleep 2
    done
    
}

bmark_cppmafia
#bmark_sort
#bmark_mpi
