"""Contains a mixer class."""
from __future__ import annotations

import asyncio
from typing import Sequence

from pyplumio.devices import Addressable, SubDevice
from pyplumio.helpers.typing import EventDataType, ParameterTupleType
from pyplumio.structures.mixer_parameters import ATTR_MIXER_PARAMETERS, MIXER_PARAMETERS
from pyplumio.structures.mixer_sensors import ATTR_MIXER_SENSORS
from pyplumio.structures.product_info import ATTR_PRODUCT, ProductInfo


class Mixer(SubDevice):
    """Represents an mixer."""

    def __init__(self, queue: asyncio.Queue, parent: Addressable, index: int = 0):
        """Initialize a new mixer."""
        super().__init__(queue, parent, index)
        self.subscribe(ATTR_MIXER_SENSORS, self._handle_sensors)
        self.subscribe(ATTR_MIXER_PARAMETERS, self._handle_parameters)

    async def _handle_sensors(self, sensors: EventDataType) -> bool:
        """Handle mixer sensors.

        For each sensor dispatch an event with the
        sensor's name and value.
        """
        for name, value in sensors.items():
            await self.dispatch(name, value)

        return True

    async def _handle_parameters(
        self, parameters: Sequence[tuple[int, ParameterTupleType]]
    ) -> bool:
        """Handle mixer parameters.

        For each parameter dispatch an event with the
        parameter's name and value.
        """
        product: ProductInfo = await self.parent.get(ATTR_PRODUCT)
        for index, value in parameters:
            description = MIXER_PARAMETERS[product.type][index]
            await self.dispatch(
                description.name,
                description.cls(
                    device=self,
                    description=description,
                    index=index,
                    value=value[0],
                    min_value=value[1],
                    max_value=value[2],
                ),
            )

        return True
