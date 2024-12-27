# Description: A simple quantum circuit that creates a superposition and entanglement between qubits.
# It's running on a real IBM quantum computer.

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
# >>> Job ID: cxmth1w6t010008d7efg
# >>> Job Status: QUEUED
# Results: {'000': 1014, '111': 1060, '101': 1040, '010': 931, '100': 18, '001': 8, '110': 16, '011': 9}
#
# Note that the states 100, 001, 110, and 011 shouldn't be in the result because the 1st and 3rd qubit aren't entangled there. It's caused by a noise in the real quantum computer.

# Import the necessary libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# Uncomment the following line to test the code on a simulator
# from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2  # for testing on a simulator with noise

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

# Get the least busy quantum computer
service = QiskitRuntimeService()
backend = service.least_busy(min_num_qubits=3, operational=True, simulator=False)
# Or use the following line to test the code on a simulator with noise
# backend = FakeAlmadenV2()  # for testing on a simulator

# Transpile the quantum circuit for the quantum computer
new_circuit = transpile(circuit, backend)

# Use Sampler to run the circuit
sampler = Sampler(backend, options={"default_shots": 4096})
job = sampler.run([new_circuit])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")

# Wait for the job to finish
print("Waiting for the job to finish...")
print("You can watch the status of the job on https://quantum.ibm.com/")

# Get and print the results
result = job.result()
# To get counts for a particular pub result, use
#
# pub_result = job_result[<idx>].data.<classical register>.get_counts()
#
# where <idx> is the index of the pub and <classical register> is the name of the classical register.
# You can use circuit.cregs to find the name of the classical registers.
pub_result = result[0]
counts = pub_result.data.c.get_counts()
print("Results:", counts)

# Create and display the histogram
plot_histogram(counts)
plt.show()  # This is needed to display the plot
