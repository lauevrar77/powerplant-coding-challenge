# powerplant-coding-challenge

## State of the project
* Working solution that respect criterion
* `domain` and `usecases` are covered by some tests but more can (and probably should) be added for a production environment
* The API uses JsonSchema in order to check if the input have the correct format
* The domain check semantic validity of the data
* A healthcheck endpoint have been added for kubernetes liveness and readiness probes

## Still to be done
Other things could be done on this project. However, as the exercise ask to not spend more than 4 hours on the project, I will leave it as it is now.

These things are : 
* Add pollution in cost calculation :
  * Create a GasPowerPlant that inherit from PowerPlant
  * Add 0.3 (tons of CO2 per MWH) * `price_per_co2_tons` in the fuel price for GasPowerPlant in the PlantFactory
* Test PlantFactory more thoroughly
* Test more test cases for the ProductionPlanner
  * Ask to field domain experts ?
* Test the API
  * Send valid and invalid cases and check return and status code
* Refactor the domain for WindPowerPlant to avoid using the fuel_price field as a placeholder for wind_force
* The code should clear enough to not necessitate any comment but comments and proper documentation could be added if it is required by the client

## Requirements
* Developped with Python 3.10+ but every version > 3.8 should work

## How to run
### With Docker
```bash
docker build -t powerplant-lauevrar77:v1.0.0 .
docker run -d -p 8888:8888 powerplant-lauevrar77:v1.0.0
```

### Bare metal
```bash
pip3 install -r requirements.txt
gunicorn --bind=0.0.0.0:8888 --worker-class=gevent --worker-connections=1000 --workers=3 wsgi
```

## How to test
With dependencies installed : 
```
python3 -m pytest .
```
