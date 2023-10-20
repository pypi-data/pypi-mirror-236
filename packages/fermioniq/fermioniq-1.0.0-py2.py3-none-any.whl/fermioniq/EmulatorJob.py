import base64
import copy
import json
import sys
import zlib
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ValidationError
from rich.console import Group
from rich.panel import Panel

from fermioniq.fermioniq_common.common.config.config_utils import (
    print_error_warning_table,
)
from fermioniq.fermioniq_common.common.config.defaults import (
    standard_input_from_cirq_qiskit,
)
from fermioniq.fermioniq_common.common.config.emulator_input import EmulatorInput
from fermioniq.fermioniq_common.common.json.decode import CustomDecoder, dejsonify
from fermioniq.fermioniq_common.common.json.encode import jsonify
from fermioniq.fermioniq_common.common.noise_models import NoiseModel
from fermioniq.fermioniq_common.common.serializers.custom_types import Circuit
from fermioniq.fermioniq_common.common.serializers.serializer import serialize_config
from fermioniq.logging.printing import (
    MIDDLE_GRAY,
    OUTER_GRAY,
    rich_amplitudes,
    rich_expectations,
    rich_global_metadata,
    rich_metadata,
    rich_mps,
    rich_samples,
)


class NoiseModelWrapper(BaseModel):
    provider: Literal["user", "fermioniq"]
    content: str


class EmulatorJob:
    # remote job id. set when scheduled
    job_id: str | None = None
    noise_model: dict | None = None
    config: list[dict[str, Any]]
    circuit: list[
        str | list[dict]
    ]  # List of strings (compressed version) or list of circuits
    remote_config_name: str | None = None

    def __init__(
        self,
        circuit: Circuit | list[Circuit],
        config: dict[str, Any] | list[dict[str, Any]] | None | list[None] = None,
        noise_model: str | NoiseModel | None = None,
        remote_config_name: str | None = None,
    ):
        """
        EmulatorJob class to setup a job on the emulator.

        :param circuit: A cirq.circuits.circuit.Circuit or a quiskit QuantumCircuit, or a list of circuits.
        :param config: Emulator configuration, or a list of configurations (one for each circuit).
        :noise_model: (Optional) A string of a remote noise model or a dict containing a noise model.
        :remote_config_name: (Optional) Name of the remote execution engine to use.

        :returns:
        An instance of EmulatorJob, which can be submitted to the emulator for running.
        """
        # Initialize config and circuit lists
        self.config = []
        self.circuit = []
        self.remote_config_name = remote_config_name

        circuit_list = []
        # Convert a single circuit into a list with one item
        if not isinstance(circuit, list):
            circuit_list = [circuit]  # type: ignore
        else:
            circuit_list = circuit
            # If the user provided a list of circuits and a list of configs, make sure the number of each is the same
            if isinstance(config, list) and len(config) != len(circuit):
                raise ValueError(
                    f"Number of configs provided ({len(config)}) does not match the number of circuits ({len(circuit)})."
                )

        # If the user provided only one config, we turn it into a list of the same length as the number of circuits
        if config is not None:
            if not isinstance(config, list):
                config = [config] * len(circuit_list)
        # Otherwise make a bunch of empty configs
        else:
            config = [None] * len(circuit_list)

        # We serialize every circuit and validate every config
        all_inputs = []
        for circ, conf in zip(circuit_list, config):

            # Always make a standard config, and update it with the user-provided one (if possible)
            conf_dict, serialized_circuit = standard_input_from_cirq_qiskit(
                circ, effort=0.1, noise=(noise_model is not None)
            )
            default_qubit_objects = conf_dict["qubits"]

            # Update the config with the user-provided one
            if conf is not None:
                conf_dict = recursive_dict_update(conf_dict, conf)

            # If this update set 'qubits' to None, we put the default qubit order there
            if conf_dict["qubits"] is None:
                conf_dict["qubits"] = default_qubit_objects

            # Fully serialize the config
            conf_dict = serialize_config(conf_dict)

            try:
                emulator_input = EmulatorInput(  # TODO: Fix mypy issue
                    emulator_config=conf_dict,  # type: ignore
                    circuit=serialized_circuit,
                    noise_model=noise_model,  # type: ignore
                )
                all_inputs.append(emulator_input)
            except ValidationError as e:
                # TODO: If verbosity is high, print the errors during validation
                # if verbose:
                print_error_warning_table("Input errors", e.errors(), title_color="red")
                sys.exit(1)

        # If all configs are equal, we only need to send one of them
        all_configs_equal = all(
            dicts_equal(
                all_inputs[0].emulator_config.dict(), input.emulator_config.dict()
            )
            for input in all_inputs
        )

        if all_configs_equal:
            self.config = [all_inputs[0].emulator_config.dict()]

        for input in all_inputs:
            # Pull out the config dict, serialized circuit
            if not all_configs_equal:
                self.config.append(input.emulator_config.dict())
            self.circuit.append(input.circuit)

        # Load noise model (only one per batch is supported)
        if isinstance(noise_model, NoiseModel):
            self.noise_model = NoiseModelWrapper(
                provider="user",
                content=json.dumps(jsonify(noise_model)),
            ).dict()
        elif isinstance(noise_model, str):
            self.noise_model = NoiseModelWrapper(
                provider="fermioniq",
                content=noise_model,
            ).dict()

        # Final step: compress the circuit data, and tag is as compressed
        self.circuit = ["__compressed__", compress_json(self.circuit)]

        # Convert to JSON readable format
        self.circuit = jsonify(self.circuit)
        self.config = jsonify(self.config)


