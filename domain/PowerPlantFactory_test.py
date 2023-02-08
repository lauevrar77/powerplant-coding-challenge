import pytest

from domain.PowerPlant import PowerPlant, WindPowerPlant
from domain.PowerPlantFactory import PowerPlantFactory


def test_from_dict(subtests):
    with subtests.test("simple plant"):
        factory = PowerPlantFactory()
        plant = factory.from_dict(
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {"gas(euro/MWh)": 100},
        )

        assert isinstance(plant, PowerPlant)
        assert plant.name == "gasfiredbig1"
        assert plant.type == "gasfired"
        assert plant.fuel_price == 100
        assert plant.efficiency == 0.53
        assert plant.pmin == 100
        assert plant.pmax == 460

    with subtests.test("simple wind plant"):
        factory = PowerPlantFactory()
        plant = factory.from_dict(
            {
                "name": "gasfiredbig1",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 460,
            },
            {"wind(%)": 30},
        )

        assert isinstance(plant, WindPowerPlant)
        assert plant.name == "gasfiredbig1"
        assert plant.type == "windturbine"
        assert plant.fuel_price == 30
        assert plant.efficiency == 1
        assert plant.pmin == 0
        assert plant.pmax == 460 * 0.3
