import matplotlib.pyplot as plt
import glob

# for call in mpi_calls:
#     print(call)
#     print(len(mins[call]))
#     generate_file(mins[call], call, "time")

def generate_file(master_data_array, calls, measure_type):
    metric="time"
    points = range(1,37)
    filename = f"data/dump_{measure_type}.txt"
    with open(filename, "w") as file:
        for call in calls:
            data_array = master_data_array[call]
            file.write(f"PARAMETER p\n")
            file.write("POINTS " + " ".join(f"({p})" for p in points) + "\n")
            file.write(f"REGION {call}\n")
            file.write(f"METRIC {metric}\n")

            for i, value in enumerate(data_array):
                #print(i,value)
                file.write(f"DATA {value}\n")

    print(f"File '{filename}' generated successfully.")


# Get the list of files with incremental names
file_pattern = 'data/bmark_np*_nrep*.log'
files = sorted(glob.glob(file_pattern))

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
                means[test].append(float(mean_runtime))
                mins[test].append(float(min_runtime))
                maxs[test].append(float(max_runtime))
                print(means)

# Calculate mean, min, and max for each MPI call
mpi_calls = list(means.keys())
#print(mpi_calls)
# means = {}
# mins = {}
# maxs = {}
# for call in mpi_calls:
#     print(f"{call}: {len(data[call])}")
#     means[call] = []
#     mins[call] = []
#     maxs[call] = []
#     for i in range(len(files)):
#         means[call].append(sum(data[call][i * 1000 : (i + 1) * 1000])/len(files))  # Convert to milliseconds
#         mins[call].append(min(data[call][i * 1000 : (i + 1) * 1000]))  # Convert to milliseconds
#         maxs[call].append(max(data[call][i * 1000 : (i + 1) * 1000]))  # Convert to milliseconds
# 
#     print(f"{call}-mean: {len(means[call])}")


print(mins)

generate_file(mins, mpi_calls, "min")
generate_file(means, mpi_calls, "mean")
generate_file(maxs, mpi_calls, "max")


# Plot the data for each MPI call
x = range(1, len(files) + 1)

for call in mpi_calls:
    plt.figure(figsize=(8, 8))
    
    # Plot means
    plt.subplot(3, 1, 1)
    plt.plot(x, means[call], marker='o', label='Mean')
    plt.xticks(x, rotation=45)
    plt.xlabel('Process Number')
    plt.ylabel('Runtime (ms)')
    plt.title(f'{call} - Mean Runtime')
    plt.legend()
    
    # Plot mins
    plt.subplot(3, 1, 2)
    plt.plot(x, mins[call], marker='v', label='Min')
    plt.xticks(x, rotation=45)
    plt.xlabel('Process Number')
    plt.ylabel('Runtime (ms)')
    plt.title(f'{call} - Min Runtime')
    plt.legend()
    
    # Plot maxs
    plt.subplot(3, 1, 3)
    plt.plot(x, maxs[call], marker='^', label='Max')
    plt.xticks(x, rotation=45)
    plt.xlabel('Process Number')
    plt.ylabel('Runtime (ms)')
    plt.title(f'{call} - Max Runtime')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'plots/performance_metrics_{call}.png')
    plt.close()
