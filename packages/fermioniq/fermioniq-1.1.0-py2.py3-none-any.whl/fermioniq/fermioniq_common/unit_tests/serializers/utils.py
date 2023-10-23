import numpy as np


def n_qubits_n_gates_generator(n_circuits):
    for _ in range(n_circuits):
        n_qubits = np.random.randint(1, 24)
        n_gates = np.random.randint(0, 100)
        yield n_qubits, n_gates
