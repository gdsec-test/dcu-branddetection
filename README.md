# Brand Detection
Brand Detection determines the hosting provider and registrar for a given domain or IP. It allows CMAP Service (https://github.secureserver.net/digital-crimes/cmap_service) to enrich abuse report data with registrar and hosting data with the corresponding brand (Goaddy or EMEA). This allows for the appropriate routing of abuse reports.

## Cloning
To clone the repository via SSH perform the following
```
git clone git@github.secureserver.net:digital-crimes/branddetection.git
```

It is recommended that you clone this project into a pyvirtualenv or equivalent virtual environment.

## Installing Dependencies
To install all dependencies for development and testing simply run `make`.

## Building
Building a local Docker image for the respective development environments can be achieved by
```
make [dev, ote, prod]
```

## Deploying
Deploying the Docker image to Kubernetes can be achieved via
```
make [dev, ote, prod]-deploy
```
You must also ensure you have the proper push permissions to Artifactory or you may experience a `Forbidden` message.

## Testing
```
make test     # runs all unit tests
make testcov  # runs tests with coverage
```

## Style and Standards
All deploys must pass Flake8 linting and all unit tests which are baked into the [Makefile](Makfile).

There are a few commands that might be useful to ensure consistent Python style:

```
make flake8  # Runs the Flake8 linter
make isort   # Sorts all imports
make tools   # Runs both Flake8 and isort
```

## Built With
Branddetection uses the following technologies:
1. Docker
2. Flask
3. Redis
4. gRPC

## RIPE API
Branddetection uses RIPE's API to to find IPs associated with each brands Autonomous System Number (ASN) to determin if a given IP or domain is hosted with each brand.

RIPE's API:
https://stat.ripe.net/data/announced-prefixes/data.?

Example API lookup:
https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS3333&starttime=2011-12-12T12:00

This API is documented on:
https://stat.ripe.net/docs/data_api

## Domain Service
gRPC is used for retrieving domain information from Domain Service: https://github.secureserver.net/digital-crimes/domainservice