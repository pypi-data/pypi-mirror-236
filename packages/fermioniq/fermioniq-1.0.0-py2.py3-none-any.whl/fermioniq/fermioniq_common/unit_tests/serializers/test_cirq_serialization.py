import numpy as np
import pytest

from common.serializers.cirq_serializer import (
    cirq_circuit_to_native_python,
    cirq_gate_map,
)
from unit_tests.serializers.cirq_testing_utils import (
    random_grid_qubits_cirq_circuit,
    random_line_qubits_cirq_circuit,
    random_mixed_qubits_cirq_circuit,
    random_named_qubits_cirq_circuit,
)
from unit_tests.serializers.utils import n_qubits_n_gates_generator

N_RANDOM_LINEQUBIT_TESTS = 20
N_RANDOM_GRIDQUBIT_TESTS = 20
N_RANDOM_NAMEDQUBIT_TESTS = 20
N_RANDOM_MIXED_QUBIT_TESTS = 20
N_RANDOM_FULL_MATRIX_TESTS = 10


def n_rows_n_cols_n_gates_generator(n_circuits):
    for _ in range(n_circuits):
        n_rows, n_cols = np.random.randint(2, 10, 2)
        n_gates = np.random.randint(1, 100)
        yield n_rows, n_cols, n_gates


def mixed_test_generator(n_circuits):
    for _ in range(n_circuits):
        n_line_qubits = np.random.randint(1, 7)
        n_grid_qubits = np.random.randint(1, 7)
        n_named_qubits = np.random.randint(1, 7)
        n_gates = np.random.randint(1, 100)
        yield n_line_qubits, n_grid_qubits, n_named_qubits, n_gates


@pytest.mark.parametrize(
    "n_qubits, n_gates", n_qubits_n_gates_generator(N_RANDOM_LINEQUBIT_TESTS)
)
def test_cirq_linequbit_serialization(n_qubits, n_gates):
    """
    Tests that a randomly generated cirq circuit on line qubits can be serialized.
    """
    circuit = random_line_qubits_cirq_circuit(n_qubits, n_gates)
    cirq_circuit_to_native_python(circuit)


@pytest.mark.parametrize(
    "n_rows, n_cols, n_gates", n_rows_n_cols_n_gates_generator(N_RANDOM_GRIDQUBIT_TESTS)
)
def test_cirq_gridqubit_serialization(n_rows, n_cols, n_gates):
    """
    Tests that a randomly generated cirq circuit on grid qubits can be serialized.
    """
    circuit = random_grid_qubits_cirq_circuit(n_rows, n_cols, n_gates)
    cirq_circuit_to_native_python(circuit)


@pytest.mark.parametrize(
    "n_qubits, n_gates", n_qubits_n_gates_generator(N_RANDOM_LINEQUBIT_TESTS)
)
def test_cirq_namedqubit_serialization(n_qubits, n_gates):
    """
    Tests that a randomly generated cirq circuit on named qubits can be serialized.
    """
    circuit = random_named_qubits_cirq_circuit(n_qubits, n_gates)
    cirq_circuit_to_native_python(circuit)


@pytest.mark.parametrize(
    "n_line_qubits, n_grid_qubits, n_named_qubits, n_gates",
    mixed_test_generator(N_RANDOM_MIXED_QUBIT_TESTS),
)
def test_cirq_mixed_qubits_serialization(
    n_line_qubits, n_grid_qubits, n_named_qubits, n_gates
):
    """
    Tests that a randomly generated cirq circuit, on a mix of qubit types, can be serialized.
    """
    circuit = random_mixed_qubits_cirq_circuit(
        n_line_qubits, n_grid_qubits, n_named_qubits, n_gates
    )
    cirq_circuit_to_native_python(circuit)


@pytest.mark.parametrize(
    "n_line_qubits, n_grid_qubits, n_named_qubits, n_gates",
    mixed_test_generator(N_RANDOM_FULL_MATRIX_TESTS),
)
def test_cirq_full_matrix_serialization(
    n_line_qubits, n_grid_qubits, n_named_qubits, n_gates
):
    """
    Test that serialization of cirq circuits doesn't miss a gate or add any extras, for each
    of the four circuit (qubit) types.
    """
    line_circuit = random_line_qubits_cirq_circuit(n_line_qubits, n_gates)
    n_rows_cols = int(np.sqrt(n_grid_qubits)) + 1
    grid_circuit = random_grid_qubits_cirq_circuit(n_rows_cols, n_rows_cols, n_gates)
    named_circuit = random_named_qubits_cirq_circuit(n_named_qubits, n_gates)
    mixed_circuit = random_mixed_qubits_cirq_circuit(
        n_line_qubits, n_grid_qubits, n_named_qubits, n_gates
    )
    circuits = [line_circuit, grid_circuit, named_circuit, mixed_circuit]

    for circuit in circuits:
        all_serialized_gate_names = [
            gate["name"]
            for gate in cirq_circuit_to_native_python(circuit, compress_rotations=False)
        ]
        all_gate_names = [
            cirq_gate_map[gate.gate.__class__.__name__]
            for moment in circuit
            for gate in moment
        ]

        assert set(all_serialized_gate_names) == set(all_gate_names)
        assert all(
            all_gate_names.count(gate) == all_serialized_gate_names.count(gate)
            for gate in all_serialized_gate_names
        )
