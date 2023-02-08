import falcon
from falcon.media.validators.jsonschema import validate

from domain.PowerPlant import PowerPlant
from domain.PowerPlantFactory import PowerPlantFactory
from infrastructure.usecases.ProductionPlanner import (
    PlantUsage,
    ProductionPlanner,
    UnsatifiableError,
)


class Healthcheck:
    def on_get(self, _, resp: falcon.Response):
        resp.media = {"success": True}
        resp.status = falcon.HTTP_200


class PlanProduction:
    POST_SCHEMA = {
        "type": "object",
        "properties": {
            "load": {"type": "number"},
            "fuels": {"type": "object"},
            "powerplants": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "efficiency": {"type": "number"},
                        "pmin": {"type": "integer"},
                        "pmax": {"type": "integer"},
                    },
                    "required": ["name", "type", "efficiency", "pmin", "pmax"],
                },
            },
        },
        "required": ["load", "fuels", "powerplants"],
    }

    @validate(POST_SCHEMA)
    def on_post(self, req: falcon.Request, resp: falcon.Response):
        factory = PowerPlantFactory()
        expected_load = req.media["load"]
        prices = req.media["fuels"]
        plants = [
            factory.from_dict(plant, prices) for plant in req.media["powerplants"]
        ]

        try:
            plan = ProductionPlanner().plan(expected_load, plants)
            resp.media = self.__format_plan(plants, plan)
            resp.status = falcon.HTTP_200
        except UnsatifiableError as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_422

    def __format_plan(self, plants: list[PowerPlant], plan: list[PlantUsage]):
        plan_as_dict = {plan_plant.plant: plan_plant.usage for plan_plant in plan}

        return [
            {"name": plant.name, "p": plan_as_dict.get(plant, 0)} for plant in plants
        ]
