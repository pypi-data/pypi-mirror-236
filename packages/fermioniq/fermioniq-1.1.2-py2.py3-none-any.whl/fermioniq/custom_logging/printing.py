import json
from typing import Any, Optional

import numpy as np
import rich
from rich import box, print
from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, TaskID
from rich.table import Table
from rich.text import Text

from fermioniq.fermioniq_common.common.config.config_utils import (
    print_error_warning_table,
)
from fermioniq.fermioniq_common.common.json.decode import CustomDecoder
from fermioniq.fermioniq_common.common.messaging.message import (
    ConfigMessage,
    ErrorMessage,
    ProgressMessage,
    StringMessage,
)

# Store colors for rich printing
OUTER_GRAY = "gray89"
MIDDLE_GRAY = "gray70"
INNER_GRAY = "gray50"


class Printer:
    progress_bar: Optional[Progress]
    task: Optional[TaskID]

    def __init__(self) -> None:
        self.progress_bar = None
        self.task = None

    def _update_progress(self, abs_value: float):
        if self.progress_bar is None:
            self.progress_bar = Progress()
            self.task = self.progress_bar.add_task("[red]Emulating...", total=1.0)
            self.progress_bar.start()

        if self.progress_bar is not None and self.task is not None:
            self.progress_bar.update(self.task, completed=abs_value)
            self.progress_bar.refresh()

    def _finish(self):
        if self.progress_bar is not None and self.task is not None:
            self.progress_bar.update(self.task, completed=1.0)
            self.progress_bar.refresh()
        self.progress_bar.stop()

    def pprint(self, s: str):
        if len(s.strip("\n")) == 0:
            return None
        try:
            obj = json.loads(s, cls=CustomDecoder)

            if isinstance(
                obj, ConfigMessage
            ):  # Config messages are printed in the usual way
                errors = obj.errors
                warnings = obj.warnings
                if errors:
                    print_error_warning_table("Errors", errors)
                if warnings:
                    print_error_warning_table("Warnings", warnings)

            elif isinstance(obj, StringMessage):
                msg = obj.message
                rich.print(f"[bold]Message:[/bold] {msg}")

            elif isinstance(obj, ErrorMessage):
                msg = obj.message
                error_type = obj.error_type
                if error_type is not None:
                    rich.print(f"[red]Error ({error_type}): {msg}")
                else:
                    rich.print(f"[red]Error: {msg}")

            elif isinstance(obj, ProgressMessage):
                abs_value = obj.abs_progress
                label = obj.label  # TODO: Multiple progress bars via label lookup
                self._update_progress(abs_value)
                if obj.finished:
                    self._finish()

        except json.decoder.JSONDecodeError:  # TODO: Remove this
            # TODO: This is temporary (and hacky :)
            if "status_code" in s:
                rest = (
                    "{"
                    + s.strip("status_code=0 ").replace("=", ":").replace("'", '"')
                    + "}"
                )
                print(rest)
            else:
                print(f"Error parsing message from emulator. Message is: '{s}'")


def rich_amplitudes(amplitudes: dict, noise: bool = False) -> Panel:
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column(
        "[deep_sky_blue1]Basis state",
        justify="right",
        style="deep_sky_blue1",
        no_wrap=True,
    )
    amp_string = "Probability" if noise else "Amplitude"
    table.add_column("[magenta]Probability", style="magenta", width=20)
    table.add_column("", style="magenta")
    table.add_column(f"[cyan]{amp_string}", style="cyan")

    for basis_state, amplitude in amplitudes.items():
        if noise:
            abs_v = amplitude
        else:
            abs_v = np.real(amplitude**2)
        bar_length = int(np.round(abs_v * 20))
        table.add_row(
            basis_state,
            "▇" * bar_length,
            str(np.round(abs_v, 5)),
            str(np.round(amplitude, 5)),
        )
    title_str = "Probabilities" if noise else "Amplitudes"
    return Panel(
        table,
        expand=False,
        title=f"[green][b]Output - {title_str}",
        border_style=INNER_GRAY,
    )


def rich_samples(samples: dict[str, int]) -> Panel:
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column(
        "[deep_sky_blue1]Basis state",
        justify="right",
        style="deep_sky_blue1",
        no_wrap=True,
    )
    table.add_column("[magenta]Frequency", style="magenta", width=20)
    table.add_column(f"[cyan]Inferred probability", style="cyan")

    total_count = sum(c for c in samples.values())
    for basis_state, count in samples.items():
        table.add_row(
            basis_state,
            str(count),
            str(np.round(count / total_count, 2)),
        )
    return Panel(
        table,
        expand=False,
        title=f"[green][b]Output - {total_count} samples",
        border_style=INNER_GRAY,
    )


