import pytest

from domain.PowerPlant import PowerPlant, WindPowerPlant
from domain.PowerPlantFactory import PowerPlantFactory
from infrastructure.usecases.ProductionPlanner import (
    ProductionPlanner,
    UnsatifiableError,
)


def test_plan(subtests):
    with subtests.test("Working"):
        planner = ProductionPlanner()
        factory = PowerPlantFactory()
        plants = [
            factory.from_dict(
                {
                    "name": "wind1",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 200,
                },
                {"wind(%)": 30},
            ),
            factory.from_dict(
                {
                    "name": "gasfiredbig1",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {"gas(euro/MWh)": 100},
            ),
            factory.from_dict(
                {
                    "name": "gasfiredbig2",
                    "type": "gasfired",
                    "efficiency": 0.50,
                    "pmin": 100,
                    "pmax": 200,
                },
                {"gas(euro/MWh)": 100},
            ),
        ]

        plan = planner.plan(230, plants)
        assert len(plan) == 2
        assert plan[0].plant.name == "wind1"
        assert plan[0].usage == 200 * 0.3
        assert plan[1].plant.name == "gasfiredbig1"
        assert plan[1].usage == 230 - (200 * 0.3)

    with subtests.test("unsatisfiable too less"):
        planner = ProductionPlanner()
        factory = PowerPlantFactory()
        plants = [
            factory.from_dict(
                {
                    "name": "gasfiredbig1",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {"gas(euro/MWh)": 100},
            ),
        ]

        with pytest.raises(UnsatifiableError):
            planner.plan(80, plants)

    with subtests.test("unsatisfiable too much"):
        planner = ProductionPlanner()
        factory = PowerPlantFactory()
        plants = [
            factory.from_dict(
                {
                    "name": "gasfiredbig1",
                    "type": "gasfired",
                    "efficiency": 0.53,
                    "pmin": 100,
                    "pmax": 460,
                },
                {"gas(euro/MWh)": 100},
            ),
        ]

        with pytest.raises(UnsatifiableError):
            planner.plan(480, plants)
