"""Contains data schema structure decoder."""
from __future__ import annotations

from typing import Final

from pyplumio.helpers.data_types import DATA_TYPES, DataType, unpack_ushort
from pyplumio.helpers.typing import EventDataType
from pyplumio.structures import StructureDecoder
from pyplumio.utils import ensure_dict

ATTR_SCHEMA: Final = "schema"

BLOCK_SIZE: Final = 3


class DataSchemaStructure(StructureDecoder):
    """Represents a data schema structure."""

    _offset: int

    def _unpack_block(self, message: bytearray) -> tuple[int, DataType]:
        """Unpack a block."""
        param_type = message[self._offset]
        param_id = unpack_ushort(message[self._offset + 1 : self._offset + BLOCK_SIZE])[
            0
        ]

        try:
            return param_id, DATA_TYPES[param_type]()
        finally:
            self._offset += BLOCK_SIZE

    def decode(
        self, message: bytearray, offset: int = 0, data: EventDataType | None = None
    ) -> tuple[EventDataType, int]:
        """Decode bytes and return message data and offset."""
        blocks = unpack_ushort(message[offset : offset + 2])[0]
        self._offset = offset + 2
        if blocks == 0:
            return ensure_dict(data), self._offset

        return (
            ensure_dict(
                data,
                {ATTR_SCHEMA: [self._unpack_block(message) for _ in range(blocks)]},
            ),
            self._offset,
        )
