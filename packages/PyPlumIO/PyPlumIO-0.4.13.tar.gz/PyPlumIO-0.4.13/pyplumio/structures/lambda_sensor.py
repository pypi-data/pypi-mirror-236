"""Contains a lambda sensor structure decoder."""
from __future__ import annotations

import math
from typing import Final

from pyplumio.const import BYTE_UNDEFINED
from pyplumio.helpers.data_types import unpack_ushort
from pyplumio.helpers.typing import EventDataType
from pyplumio.structures import StructureDecoder
from pyplumio.utils import ensure_dict

ATTR_LAMBDA_STATE: Final = "lambda_state"
ATTR_LAMBDA_TARGET: Final = "lambda_target"
ATTR_LAMBDA_LEVEL: Final = "lambda_level"

LAMBDA_LEVEL_SIZE: Final = 4


class LambaSensorStructure(StructureDecoder):
    """Represents a lambda sensor data structure."""

    def decode(
        self, message: bytearray, offset: int = 0, data: EventDataType | None = None
    ) -> tuple[EventDataType, int]:
        """Decode bytes and return message data and offset."""
        if message[offset] == BYTE_UNDEFINED:
            return ensure_dict(data), offset + 1

        level = unpack_ushort(message[offset + 2 : offset + LAMBDA_LEVEL_SIZE])[0]
        return (
            ensure_dict(
                data,
                {
                    ATTR_LAMBDA_STATE: message[offset],
                    ATTR_LAMBDA_TARGET: message[offset + 1],
                    ATTR_LAMBDA_LEVEL: None if math.isnan(level) else (level / 10),
                },
            ),
            offset + LAMBDA_LEVEL_SIZE,
        )
