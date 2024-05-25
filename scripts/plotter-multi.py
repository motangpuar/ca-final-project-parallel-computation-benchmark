import matplotlib.pyplot as plt
import glob

# Get the list of files with incremental names
file_pattern = 'data/bmark_np*_nrep*.log'
files = sorted(glob.glob(file_pattern))

# Parse the data from each file
data = {}
for file_path in files:
    with open(file_path, 'r') as file:
        document_content = file.read()

    current_call = None
    for line in document_content.split('\n'):
        if not line.startswith('#'):
            current_call = line.strip()
            if current_call.startswith('MPI_'):
                test, _, nrep, runtime = current_call.split()
                if test not in data:
                    data[test] = []
                data[test].append(float(runtime))

# Calculate mean, min, and max for each MPI call
mpi_calls = list(data.keys())
means = {}
mins = {}
maxs = {}
for call in mpi_calls:
    means[call] = []
    mins[call] = []
    maxs[call] = []
    for i in range(len(files)):
        means[call].append(data[call][i * 1000] * 1000)  # Convert to milliseconds
        mins[call].append(min(data[call][i * 1000 : (i + 1) * 1000]) * 1000)  # Convert to milliseconds
        maxs[call].append(max(data[call][i * 1000 : (i + 1) * 1000]) * 1000)  # Convert to milliseconds

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
    plt.savefig(f'performance_metrics_{call}.png')
    plt.close()
