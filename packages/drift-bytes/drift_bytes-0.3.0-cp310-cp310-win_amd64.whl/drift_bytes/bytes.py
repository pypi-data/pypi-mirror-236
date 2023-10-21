# pylint: disable=missing-docstring, too-many-public-methods, useless-super-delegation
"""Bindings for the C++ implementation of the Bytes class."""
from typing import List, Union, Optional

import drift_bytes._drift_bytes as impl  # pylint: disable=import-error, no-name-in-module


class Variant:
    TYPES = impl.supported_types()  # pylint: disable=c-extension-no-member
    SUPPORTED_TYPES = Union[
        None,
        bool,
        int,
        float,
        str,
        List[bool],
        List[int],
        List[float],
        List[str],
    ]

    def __init__(
        self,
        value: SUPPORTED_TYPES = None,
        kind: Optional[str] = None,
    ):
        """Create Variant object from value

        Args:
            kind (str): Type of value can be: bool, uint8, int8,
            uint16, int16, uint32, int32, uint64, int64, float32, float64, string
            value (Union[bool, int, float, str, List[bool], List[int], List[float],
            List[str]]): Value to be stored in Variant object
        """

        if isinstance(value, impl.Variant):
            # for internal use only to pop from InputBuffer
            self._variant = value
            self._shape = value.shape()
            return

        type_error = TypeError(
            f"Unsupported type: {kind}. Must be one of: {self.TYPES}"
        )

        type = self._find_type(kind, type_error, value)

        if not isinstance(value, list):
            value = [value]

        self._shape = [len(value)]
        self._make_variant(type, self._shape, value)

    def _find_type(self, kind, type_error, value):  # pylint: disable=too-many-branches
        if kind is None:
            if value is None:
                kind = "none"
            elif isinstance(value, bool):
                kind = "bool"
            elif isinstance(value, int):
                kind = "int64"
            elif isinstance(value, float):
                kind = "float64"
            elif isinstance(value, str):
                kind = "string"
            elif isinstance(value, list):
                if len(value) == 0:
                    raise ValueError("Empty list cannot be converted to Variant")
                if isinstance(value[0], bool):
                    kind = "bool"
                elif isinstance(value[0], int):
                    kind = "int64"
                elif isinstance(value[0], float):
                    kind = "float64"
                elif isinstance(value[0], str):
                    kind = "string"
                else:
                    raise type_error
            elif isinstance(value, Variant):
                kind = value.type
            else:
                raise type_error
        if kind not in self.TYPES:
            raise type_error
        return kind

    def _make_variant(self, kind, shape, value):
        if kind == "none":
            self._variant = impl.Variant.from_none()
        if kind == "bool":
            self._variant = impl.Variant.from_bools(shape, value)
        elif kind == "uint8":
            self._variant = impl.Variant.from_int8s(shape, value)
        elif kind == "int8":
            self._variant = impl.Variant.from_int8s(shape, value)
        elif kind == "uint16":
            self._variant = impl.Variant.from_uint16s(shape, value)
        elif kind == "int16":
            self._variant = impl.Variant.from_int16s(shape, value)
        elif kind == "uint32":
            self._variant = impl.Variant.from_uint32s(shape, value)
        elif kind == "int32":
            self._variant = impl.Variant.from_int32s(shape, value)
        elif kind == "uint64":
            self._variant = impl.Variant.from_uint64s(shape, value)
        elif kind == "int64":
            self._variant = impl.Variant.from_int64s(shape, value)
        elif kind == "float32":
            self._variant = impl.Variant.from_float32s(shape, value)
        elif kind == "float64":
            self._variant = impl.Variant.from_float64s(shape, value)
        elif kind == "string":
            self._variant = impl.Variant.from_strings(shape, value)

    @property
    def type(self) -> str:
        """Get type"""
        return self._variant.type()

    @property
    def shape(self) -> List[int]:
        """Get shape"""
        return self._variant.shape()

    @property
    def value(self) -> SUPPORTED_TYPES:  # pylint: disable=too-many-branches
        """Get value"""
        if self.type == "none":
            return None

        if self.type == "bool":
            ary = self._variant.to_bools()
        elif self.type == "uint8":
            ary = self._variant.to_uint8s()
        elif self.type == "int8":
            ary = self._variant.to_int8s()
        elif self.type == "uint16":
            ary = self._variant.to_uint16s()
        elif self.type == "int16":
            ary = self._variant.to_int16s()
        elif self.type == "uint32":
            ary = self._variant.to_uint32s()
        elif self.type == "int32":
            ary = self._variant.to_int32s()
        elif self.type == "uint64":
            ary = self._variant.to_uint64s()
        elif self.type == "int64":
            ary = self._variant.to_int64s()
        elif self.type == "float32":
            ary = self._variant.to_float32s()
        elif self.type == "float64":
            ary = self._variant.to_float64s()
        elif self.type == "string":
            ary = self._variant.to_strings()
        else:
            raise TypeError(f"Unsupported type: {self.type}")

        if self.shape == [1]:
            return ary[0]

        return ary


class InputBuffer:
    """Input buffer for reading Variants from bytes"""

    def __init__(self, buffer: bytes):
        self._buffer = impl.InputBuffer.from_bytes(buffer)

    def pop(self) -> Variant:
        """Pop a Variant from the buffer"""
        return Variant(self._buffer.pop())

    def empty(self) -> bool:
        """Check if buffer is empty"""
        return self._buffer.empty()

    def size(self) -> int:
        """Get size of buffer"""
        return self._buffer.size()

    def __getitem__(self, item):
        """Get item from buffer"""
        return Variant(self._buffer.get(item))


class OutputBuffer:
    def __init__(self, size: int = 0):
        """Create an empty OutputBuffer"""
        self._buffer = impl.OutputBuffer(size)

    def push(self, value):
        """Push a Variant to the buffer"""
        if not isinstance(value, Variant):
            value = Variant(value)

        self._buffer.push(value._variant)  # pylint: disable=protected-access

    def empty(self) -> bool:
        """Check if buffer is empty"""
        return self._buffer.empty()

    def size(self) -> int:
        """Get size of buffer"""
        return self._buffer.size()

    def __setitem__(self, key, value):
        """Set item in buffer"""
        if not isinstance(value, Variant):
            value = Variant(value)
        self._buffer.set(key, value._variant)  # pylint: disable=protected-access

    def bytes(self):
        """Get bytes"""
        return self._buffer.bytes()
