from dependency_injector import containers, providers

from infrastructure.services.logger import logger


class Services(containers.DeclarativeContainer):
    """Application IoC container."""

    logger = providers.Singleton(logger)
