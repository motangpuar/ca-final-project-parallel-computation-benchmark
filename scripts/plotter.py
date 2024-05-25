import matplotlib.pyplot as plt

# Load the data from a text file
with open('bmark_np32_nrep1000.log', 'r') as file:
    document_content = file.read()

# Parse the data from the document content
data = {}
current_call = None

for line in document_content.split('\n'):
    if not line.startswith('#'):
        #print(line)
        current_call = line.strip()
        if current_call.startswith('MPI_'):
            print(current_call)
            test, _, nrep, runtime = current_call.split()
            if test not in data:
                data[test] = []
            data[test].append(float(runtime))
            print(data)

# Calculate mean, min, and max for each MPI call
mpi_calls = []
means = []
mins = []
maxs = []

for call, runtimes in data.items():
    mpi_calls.append(call)
    means.append(sum(runtimes) / len(runtimes))
    mins.append(min(runtimes))
    maxs.append(max(runtimes))

# Plot the data
print(mpi_calls)
x = range(len(mpi_calls))

plt.figure(figsize=(10, 6))
plt.plot(x, means, marker='o', label='Mean')
plt.plot(x, mins, marker='v', label='Min')
plt.plot(x, maxs, marker='^', label='Max')

plt.xticks(x, mpi_calls)
plt.xlabel('MPI Calls')
plt.ylabel('Runtime (sec)')
plt.title('MPI Performance Metrics')
plt.legend()

plt.tight_layout()
plt.savefig('hello.png')
