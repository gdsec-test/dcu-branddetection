# Brand Detection
Brand Detection determines the hosting provider and registrar for a given domain or IP. It allows CMAP Service (https://github.secureserver.net/ITSecurity/cmap_service) to enrich abuse report data with registrar and hosting data with the corresponding brand (Goaddy or EMEA). This allows for the appropriate routing of abuse reports.

## Cloning
Create the appropriate folder in your local dev location and clone the repo.
Linux example using python's virtualenvwrapper.
```
mkdir branddetection
cd branddetection
mkvirtualenv branddetection
workon branddetection
git clone git@github.secureserver.net:ITSecurity/branddetection.git
```

## Installing Dependencies
Depenencies:
```
pip install -r requirements.txt
```
Test Depenencies:
```
pip install -r test_requirements.txt
```

## Building
To build a Docker container use a specific target: prod, ote, or dev.
```
make [prod,ote,dev]
```

## Deploying
To deploy the container to kubernetes run one of the deploy targets: prod, ote, or dev.
```
make [prod,ote,dev]-deploy
```

## Testing
Nose tests can be run from within the virtual environment and branddetection directory. A HTML coverage report will be created in a 'cover' directory. Open the index.html file to review the report.
```
nosetests --with-coverage --cover-html --cover-package ./
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
gRPC is used for retrieving domain information from Domain Service: https://github.secureserver.net/ITSecurity/domainservice