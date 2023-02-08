from typing import Any

from domain.PowerPlant import PowerPlant, WindPowerPlant

type_fuel_type_map = {
    "gasfired": "gas(euro/MWh)",
    "turbojet": "kerosine(euro/MWh)",
    "windturbine": "wind(%)",
}


class PowerPlantFactory:
    __type_factory = {"windturbine": WindPowerPlant}

    def from_dict(self, data: dict[str, Any], prices: dict[str, float]) -> PowerPlant:
        return self.__type_factory.get(data["type"], PowerPlant)(
            data["name"],
            data["type"],
            prices[type_fuel_type_map[data["type"]]],
            data["efficiency"],
            data["pmin"],
            data["pmax"],
        )
