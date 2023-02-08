import falcon

from infrastructure.services.services import Services
from web.api.endpoints import Healthcheck, PlanProduction
from web.middlewares.timing import TimingMiddleware


def create_app() -> falcon.App:
    """Create the flask application."""
    app = falcon.App(middleware=[TimingMiddleware(Services.logger())])
    app.add_route("/healthcheck", Healthcheck())
    app.add_route("/productionplan", PlanProduction())
    return app
