"""Contains an outputs structure decoder."""
from __future__ import annotations

import math
from typing import Final

from pyplumio.helpers.data_types import unpack_uint
from pyplumio.helpers.typing import EventDataType
from pyplumio.structures import StructureDecoder
from pyplumio.utils import ensure_dict

ATTR_FAN: Final = "fan"
ATTR_FEEDER: Final = "feeder"
ATTR_HEATING_PUMP: Final = "heating_pump"
ATTR_WATER_HEATER_PUMP: Final = "water_heater_pump"
ATTR_CIRCULATION_PUMP: Final = "circulation_pump"
ATTR_LIGHTER: Final = "lighter"
ATTR_ALARM: Final = "alarm"
ATTR_OUTER_BOILER: Final = "outer_boiler"
ATTR_FAN2_EXHAUST: Final = "fan2_exhaust"
ATTR_FEEDER2: Final = "feeder2"
ATTR_OUTER_FEEDER: Final = "outer_feeder"
ATTR_SOLAR_PUMP: Final = "solar_pump"
ATTR_FIREPLACE_PUMP: Final = "fireplace_pump"
ATTR_GCZ_CONTACT: Final = "gcz_contact"
ATTR_BLOW_FAN1: Final = "blow_fan1"
ATTR_BLOW_FAN2: Final = "blow_fan2"

OUTPUTS: tuple[str, ...] = (
    ATTR_FAN,
    ATTR_FEEDER,
    ATTR_HEATING_PUMP,
    ATTR_WATER_HEATER_PUMP,
    ATTR_CIRCULATION_PUMP,
    ATTR_LIGHTER,
    ATTR_ALARM,
    ATTR_OUTER_BOILER,
    ATTR_FAN2_EXHAUST,
    ATTR_FEEDER2,
    ATTR_OUTER_FEEDER,
    ATTR_SOLAR_PUMP,
    ATTR_FIREPLACE_PUMP,
    ATTR_GCZ_CONTACT,
    ATTR_BLOW_FAN1,
    ATTR_BLOW_FAN2,
)

OUTPUTS_SIZE: Final = 4


class OutputsStructure(StructureDecoder):
    """Represents an outputs data structure."""

    def decode(
        self, message: bytearray, offset: int = 0, data: EventDataType | None = None
    ) -> tuple[EventDataType, int]:
        """Decode bytes and return message data and offset."""
        outputs = unpack_uint(message[offset : offset + OUTPUTS_SIZE])[0]
        return (
            ensure_dict(
                data,
                {
                    output: bool(outputs & int(math.pow(2, index)))
                    for index, output in enumerate(OUTPUTS)
                },
            ),
            offset + OUTPUTS_SIZE,
        )
