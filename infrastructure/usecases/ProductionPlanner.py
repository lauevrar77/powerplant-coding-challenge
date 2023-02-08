from dataclasses import dataclass

from domain.PowerPlant import PowerPlant


class UnsatifiableError(Exception):
    ...


@dataclass
class PlantUsage:
    plant: PowerPlant
    usage: int


class ProductionPlanner:
    def plan(self, load: int, plants: list[PowerPlant]) -> list[PlantUsage]:
        filled_load, used_plants = self.__fill_needs(
            load, plants
        )  # First fill the need

        if filled_load < load:
            raise UnsatifiableError("Cannot produce so much power")
        elif filled_load > load:  # Adjust to fill exactly
            used_plants = self.__adjust_load(load, filled_load, used_plants)

        return used_plants

    def __fill_needs(
        self, load: int, plants: list[PowerPlant]
    ) -> tuple[int, list[PlantUsage]]:
        actual_load = 0
        sorted_plants = list(
            sorted(plants, key=lambda plant: plant.price_per_mwh())
        )  # Sort by price
        plants_usage = []
        while len(sorted_plants) > 0 and actual_load < load:
            actual_load += sorted_plants[0].pmax
            plants_usage.append(PlantUsage(sorted_plants[0], sorted_plants[0].pmax))
            sorted_plants = sorted_plants[1:]

        return actual_load, plants_usage

    def __adjust_load(
        self, load: int, filled_load: int, plants_usage: list[PlantUsage]
    ) -> list[PlantUsage]:
        last_plant = plants_usage[-1]
        if (
            filled_load - last_plant.usage + last_plant.plant.pmin < load
        ):  # Adjusting only the last one if possible
            last_plant.usage -= filled_load - load
        elif len(plants_usage) >= 2:  # Adjust the two last ones otherwise
            plants_usage[-2].usage -= last_plant.plant.pmin
            last_plant.usage = last_plant.plant.pmin
        else:
            raise UnsatifiableError("Can not produce so less power")
        return plants_usage
