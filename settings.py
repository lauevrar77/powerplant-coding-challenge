import os

APP_NAME = os.getenv("APP_NAME", "powerplant")
DEV = os.getenv("DEV", "True").lower() == "true"
