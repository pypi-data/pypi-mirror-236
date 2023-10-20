import numpy as np
import pytest

from common.serializers.qiskit_serializer import (
    qiskit_circuit_to_native_python,
    qiskit_gate_map,
)
from unit_tests.serializers.qiskit_testing_utils import random_qiskit_circuit
from unit_tests.serializers.utils import n_qubits_n_gates_generator

N_RANDOM_CIRCUIT_TESTS = 20
N_RANDOM_FULL_MATRIX_TESTS = 10


@pytest.mark.parametrize(
    "n_qubits, n_gates", n_qubits_n_gates_generator(N_RANDOM_CIRCUIT_TESTS)
)
def test_qiskit_serialization(n_qubits, n_gates):
    """Test that qiskit circuits can be serialized without error"""
    circuit = random_qiskit_circuit(n_qubits, n_gates)
    qiskit_circuit_to_native_python(circuit)


@pytest.mark.parametrize(
    "n_qubits, n_gates", n_qubits_n_gates_generator(N_RANDOM_CIRCUIT_TESTS)
)
def test_qiskit_full_matrix_serialization(n_qubits, n_gates):
    """Test that serialization of qiskit circuits doesn't miss a gate or add any extras"""
    circuit = random_qiskit_circuit(n_qubits, n_gates)
    all_serialized_gate_names = [
        gate["name"] for gate in qiskit_circuit_to_native_python(circuit)
    ]
    all_gate_names = [qiskit_gate_map[gate.operation.name] for gate in circuit.data]

    assert set(all_serialized_gate_names) == set(all_gate_names)
    assert all(
        all_gate_names.count(gate) == all_serialized_gate_names.count(gate)
        for gate in all_serialized_gate_names
    )
