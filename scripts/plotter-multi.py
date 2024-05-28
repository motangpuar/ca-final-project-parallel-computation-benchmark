import matplotlib.pyplot as plt
import glob
import numpy as np
import seaborn as sns

def generate_file_reprompi(master_data_array, calls, measure_type, metric, param):
    #points = range(1,49)

    for item in master_data_array:
        print(item)
        points = range(1,len(master_data_array[item])+1)
        print(points)

    filename = f"data/dump_{measure_type}.txt"
    with open(filename, "w") as file:
        for call in calls:
            data_array = master_data_array[call]
            file.write(f"PARAMETER {param}\n")
            file.write("POINTS " + " ".join(f"({p})" for p in points) + "\n")
            file.write(f"REGION {call}\n")
            file.write(f"METRIC {metric}\n")

            print(len(data_array))

            for i, value in enumerate(data_array):
                #print(i,value)
                file.write(f"DATA {value}\n")

    print(f"File '{filename}' generated successfully.")

def process_file_sort():
    # Get the list of files with incremental names
    file_pattern = 'data/sort_np*.log'
    files = sorted(glob.glob(file_pattern))

    print(files)

    data = {}

    data['radix'] = []
    data['qsort'] = []
    data['omp'] = []

    means = {}
    mins = {}
    maxs = {}
    for file_path in files:
        with open(file_path, 'r') as file:
            document_content = file.read()
        current_file = [] 
        current_call = None
        c_data = {}
        c_data['radix'] = []
        c_data['qsort'] = []
        c_data['omp'] = []
        for line in document_content.split('\n'):
            if len(line) > 0:
                _, _, sort_type, runtime = line.split()
                print(runtime)
                
                sort_type = sort_type[:-1]
                print(sort_type)
                c_data[sort_type].append(float(runtime))

        print(c_data)
        data['radix'].append(np.mean(c_data['radix']))
        data['qsort'].append(np.mean(c_data['qsort']))
        data['omp'].append(np.mean(c_data['omp']))

    metric = "time (s)"
    keys = list(data.keys())
    generate_file_reprompi(data, keys, "sort", metric, "Process Num")

def process_file_cppmafia():
    # Get the list of files with incremental names
    file_pattern = 'data/cppmafia_np*.log'
    files = sorted(glob.glob(file_pattern))

    print(files)

    data = {}

    data['min'] = []
    data['mean'] = []
    data['max'] = []
    for file_path in files:
        with open(file_path, 'r') as file:
            document_content = file.read()
        current_file = [] 
        current_call = None
        for line in document_content.split('\n'):
            if len(line) > 0:
                _, _, runtime, metric = line.split()
                current_file.append(float(runtime))
                print(current_file)
                print(len(current_file))
       
        #data['MAFIA'].append(sum(current_file)/len(current_file))
        data['mean'].append(np.mean(current_file))
        data['min'].append(np.min(current_file))
        data['max'].append(np.max(current_file))

    metric="time (s)"
    keys = list(data.keys())

    generate_file_reprompi(data, keys, "cppmafia", metric, "k")
    plot_cppmafia(data, files, metric)

def process_file_reprompi():
    # Get the list of files with incremental names
    file_pattern = 'data/bmark_np*_nrep*.log'
    files = sorted(glob.glob(file_pattern))
    
    print(files)
    
    # Parse the data from each file
    data = {}
    means = {}
    mins = {}
    maxs = {}
    for file_path in files:
        with open(file_path, 'r') as file:
            document_content = file.read()
    
        current_call = None
        for line in document_content.split('\n'):
            if line.startswith('#@nprocs'):
                print(line)
                index = line.split('=')
                print(index[1])
            if not line.startswith('#'):
                current_call = line.strip()
                if current_call.startswith('MPI_'):
                    test, _, nrep, valid_nrep, mean_runtime, min_runtime, max_runtime = current_call.split()
                    print(min_runtime)
                    if test not in means:
                        means[test] = []
                    if test not in mins:
                        mins[test] = []
                    if test not in maxs:
                        maxs[test] = []
                    means[test].append(float(mean_runtime)*1*1000)
                    mins[test].append(float(min_runtime)*1*1000)
                    maxs[test].append(float(max_runtime)*1*1000)
                    print(means)
    
    mpi_calls = list(means.keys())
    metric = "time (ms)"
    generate_file_reprompi(mins, mpi_calls, "reprompi_min", metric, "Process Num")
    generate_file_reprompi(means, mpi_calls, "reprompi_mean", metric, "Process Num")
    generate_file_reprompi(maxs, mpi_calls, "reprompi_max", metric, "Process Num")

    plot_reprompi(mins, means, maxs, files)

def plot_cppmafia(data, files, metric):

    index = list(data.keys())
    
    # Plot the data for each MPI call
    x = range(1, len(files)+1)
    x_ticks = list(range(1, len(files), 8))
    x_ticks.append(len(files))
    
    print(data)
    plt.figure(figsize=(16, 12))
    #sns.set_theme(palette="Blues")
    i=1
    for call in data:
    
        # Plot means
        plt.subplot(len(data), 1, i)
        plt.grid(True)
        plt.plot(x, data[call], marker='o', label='Mean')
        plt.xticks(x_ticks)
        plt.xlabel('k')
        plt.ylabel(metric)
        plt.title(f'{call} Runtime')
        plt.legend()

        i=i+1


    plt.tight_layout()
    plt.savefig(f'plots/performance_metrics_MAFIA.png')
    plt.close()

def plot_reprompi(mins, means, maxs, files):

    mpi_calls = list(means.keys())
    
    # Plot the data for each MPI call
    x = range(1, len(files)+1)
    x_ticks = list(range(1, len(files), 6))
    x_ticks.append(len(files))
    
    for call in mpi_calls:
        
    
        plt.figure(figsize=(8, 8))
        sns.set_theme(style="whitegrid", palette="pastel")
        # Plot means
        plt.subplot(3, 1, 1)
        plt.plot(x, means[call], marker='o', label='Mean')
        plt.grid(True)
        plt.xticks(x_ticks)
        plt.xlabel('Process Number')
        plt.ylabel('Runtime (us)')
        plt.title(f'{call} - Mean Runtime')
        plt.legend()
        
        # Plot mins
        plt.subplot(3, 1, 2)
        plt.plot(x, mins[call], marker='v', label='Min')
        plt.grid(True)
        plt.xticks(x_ticks)
        plt.xlabel('Process Number')
        plt.ylabel('Runtime (us)')
        plt.title(f'{call} - Min Runtime')
        plt.legend()
        
        # Plot maxs
        plt.subplot(3, 1, 3)
        plt.plot(x, maxs[call], marker='^', label='Max')
        plt.grid(True)
        plt.xticks(x_ticks)
        plt.xlabel('Process Number')
        plt.ylabel('Runtime (us)')
        plt.title(f'{call} - Max Runtime')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f'plots/performance_metrics_{call}.png')
        plt.close()

#process_file_reprompi()
process_file_cppmafia()
#process_file_sort()
