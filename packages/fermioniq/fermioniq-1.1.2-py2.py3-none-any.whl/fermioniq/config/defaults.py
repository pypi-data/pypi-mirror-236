from typing import Any

from fermioniq.fermioniq_common.common.config.defaults import (
    standard_input_from_cirq_qiskit,
)
from fermioniq.fermioniq_common.common.noise_models import NoiseModel
from fermioniq.fermioniq_common.common.noise_models.channel import DepolarizingChannel
from fermioniq.fermioniq_common.common.serializers.custom_types import Circuit
from fermioniq.fermioniq_common.common.serializers.serializer import serialize_circuit


def standard_config_noisy(circuit: Circuit, effort: float = 0.1) -> dict[str, Any]:
    """Given a circuit return a default config setup that should perform well on a noisy emulation of this circuit.
    The effort parameter is used to control how much computational effort will be put into emulating
    this circuit. More effort will usually mean higher fidelity, although it depends on the difficulty
    of the circuit.

    :param circuit: The circuit (from Cirq / Qiskit).
    :param effort: A float between 0 and 1 that specifies the 'effort' that should be put into emulation.
        A number closer to 1 will aim to maximize fidelity of the emulation (up to memory limitations).

    :returns: Updated emulator input with standard settings.
    """
    return standard_config(circuit, effort, True)


def standard_config(
    circuit: Circuit,
    effort: float = 0.1,
    noise: bool = False,
) -> dict[str, Any]:
    """Given a circuit in qiskit or cirq, return a default config setup that should perform well on this circuit.
    The effort parameter is used to control how much computational effort will be put into emulating
    this circuit. More effort will usually mean higher fidelity, although it depends on the difficulty
    of the circuit.

    :param circuit: The circuit.
    :param effort: A float between 0 and 1 that specifies the 'effort' that should be put into emulation.
        A number closer to 1 will aim to maximize fidelity of the emulation (up to memory limitations).
    :param noise: Indicate whether this is a noisy simulation or not

    :returns: Emulator config with standard settings.
    """
    config, _ = standard_input_from_cirq_qiskit(circuit, effort, noise)
    return config


def depolarizing_noise_model(
    circuit: Circuit,
    one_qubit_fidelity: float,
    two_qubit_fidelity: float,
    readout_fidelity: float | None = None,
) -> NoiseModel:
    """
    Given a circuit, generates a noise model for it, where noise is assumed to be depolarizing. Readout error can also optionally be added.

    :param circuit: Circuit.
    :param one_qubit_fidelity: Fidelity to use for single-qubit gates.
    :param two_qubit_fidelity: Fidelity to use for two-qubit gates.
    :param readout_fidelity: (Optional) Fidelity to use for readout error.
        Default is None, which correponds to no readout error.

    :return: Noise model
    """
    if not (0.5 <= one_qubit_fidelity <= 1.0):
        raise ValueError(
            f"Single-qubit gate fidelity should be between 0.5 and 1.0. Got {one_qubit_fidelity}."
        )
    if not (0.25 <= two_qubit_fidelity <= 1.0):
        raise ValueError(
            f"Two-qubit gate fidelity should be between 0.25 and 1.0. Got {two_qubit_fidelity}."
        )

    # First serialize the circuit
    serialized_circuit = serialize_circuit(circuit)

    # Pull out all the qubits
    all_qubits = set()
    for gate in serialized_circuit:
        all_qubits.update(gate["qubits"])

    # Make the noise model
    noise_model = NoiseModel(
        qubits=list(all_qubits),
        name="depolarizing",
        description="Depolarizing one- and two-qubit noise model",
    )

    # Make one- and two-qubit depolarizing noise channels
    d_1 = DepolarizingChannel(p=(1 - one_qubit_fidelity) / 0.5, num_qubits=1)
    d_2 = DepolarizingChannel(p=(1 - two_qubit_fidelity) / 0.75, num_qubits=2)

    # Add them to the noise model
    noise_model.add("any", 1, d_1, "same")  # One-qubit gates + noise
    noise_model.add("any", 2, d_2, "same")  # Two-qubit gates + noise

    # Readout noise
    if readout_fidelity is not None:
        noise_model.add_readout_error(
            "any", (1 - readout_fidelity), (1 - readout_fidelity)
        )

    return noise_model
