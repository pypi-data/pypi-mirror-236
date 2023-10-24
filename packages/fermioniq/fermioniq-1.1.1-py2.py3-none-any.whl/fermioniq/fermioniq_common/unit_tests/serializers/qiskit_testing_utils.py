import random
from typing import Sequence, Union

import numpy as np
import qiskit
import scipy as sp


def add_qiskit_gate(
    circuit: qiskit.QuantumCircuit,
    qubit_indices: Union[None, Sequence[int]] = None,
    gate_index: Union[None, int] = None,
):
    """
    add a gate to a Qiskit Circuit

    :param circuit: qiskit.QuantumCircuit:
        A circuit from Qiskit to add a gate to

    :param qubit_index: int
        The index of the qubit to add the gate to. If None,
        the gate is applied to a random qubit(s) in the circuit.
        Default is None

    :param gate_index: int
        an integer specifying which gate to add. See below in the code which integer
        corresponds to which gate. If None, a random gate is applied to the qubit
        Default is None
    """

    N_q = circuit.num_qubits
    assert N_q > 0, "circuit must have at least one qubit"
    assert isinstance(
        circuit, qiskit.QuantumCircuit
    ), "circuit must be a qiskit.QuantumCircuit"

    if gate_index is None:
        # Generate a random gate index
        gate_index = np.random.randint(0, 100000)
    else:
        assert isinstance(gate_index, int), "gate_index must be an integer"

    # Make sure the gate index is in the correct range for the number of qubits in the circuit
    if N_q == 1:
        gate_index %= 15
    elif N_q == 2:
        gate_index %= 28
    elif N_q == 3:
        gate_index %= 33
    elif N_q >= 4:
        gate_index %= 36

    # Generate a random qubit index if qubit_index is None
    if qubit_indices is None:
        all_qubit_indices = list(range(N_q))
        if gate_index < 15:
            qubit_indices = random.sample(all_qubit_indices, 1)
        elif 15 <= gate_index < 28:
            qubit_indices = random.sample(all_qubit_indices, 2)
        elif 28 <= gate_index < 33:
            qubit_indices = random.sample(all_qubit_indices, 3)
        elif 33 <= gate_index < 36:
            qubit_indices = random.sample(all_qubit_indices, 4)
    # Make sure the qubit index is in the correct range for the number of qubits in the circuit
    else:
        assert all(
            [isinstance(qubit_index, int) for qubit_index in qubit_indices]
        ), "qubit_indices must be a list of integers"
        assert all(
            [0 <= qubit_index < N_q for qubit_index in qubit_indices]
        ), "qubit_indices must be in the range [0, N_q)"
        assert len(set(qubit_indices)) == len(
            qubit_indices
        ), "qubit_indices must be unique"

    # 1-qubit gates
    if gate_index == 0:
        circuit.x(*qubit_indices)
    elif gate_index == 1:
        circuit.y(*qubit_indices)
    elif gate_index == 2:
        circuit.z(*qubit_indices)
    elif gate_index == 3:
        circuit.h(*qubit_indices)
    elif gate_index == 4:
        circuit.s(*qubit_indices)
    elif gate_index == 5:
        circuit.sdg(*qubit_indices)
    elif gate_index == 6:
        circuit.t(*qubit_indices)
    elif gate_index == 7:
        circuit.tdg(*qubit_indices)
    elif gate_index == 8:
        circuit.rx(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 9:
        circuit.ry(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 10:
        circuit.rz(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 11:
        circuit.u(*np.random.uniform(0, 2 * np.pi, 3), *qubit_indices)
    elif gate_index == 12:
        circuit.p(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 13:
        U = sp.stats.unitary_group.rvs(2).tolist()
        circuit.unitary(U, qubit_indices)
    elif gate_index == 14:
        circuit.id(qubit_indices)

    # 2-qubit gates
    elif gate_index == 15:
        circuit.swap(*qubit_indices)
    elif gate_index == 16:
        circuit.cx(*qubit_indices)
    elif gate_index == 17:
        circuit.cz(*qubit_indices)
    elif gate_index == 18:
        circuit.ch(*qubit_indices)
    elif gate_index == 19:
        circuit.crz(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 20:
        circuit.crx(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 21:
        circuit.cry(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 22:
        circuit.cu(*np.random.uniform(0, 2 * np.pi, 4), *qubit_indices)
    elif gate_index == 23:
        circuit.rxx(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 24:
        circuit.ryy(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 25:
        circuit.rzz(np.random.uniform(0, 2 * np.pi), *qubit_indices)
    elif gate_index == 26:
        U = sp.stats.unitary_group.rvs(4).tolist()
        circuit.unitary(U, qubit_indices)
    elif gate_index == 27:
        circuit.id(qubit_indices)

    # 3-qubit gates
    elif gate_index == 28:
        circuit.ccx(*qubit_indices)
    elif gate_index == 29:
        circuit.cswap(*qubit_indices)
    elif gate_index == 30:
        circuit.rccx(*qubit_indices)
    elif gate_index == 31:
        U = sp.stats.unitary_group.rvs(8).tolist()
        circuit.unitary(U, qubit_indices)
    elif gate_index == 32:
        circuit.id(qubit_indices)

    # 4-qubit gates
    elif gate_index == 33:
        circuit.rcccx(*qubit_indices)
    elif gate_index == 34:
        U = sp.stats.unitary_group.rvs(2).tolist()
        circuit.unitary(U, qubit_indices)
    elif gate_index == 35:
        circuit.id(qubit_indices)

    return circuit


def random_qiskit_circuit(n_qubits: int = 5, n_gates: int = 100):

    circuit = qiskit.QuantumCircuit(n_qubits)
    for _ in range(n_gates):
        circuit = add_qiskit_gate(circuit)
    return circuit
