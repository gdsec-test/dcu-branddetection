# Brand Detection Service
FROM docker-dcu-local.artifactory.secureserver.net/dcu-python3.7:3.3
LABEL MAINTAINER=dcueng@godaddy.com

USER root
RUN apt-get update && apt-get install -y gcc

RUN mkdir -p /tmp/build
COPY requirements.txt /tmp/build/
COPY pip_config /tmp/build/pip_config
RUN PIP_CONFIG_FILE=/tmp/build/pip_config/pip.conf pip install -r /tmp/build/requirements.txt

# Move files to new dir

COPY *.py /tmp/build/
COPY test_requirements.txt /tmp/build/
COPY README.md /tmp/build/
COPY branddetection /tmp/build/branddetection
COPY pb /tmp/build/pb
RUN PIP_CONFIG_FILE=/tmp/build/pip_config/pip.conf pip install --compile /tmp/build

EXPOSE 5000

COPY ./*.ini ./run.py ./runserver.sh ./settings.py ./setup.py /app/
# cleanup
RUN apt-get remove -y gcc
RUN rm -rf /tmp/build
RUN chown -R dcu:dcu /app
WORKDIR /app
USER dcu

ENTRYPOINT ["/app/runserver.sh"]