class JobResult(BaseModel):
    status_code: int = -1
    job_outputs: list[dict[str, Any]] = []
    job_metadata: dict[str, Any] = {"unique_configs": {}}

    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        super().__init__(*args, **kwargs)
        # Dejsonify the job_outputs and job_metadata
        self.job_outputs = dejsonify(self.job_outputs)
        self.job_metadata = dejsonify(self.job_metadata)

        # Populate the configs of the job_output dicts from the job_metadata unique_configs
        #  and then remove the unique_configs field from the job_metadata
        unique_configs = self.job_metadata["unique_configs"]
        for emulation_output in self.job_outputs:
            emulation_output["config"] = unique_configs[emulation_output["config"]]
        self.job_metadata.pop("unique_configs")

    def _extract_field(
        self, circuit_number: int, run_number: int, field: str
    ) -> Any | None:
        """
        Extract a field from a list of results.
        """
        for output in self.job_outputs:
            if (
                output["circuit_number"] == circuit_number
                and output["run_number"] == run_number
            ):
                if field in output["output"]:
                    return output["output"][field]
                elif field in output:
                    return output[field]

        return None

    def amplitudes(self, circuit_number: int, run_number: int):
        return self._extract_field(
            circuit_number=circuit_number, run_number=run_number, field="amplitudes"
        )

    def samples(self, circuit_number: int, run_number: int):
        return self._extract_field(
            circuit_number=circuit_number, run_number=run_number, field="samples"
        )

    def run_metadata(self, circuit_number: int, run_number: int):
        return self._extract_field(
            circuit_number=circuit_number, run_number=run_number, field="metadata"
        )

    def config(self, circuit_number: int, run_number: int):
        return self._extract_field(
            circuit_number=circuit_number, run_number=run_number, field="config"
        )

    def expectation_values(self, circuit_number: int, run_number: int):
        return self._extract_field(
            circuit_number=circuit_number,
            run_number=run_number,
            field="expectation_values",
        )

    def __str__(self) -> str:
        return str({"job_outputs": self.job_outputs, "job_metadata": self.job_metadata})

    def __rich__(self):
        # Assumptions on the output format: a list of dicts, each with a circuit number, run number, output
        #  dict, metadata dict and config specific to the run.
        all_data = (
            (
                r["circuit_number"],
                r["run_number"],
                r["output"],
                r["metadata"],
                r["config"],
            )
            for r in self.job_outputs
        )
        all_data_sorted = sorted(all_data, key=lambda x: (x[0], x[1]))

        all_rich_groups = []
        curr_circuit_number = -1
        circuit_groups = (
            []
        )  # List of result and metadata panels per run, for the current circuit.
        for (
            next_circuit_number,
            run_number,
            output,
            metadata,
            config,
        ) in all_data_sorted:
            amplitudes = output.get("amplitudes", None)
            samples = output.get("samples", None)
            expectation_values = output.get("expectation_values", None)
            mps = output.get("mps", None)

            # Put all circuits into a single panel
            if curr_circuit_number != next_circuit_number:
                # Make a panel for all runs of the previous circuit
                if len(circuit_groups) > 0:
                    circuit_title = f"[bold]Circuit {curr_circuit_number}[/bold]"
                    circuit_panel = Panel(
                        Group(*circuit_groups),
                        title=circuit_title,
                        border_style=OUTER_GRAY,
                        title_align="left",
                    )
                    all_rich_groups.append(circuit_panel)
                curr_circuit_number = next_circuit_number
                circuit_groups = []

            run_title = f"[bold]Run {run_number}[/bold]"

            # Amplitudes panel
            # Decide whether this was a noisy emulation or not by inspecting the config (if possible)
            noise = False
            if config:
                noise = config["noise"].get("enabled", False)

            amplitude_panel = (
                rich_amplitudes(amplitudes, noise=noise) if amplitudes else None
            )

            # Samples panel
            sample_panel = rich_samples(samples) if samples else None

            exp_val_panel = (
                rich_expectations(expectation_values) if expectation_values else None
            )

            mps_panel = rich_mps(mps) if mps else None

            # Metadata panel
            metadata_panel = rich_metadata(metadata, config)

            result_panels = [
                p
                for p in [amplitude_panel, sample_panel, exp_val_panel, mps_panel]
                if p is not None
            ]
            if not result_panels:
                group = Group(
                    "[red][bold]Unexpected results. Printing raw output instead:[/bold]",
                    str(output),
                    metadata_panel,
                )
                circuit_groups.append(
                    Panel(
                        Group(group, metadata_panel),
                        title=run_title,
                        border_style=MIDDLE_GRAY,
                        title_align="left",
                    )
                )
            else:
                # Add the group (for the run) to the list of groups for this circuit
                circuit_groups.append(
                    Panel(
                        Group(*result_panels, metadata_panel),
                        title=run_title,
                        border_style=MIDDLE_GRAY,
                        title_align="left",
                    )
                )

        # Add the final circuit panel
        if len(circuit_groups) > 0:
            circuit_title = f"[bold]Circuit {curr_circuit_number}[/bold]"
            circuit_panel = Panel(
                Group(*circuit_groups),
                title=circuit_title,
                border_style=OUTER_GRAY,
                title_align="left",
            )
            all_rich_groups.append(circuit_panel)

        # Make a panel for the metadata for all runs
        global_metadata = self.job_metadata
        global_panel = rich_global_metadata(global_metadata)

        return Group(*all_rich_groups, global_panel)


def recursive_dict_update(d: dict, u: dict) -> dict:
    """Recursively update a dictionary with another dictionary."""
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = recursive_dict_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def dicts_equal(d1: dict, d2: dict) -> bool:
    """
    Test if two dictionaries are equal, provided that they only contain primitive types
    and other dictionaries (i.e. are serializable).
    """
    equal = True
    for k in d1:
        if k in d2:
            if isinstance(d1[k], dict) and isinstance(d2[k], dict):
                equal = equal and dicts_equal(d1[k], d2[k])
            elif d1[k] != d2[k]:
                equal = False
        else:
            return False
    return equal


def compress_json(json_data: list | dict) -> str:
    """Compresses serializable objects (a (nested) list or dict) into a string

    :param json_data: The data to compress.

    :returns: The compressed data as a string.
    """
    return base64.b64encode(
        zlib.compress(json.dumps(json_data).encode("utf-8"))
    ).decode("utf-8")


def test_printing(out_fname: str, stats_fname: str):
    with open(out_fname, "r") as f:
        out = json.load(f)
    with open(stats_fname, "r") as f:
        stats = yaml.safe_load(f)
    res = JobResult(job_outputs=out, job_metadata=stats)

    import rich

    rich.print(res)
