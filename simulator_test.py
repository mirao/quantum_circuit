# Description: A simple quantum circuit that creates a superposition and entanglement between qubits.
# It's running on a simulator that doesn't have noise.

# Example output:
#
# Quantum circuit:
#      ┌───┐        ┌─┐
# q_0: ┤ H ├──■─────┤M├───
#      ├───┤  │  ┌─┐└╥┘
# q_1: ┤ H ├──┼──┤M├─╫────
#      └───┘┌─┴─┐└╥┘ ║ ┌─┐
# q_2: ─────┤ X ├─╫──╫─┤M├
#           └───┘ ║  ║ └╥┘
# c: 3/═══════════╩══╩══╩═
#                 1  0  2
# Results: {'111': 1019, '101': 1062, '010': 993, '000': 1022}

# Import the necessary libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator  # for simulation
from qiskit import transpile  # for transpiling the circuit
from qiskit.visualization import plot_histogram  # for plotting the results
import matplotlib.pyplot as plt  # you'll need this for displaying the plot

# Create a quantum circuit
qreg = QuantumRegister(3, "q")  # three qubits
creg = ClassicalRegister(3, "c")  # three classical bits to measure the qubits
circuit = QuantumCircuit(qreg, creg)

# Apply Hadamard gate to the first two qubits
circuit.h(qreg[0])
circuit.h(qreg[1])

# Apply CNOT gate to the first and the third qubit
circuit.cx(qreg[0], qreg[2])

# Measure the qubits
circuit.measure(qreg, creg)

# Print the quantum circuit
print("Quantum circuit:")
print(circuit)

# Simulate the quantum circuit
backend = AerSimulator()
new_circuit = transpile(circuit, backend)
job = backend.run(new_circuit, shots=4096)

# Get and print the results
result = job.result()
counts = result.get_counts(circuit)
print("Results:", counts)

# Create and display the histogram
plot_histogram(counts)
plt.show()  # This is needed to display the plot
