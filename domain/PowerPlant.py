from dataclasses import dataclass


@dataclass
class PowerPlant:
    name: str
    type: str
    fuel_price: float
    efficiency: float
    pmin: int
    pmax: int

    def __post_init__(self):
        if self.fuel_price < 0:
            raise ValueError("Fuel price should be >= 0")

        if self.efficiency < 0:
            raise ValueError("Efficiency should be >= 0")

        if self.pmin < 0:
            raise ValueError("pmin should be >= 0")

        if self.pmax < 0:
            raise ValueError("pmax should be >= 0")

        if self.pmin > self.pmax:
            raise ValueError("pmin should be > pmax")

    def price_per_mwh(self):
        return self.fuel_price / self.efficiency

    def __hash__(self):
        return hash((self.type, self.name))


@dataclass
class WindPowerPlant(PowerPlant):
    _pmin = 0
    _pmax = 0
    _fuel_price = 0

    @property
    def pmin(self) -> float:
        return self._pmin * self.fuel_price / 100

    @pmin.setter
    def pmin(self, pmin: float):
        self._pmin = pmin

    @property
    def pmax(self) -> float:
        return self._pmax * self.fuel_price / 100

    @pmax.setter
    def pmax(self, pmin: float):
        self._pmax = pmin

    def price_per_mwh(self):
        return 0

    def __hash__(self):
        return hash((self.type, self.name))
