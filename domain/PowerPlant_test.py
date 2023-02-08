import pytest

from domain.PowerPlant import PowerPlant, WindPowerPlant


def test_plant_creation(subtests):
    with subtests.test("Valid parameters"):
        PowerPlant("plant1", "gas", 10, 30, 10, 1000)
        assert True

    with subtests.test("fuel price < 0"):
        with pytest.raises(ValueError):
            PowerPlant("plant1", "gas", -1, 30, 10, 1000)

    with subtests.test("efficiency < 0"):
        with pytest.raises(ValueError):
            PowerPlant("plant1", "gas", 10, -30, 10, 1000)

    with subtests.test("pmin < 0"):
        with pytest.raises(ValueError):
            PowerPlant("plant1", "gas", 10, 30, -10, 1000)

    with subtests.test("pmax < 0"):
        with pytest.raises(ValueError):
            PowerPlant("plant1", "gas", 10, 30, 10, -1000)

    with subtests.test("pmax < pmin"):
        with pytest.raises(ValueError):
            PowerPlant("plant1", "gas", 10, 30, 1000, 100)


def test_wind_plant_creation(subtests):
    with subtests.test("Valid parameters"):
        WindPowerPlant("plant1", "gas", 10, 30, 10, 1000)
        assert True

    with subtests.test("fuel price < 0"):
        with pytest.raises(ValueError):
            WindPowerPlant("plant1", "gas", -1, 30, 10, 1000)

    with subtests.test("efficiency < 0"):
        with pytest.raises(ValueError):
            WindPowerPlant("plant1", "gas", 10, -30, 10, 1000)

    with subtests.test("pmin < 0"):
        with pytest.raises(ValueError):
            WindPowerPlant("plant1", "gas", 10, 30, -10, 1000)

    with subtests.test("pmax < 0"):
        with pytest.raises(ValueError):
            WindPowerPlant("plant1", "gas", 10, 30, 10, -1000)

    with subtests.test("pmax < pmin"):
        with pytest.raises(ValueError):
            WindPowerPlant("plant1", "gas", 10, 30, 1000, 100)


def test_price_calculation(subtests):
    with subtests.test("Simple power plant"):
        plant = PowerPlant("plant1", "gas", 10, 30, 100, 1000)
        assert plant.price_per_mwh() == plant.fuel_price / plant.efficiency

    with subtests.test("Wind power plant"):
        plant = WindPowerPlant("plant1", "gas", 10, 30, 100, 1000)
        assert plant.price_per_mwh() == 0
