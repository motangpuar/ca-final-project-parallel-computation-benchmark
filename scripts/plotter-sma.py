import matplotlib.pyplot as plt
import glob
import numpy as np

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

# Apply SMA to the data
window_size = 10  # Adjust the window size as needed
sma_means = {}
sma_mins = {}
sma_maxs = {}
for call in mpi_calls:
    sma_means[call] = np.convolve(means[call], np.ones(window_size) / window_size, mode='valid')
    sma_mins[call] = np.convolve(mins[call], np.ones(window_size) / window_size, mode='valid')
    sma_maxs[call] = np.convolve(maxs[call], np.ones(window_size) / window_size, mode='valid')

# Create smooth data points for plotting
smooth_factor = 1000  # Adjust the smooth factor as needed
processes = range(1, len(files) + 1)
smooth_processes = np.linspace(1, len(files), len(files) * smooth_factor)

for call in mpi_calls:
    plt.figure(figsize=(8, 6))

    # Interpolate the data for a smoother curve
    smooth_means = np.interp(smooth_processes, processes, means[call])
    smooth_sma_means = np.interp(smooth_processes[window_size-1:], processes[window_size-1:], sma_means[call])

    plt.plot(smooth_processes, smooth_means, linestyle='-', label=call, alpha=0.3)
    plt.plot(smooth_processes[window_size-1:], smooth_sma_means, linestyle='-', label=f'{call} (SMA)', linewidth=2)

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
    plt.text(len(files), sma_means[call][-1], f'{sma_means[call][-1]:.2f}', ha='left', va='center')

    # Add text annotations for growth rates
    growth_rate = means[call][-1] / means[call][0]
    plt.text(len(files) / 2, means[call][len(files) // 2], f'{growth_rate:.2f}x', ha='center', va='bottom')

    # Adjust the plot layout
    plt.tight_layout()

    # Save the plot
    plt.savefig(f'plots/performance_metrics_{call}_smooth.png', dpi=300)

    # Close the current figure
    plt.close()
