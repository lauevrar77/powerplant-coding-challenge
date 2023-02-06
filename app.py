import falcon

from infrastructure.services.services import Services
from web.api.endpoints import Healthcheck
from web.middlewares.timing import TimingMiddleware


def create_app() -> falcon.App:
    """Create the flask application."""
    app = falcon.App(middleware=[TimingMiddleware(Services.logger())])
    app.add_route("/healthcheck", Healthcheck())
    return app