def rich_expectations(expectation_values: list[dict[str, str]]) -> Panel:
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column(
        "[deep_sky_blue1]Observable",
        justify="right",
        style="deep_sky_blue1",
        no_wrap=True,
    )
    table.add_column("[magenta]Expectation Value", style="magenta", width=20)
    for exp_val in expectation_values:
        value_to_print = exp_val["expval"]
        if isinstance(value_to_print, complex):
            str_val = (
                f"{round(value_to_print.real, 5)} + {round(value_to_print.imag, 5)}j"
            )
        elif isinstance(value_to_print, float):
            str_val = str(round(value_to_print, 5))
        else:
            str_val = str(value_to_print)

        table.add_row(str(exp_val["name"]), str_val)
    return Panel(
        table,
        expand=False,
        title="[green][b]Output - Expectation Values",
        border_style=INNER_GRAY,
    )


def rich_mps(mps: list) -> Panel:
    # Make a string version of the mps
    tensors = [np.asarray(t) for _, t in mps]
    group_sizes = [len(t.shape) - 2 for t in tensors]
    top = "●" * group_sizes[0]
    mid = "|" * group_sizes[0]
    bot = "".join([str(d) for d in tensors[0].shape[1:-1]])
    for t, group_size in zip(tensors[1:], group_sizes[1:]):
        top_addition = f" - {t.shape[0]} - " + "●" * group_size
        top += top_addition
        mid += " " * (len(top_addition) - group_size) + "|" * group_size
        bot += " " * (len(top_addition) - group_size) + "".join(
            [str(d) for d in t.shape[1:-1]]
        )
    mps_str = Text(top + "\n" + mid + "\n" + bot, no_wrap=True, overflow="ellipsis")

    # Add extra information
    mps_len_str = f"Length: {len(mps)}"
    max_bd_str = (
        f"Max bond dimension: {max([max(t.shape[0], t.shape[-1]) for t in tensors])}\n"
    )

    group = Group(mps_len_str, max_bd_str, mps_str)
    return Panel(
        group,
        expand=False,
        title="[green][b]Output - MPS",
        border_style=INNER_GRAY,
        highlight=True,
    )


def rich_metadata(metadata: dict, config: dict) -> Panel:
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[deep_sky_blue1]Field", style="cyan")
    table.add_column("[cyan]Value", style="white")

    # Relevant bond dimension
    mode = config.get("mode")
    if mode == "dmrg":
        bond_dim = config["dmrg"]["D"]
    else:
        bond_dim = config["tebd"]["max_D"]
    if mode:
        table.add_row("Mode", str(mode))
        table.add_row("Bond dimension", str(bond_dim))

    # Runtime
    runtime = metadata.get("runtime", None)
    if runtime:
        table.add_row("Runtime", str(runtime))

    # Circuit depth
    circuit_depth = metadata.get("circuit_depth", None)
    if circuit_depth:
        table.add_row("Circuit depth", str(circuit_depth))

    # Number of 2-qubit gates
    number_2qubit_gates = metadata.get("number_2qubit_gates", None)
    if number_2qubit_gates:
        table.add_row("Number of 2-qubit gates", str(number_2qubit_gates))

    # Fidelity
    fidelity = metadata.get("fidelity_product", None)
    if fidelity:
        table.add_row("Estimated fidelity", str(fidelity))

    # Gate fidelity
    gate_fidelity = metadata.get("extrapolated_2qubit_gate_fidelity", None)
    if gate_fidelity:
        table.add_row("Estimated 2-qubit gate fidelity", str(gate_fidelity))

    if len(metadata) > 3:
        table.add_row(
            "[yellow]To view more information, inspect the result.metadata manually."
        )
    return Panel(table, expand=False, title=f"[yellow][b]Info", border_style=INNER_GRAY)


def rich_global_metadata(metadata: dict) -> Panel:
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[deep_sky_blue1]Field", style="cyan")
    table.add_column("[cyan]Value", style="white")

    # Runtime
    runtime = metadata.get("total_runtime", None)
    if runtime is not None:
        table.add_row("Total runtime (all emulations)", str(runtime))

    # Number of runs
    total_runs = metadata.get("total_runs", None)
    if total_runs is not None:
        table.add_row("Total number of emulations", str(total_runs))

    # GPU usage
    gpu_used = metadata.get("gpu_used", None)
    if gpu_used is not None:
        table.add_row("GPU-accelerated", str(gpu_used))

    return Panel(
        table, expand=False, title=f"[yellow][b]Metadata", border_style=OUTER_GRAY
    )
