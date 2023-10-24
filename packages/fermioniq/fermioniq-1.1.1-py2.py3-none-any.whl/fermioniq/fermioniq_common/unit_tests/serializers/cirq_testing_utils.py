import random
import uuid
from typing import Sequence, Union

import cirq
import numpy as np
import scipy as sp


def add_cirq_gate(
    circuit: cirq.Circuit,
    all_circuit_qubits: Sequence[
        Union[cirq.LineQubit, cirq.GridQubit, cirq.NamedQubit]
    ],
    qubit_indices: Union[Sequence[int], None] = None,
    gate_index: Union[None, int] = None,
):
    """
    Add a Cirq gate to a cirq circuit.

    :param circuit: cirq.Circuit
        The circuit to add the gate to

    :param qubit_indices: Union[Sequence[int], None]
        The qubits to add the gate to. If None, the gate is applied to a random qubit(s) in the circuit.

    :param gate_index: int
        The index of the gate to add. See the code in this function to determine which gate is applied If None, a random gate is applied.
    """
    N_q = len(all_circuit_qubits)

    assert N_q > 0

    if gate_index is None:
        # Generate a random gate index
        gate_index = np.random.randint(0, 100000)
    else:
        assert isinstance(gate_index, int), "gate_index must be an integer"

    if N_q == 1:
        gate_index %= 16
    elif N_q == 2:
        gate_index %= 30
    elif N_q >= 3:
        gate_index %= 35

    if qubit_indices is None:
        all_qubit_indices = list(range(N_q))
        if gate_index <= 16:
            qubit_indices = random.sample(all_qubit_indices, 1)
        elif gate_index <= 30:
            qubit_indices = random.sample(all_qubit_indices, 2)
        elif gate_index <= 35:
            qubit_indices = random.sample(all_qubit_indices, 3)

    else:
        # assert isinstance(qubit_ids, Sequence), "qubit_ids must be a sequence"
        # assert len(qubit_ids) > 0, "qubit_ids must be non-empty"
        # assert all([isinstance(q, cirq.Qid) for q in qubit_ids]), "qubit_ids must be a sequence of cirq.Qid"
        # assert all([q in all_qubits for q in qubit_ids]), "qubit_ids must be a subset of the qubits in the circuit"
        # assert len(set(qubit_ids)) == len(qubit_ids), "qubit_ids must be unique"
        assert all(
            [0 <= q_i < N_q for q_i in qubit_indices]
        ), "qubit_indices must be a subset of the qubits in the circuit"

    qubits = [all_circuit_qubits[i] for i in qubit_indices]

    # 1 qubit gates
    if gate_index == 1:
        circuit.append(cirq.H(*qubits))
    elif gate_index == 2:
        circuit.append(cirq.X(*qubits))
    elif gate_index == 3:
        circuit.append(cirq.Y(*qubits))
    elif gate_index == 4:
        circuit.append(cirq.Z(*qubits))
    elif gate_index == 5:
        circuit.append(cirq.S(*qubits))
    elif gate_index == 6:
        circuit.append(cirq.T(*qubits))
    elif gate_index == 7:
        circuit.append(cirq.XPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 8:
        circuit.append(cirq.YPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 9:
        circuit.append(cirq.ZPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 10:
        circuit.append(cirq.HPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 11:
        circuit.append(cirq.rx(rads=np.random.uniform(0, 2 * np.pi)).on(*qubits))
    elif gate_index == 12:
        circuit.append(cirq.ry(rads=np.random.uniform(0, 2 * np.pi)).on(*qubits))
    elif gate_index == 13:
        circuit.append(cirq.rz(rads=np.random.uniform(0, 2 * np.pi)).on(*qubits))
    elif gate_index == 14:
        circuit.append(
            cirq.PhasedXPowGate(
                exponent=np.random.uniform(0, 2), phase_exponent=np.random.uniform(0, 2)
            ).on(*qubits)
        )
    elif gate_index == 15:
        circuit.append(
            cirq.PhasedXZGate(
                x_exponent=np.random.uniform(0, 2),
                z_exponent=np.random.uniform(0, 2),
                axis_phase_exponent=np.random.uniform(0, 2),
            ).on(*qubits)
        )
    elif gate_index == 16:
        U = sp.stats.unitary_group.rvs(2)
        gate = cirq.MatrixGate(U)
        circuit.append(gate.on(*qubits))

    # 2-qubit gates
    elif gate_index == 17:
        circuit.append(cirq.CNOT(*qubits))
    elif gate_index == 18:
        circuit.append(cirq.CZ(*qubits))
    elif gate_index == 19:
        circuit.append(cirq.SWAP(*qubits))
    elif gate_index == 20:
        circuit.append(cirq.ISWAP(*qubits))
    elif gate_index == 21:
        circuit.append(cirq.CZPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 22:
        circuit.append(cirq.CNotPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 23:
        circuit.append(cirq.SwapPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 24:
        circuit.append(cirq.ISwapPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 25:
        circuit.append(cirq.XXPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 26:
        circuit.append(cirq.YYPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 27:
        circuit.append(cirq.ZZPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 28:
        circuit.append(
            cirq.FSimGate(
                theta=np.random.uniform(0, 2), phi=np.random.uniform(0, 2)
            ).on(*qubits)
        )
    elif gate_index == 29:
        circuit.append(
            cirq.PhasedFSimGate(
                theta=np.random.uniform(0, 2),
                zeta=np.random.uniform(0, 2),
                chi=np.random.uniform(0, 2),
                gamma=np.random.uniform(0, 2),
                phi=np.random.uniform(0, 2),
            ).on(*qubits)
        )
    elif gate_index == 30:
        U = sp.stats.unitary_group.rvs(4)
        gate = cirq.MatrixGate(U)
        circuit.append(gate.on(*qubits))

    # 3-qubit gates
    elif gate_index == 31:
        circuit.append(cirq.CCX(*qubits))
    elif gate_index == 32:
        circuit.append(cirq.CCNOT(*qubits))
    elif gate_index == 33:
        circuit.append(cirq.TOFFOLI(*qubits))
    elif gate_index == 34:
        circuit.append(cirq.CCXPowGate(exponent=np.random.uniform(0, 2)).on(*qubits))
    elif gate_index == 35:
        U = sp.stats.unitary_group.rvs(8)
        gate = cirq.MatrixGate(U)
        circuit.append(gate.on(*qubits))

    return circuit


def random_line_qubits_cirq_circuit(n_qubits: int = 5, n_gates: int = 100):
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(n_qubits)
    for _ in range(n_gates):
        circuit = add_cirq_gate(circuit, qubits)
    return circuit


def random_grid_qubits_cirq_circuit(
    n_rows: int = 2, n_cols: int = 2, n_gates: int = 100
):
    circuit = cirq.Circuit()
    qubits = cirq.GridQubit.rect(n_rows, n_cols)
    for _ in range(n_gates):
        circuit = add_cirq_gate(circuit, qubits)
    return circuit


def random_named_qubits_cirq_circuit(n_qubits: int = 5, n_gates: int = 100):
    circuit = cirq.Circuit()

    random_strings = [uuid.uuid4().hex for i in range(n_qubits)]

    qubits = [cirq.NamedQubit(s) for s in random_strings]
    for _ in range(n_gates):
        circuit = add_cirq_gate(circuit, qubits)
    return circuit


def random_mixed_qubits_cirq_circuit(
    n_line_qubits: int = 5,
    n_grid_qubits: int = 5,
    n_named_qubits: int = 5,
    n_gates: int = 100,
):
    circuit = cirq.Circuit()

    line_qubits = cirq.LineQubit.range(n_line_qubits)

    grid_side_length = int(np.ceil(np.sqrt(n_grid_qubits)))
    grid_qubits = cirq.GridQubit.rect(grid_side_length, grid_side_length)
    random_strings = [uuid.uuid4().hex for i in range(n_named_qubits)]
    named_qubits = [cirq.NamedQubit(s) for s in random_strings]

    qubits = line_qubits + grid_qubits + named_qubits
    for _ in range(n_gates):
        circuit = add_cirq_gate(circuit, qubits)
    return circuit


if __name__ == "__main__":
    circuit = random_mixed_qubits_cirq_circuit()
    print(circuit)
