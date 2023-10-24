import numpy as np
from qiskit import QuantumCircuit


def qiskit_bell_pair() -> QuantumCircuit:
    circuit = QuantumCircuit(2)
    circuit.x(0)
    circuit.h(0)
    circuit.cx(0, 1)
    return circuit
