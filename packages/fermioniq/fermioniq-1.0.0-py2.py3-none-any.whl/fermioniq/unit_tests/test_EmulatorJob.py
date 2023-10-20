from typing import Any

from fermioniq import EmulatorJob
from fermioniq.unit_tests.utils import qiskit_bell_pair


def assert_default_config(config: dict[str, Any]):
    """
    This functions checks whether the config has the correct default arguments.
    """
    # default mode and no noise
    assert config["mode"] == "dmrg"

    # default dmrg settings
    assert config["dmrg"]["D"] == 2
    assert config["dmrg"]["convergence_window_size"] == 2 * 2
    assert config["dmrg"]["max_subcircuit_rows"] == 1
    assert config["dmrg"]["mpo_bond_dim"] == 4
    assert config["dmrg"]["regular_grid"] == True

    assert config["qubits"] == ["0", "1"]
    assert config["grouping"] == [["0"], ["1"]]

    # Only sampling is enabled
    assert not config["output"]["amplitudes"]["enabled"]
    assert config["output"]["amplitudes"]["bitstrings"] == "all"

    assert config["output"]["sampling"]["enabled"]
    assert config["output"]["sampling"]["n_shots"] == 1000

    assert not config["output"]["mps"]["enabled"]


def test_default_construction():
    """
    Test whether EmulatorJob correctly constructs a default config when no config
    is provided and the input is one single circuit.
    """
    circuit = qiskit_bell_pair()
    job = EmulatorJob(circuit=circuit)  # type: ignore

    assert job.noise_model == None, "Noise Model should have been None"
    assert type(job.config) == list, "Configs should be list"
    assert len(job.config) == 1, "Only 1 config should be returned"

    config = job.config[0]

    assert_default_config(config=config)


def test_default_construction_list():
    """
    Test whether EmulatorJob correctly constructs a default config when no config
    is provided and the input is a list of circuits.
    """
    circuit1 = qiskit_bell_pair()
    circuit2 = qiskit_bell_pair()
    job = EmulatorJob(circuit=[circuit1, circuit2])  # type: ignore

    assert job.noise_model == None, "Noise Model should have been None"
    assert type(job.config) == list, "Configs should be list"
    assert len(job.config) == 1, "Only 1 config should be returned"

    config = job.config[0]

    assert_default_config(config=config)
