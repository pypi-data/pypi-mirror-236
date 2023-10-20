from typing import Any as AnyType
from typing import TypeGuard, Union

from pydantic import PrivateAttr

from ..config.config_utils import BaseConfigWithWarning
from ..serializers.cirq_serializer import cirq_gate_map, cirq_qubit_to_str
from ..serializers.custom_types import is_cirq_qubit, is_qiskit_qubit
from ..serializers.qiskit_serializer import qiskit_gate_map, qiskit_qubit_to_str


# This is only used for correctly decoding jsonified objects from the noise models
class BaseNoiseComponent(BaseConfigWithWarning):
    class Config:
        arbitrary_types_allowed = True


# Class used to indicate a match to "any" qubits or "any" gate
class Any(BaseNoiseComponent):
    def __str__(self) -> str:
        return "__any"

    def __repr__(self):
        return "__any"

    def __eq__(self, other) -> bool:
        return isinstance(other, Any)

    def __hash__(self) -> int:
        return hash(str(self))

    ...


# Instance of the class to use for matching "any" qubits
ANY = Any()


class QubitInternal(BaseNoiseComponent):
    object: AnyType
    _string: str = PrivateAttr(default="")

    def __init__(self, **data):
        """
        Sets the object attribute, which should have been provided as
        Cirq qubit, Qiskit qubit or string.

        Converts the object to a string, and stores it in the _string
        attribute.

        :param object: Cirq qubit, Qiskit qubit or string.

        """

        super().__init__(**data)
        object = self.object
        if isinstance(object, str):
            qubit_str = object
        elif is_qiskit_qubit(object):
            qubit_str = qiskit_qubit_to_str(object)
        elif is_cirq_qubit(object):
            qubit_str = cirq_qubit_to_str(object)
        else:
            raise ValueError(
                "Qubit is not a string, Qiskit qubit or Cirq qubit as required"
            )
        self._string = qubit_str

    def __hash__(self):
        return hash(self._string)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return self._string

    def to_dict(self):
        fields = {"object": getattr(self, "_string")}
        return {
            "type": self.__class__.__name__,
            "fields": fields,
        }

    # Ignores the private attribute _string, and builds the qubit from the provided fields,
    # which should only contain 'object'.
    @classmethod
    def from_dict(cls, d):
        # Create an instance of the class with the fields specified in the dictionary
        obj = cls(**d["fields"])
        return obj


# All currently supported gates, and the number of qubits that they act on
supported_gate_sizes = {
    "I": -1,
    "Gate": -1,
    "X": 1,
    "RX": 1,
    "S": 1,
    "SDG": 1,
    "T": 1,
    "TDG": 1,
    "Y": 1,
    "RY": 1,
    "Z": 1,
    "RZ": 1,
    "H": 1,
    "RH": 1,
    "P": 1,
    "PhasedXPOW": 1,
    "PhasedXZ": 1,
    "U3": 1,
    "CX": 2,
    "CXPOW": 2,
    "CRX": 2,
    "CZ": 2,
    "CZPOW": 2,
    "CRZ": 2,
    "CY": 2,
    "CRY": 2,
    "RXX": 2,
    "RYY": 2,
    "RZZ": 2,
    "SWAP": 2,
    "SWAPPOW": 2,
    "ISWAP": 2,
    "ISWAPPOW": 2,
    "FSIM": 2,
    "PhasedFSIM": 2,
    "CU": 2,
    "CH": 2,
    "CCX": 3,
    "CCXPOW": 3,
    "RCCX": 3,
    "CSWAP": 3,
    "RCCCX": 4,
}


def tuples_to_lists(input):
    """Given a nested structure of tuples and lists, convert every tuple to a list."""
    if isinstance(input, tuple):
        return list(map(tuples_to_lists, input))
    elif isinstance(input, list):
        return [tuples_to_lists(item) for item in input]
    else:
        return input
