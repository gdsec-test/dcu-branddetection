# Brand Detection
Brand Detection determins the hosting provider and registrar for a given domain or IP. It allows CMAP Service (https://github.secureserver.net/ITSecurity/cmap_service) to enrich abuse report data with registrar and hosting data with the corresponding brand (Goaddy or EMEA). This allows for the appropriate routing of abuse reports.

## Cloning
Create the appropriate folder in your local dev location and clone the repo.
Linux example using and python's virtualenvwrapper.
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
Discuss the process of building the project.

## Deploying
To deploy the container to kubernetes run one of the deploy targets
```
make [prod,ote,dev]-deploy
```

## Testing
Nose tests can be from within the virtual environment and branddetection directory. A HTML coverage report will be created in a 'cover' directory. Open the index.html file to review the report.
```
nosetests --with-coverage --cover-html --cover-package ./
```
Sample terminal output:
```
Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
branddetection/__init__.py                           0      0   100%
branddetection/asnhelper.py                         48      2    96%
branddetection/branddetector.py                     78      2    97%
branddetection/brands/__init__.py                    0      0   100%
branddetection/brands/domainfactorybrand.py         19      0   100%
branddetection/brands/emeabrand.py                  33      0   100%
branddetection/brands/godaddybrand.py               27      0   100%
branddetection/brands/heartinternetbrand.py         19      0   100%
branddetection/brands/hosteuropebrand.py            19      0   100%
branddetection/brands/hosteuropeiberiabrand.py      19      0   100%
branddetection/brands/meshdigitalbrand.py           19      0   100%
branddetection/brands/paragonbrand.py               19      0   100%
branddetection/brands/plusserverbrand.py            20      0   100%
branddetection/brands/reg123brand.py                20      0   100%
branddetection/brands/server4ugmbhbrand.py          19      0   100%
branddetection/brands/server4uincbrand.py           19      0   100%
branddetection/brands/veliabrand.py                 19      0   100%
branddetection/domainhelper.py                      79      3    96%
branddetection/interfaces/__init__.py                0      0   100%
branddetection/interfaces/brand.py                  15      0   100%
branddetection/pb/__init__.py                        0      0   100%
branddetection/pb/domain_service.py                 22      4    82%
branddetection/pb/domainservice_pb2.py              98     33    66%
branddetection/pb/domainservice_pb2_grpc.py         24     12    50%
branddetection/rediscache.py                        22     12    45%
run.py                                              32     32     0%
settings.py                                         19      5    74%
setup.py                                             7      7     0%
tests/__init__.py                                    0      0   100%
tests/asnhelper_tests.py                            12      0   100%
tests/branddetector_tests.py                       112      0   100%
tests/domainhelper_tests.py                         59      0   100%
tests/emeabrand_tests.py                            34      0   100%
tests/godaddybrand_tests.py                         32      0   100%
tests/plusserverbrand_tests.py                      28      0   100%
tests/reg123brand_tests.py                          28      0   100%
--------------------------------------------------------------------
TOTAL                                             1020    112    89%
--------------------------------------------------------------------
```

## Built With
A list of technologies that this project utilizes such as Flask, Celery, etc. These should be major architecture technologies and not minutia.

## Other Information (Change section titles for this as necessary)
Provide any other information that may be relevant for understanding or utilizing this project. This may include re-generating files after making code changes or any other relevant information.