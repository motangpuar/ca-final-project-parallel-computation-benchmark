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
        means[call].append(data[call][i * 1000] * 1000)  # Convert to microseconds
        mins[call].append(min(data[call][i * 1000 : (i + 1) * 1000]) * 1000)  # Convert to microseconds
        maxs[call].append(max(data[call][i * 1000 : (i + 1) * 1000]) * 1000)  # Convert to microseconds

# Plot the data for each MPI call
processes = range(1, len(files) + 1)
for call in mpi_calls:
    plt.figure(figsize=(8, 6))
    plt.plot(processes, means[call], marker='o', linestyle='-', label=call)

    # Set the x-axis labels
    plt.xticks(processes, [str(i) for i in processes], rotation=45)
    plt.xlabel('Processes')

    # Set the y-axis label
    plt.ylabel('Time [us]')

    # Set the legend
    plt.legend()

    # Set the title
    plt.title('MPI Performance')

    # Add text annotations for specific data points
    plt.text(len(files), means[call][-1], f'{means[call][-1]:.2f}', ha='left', va='center')

    # Add text annotations for growth rates
    growth_rate = means[call][-1] / means[call][0]
    plt.text(len(files) / 2, means[call][len(files) // 2], f'{growth_rate:.2f}x', ha='center', va='bottom')

    # Adjust the plot layout
    plt.tight_layout()

    # Save the plot
    plt.savefig(f'performance_metrics_{call}.png', dpi=300)

    # Close the current figure
    plt.close()
