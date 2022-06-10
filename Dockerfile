# Brand Detection Service
FROM docker-dcu-local.artifactory.secureserver.net/dcu-python3.7:3.3

LABEL MAINTAINER=dcueng@godaddy.com

USER root
EXPOSE 5000

# Move files to new dir
COPY ./*.ini ./run.py ./runserver.sh ./settings.py ./setup.py /app/
COPY . /tmp

RUN apt-get update && apt-get install gcc -y
RUN PIP_CONFIG_FILE=/tmp/pip_config/pip.conf pip install --compile /tmp && rm -rf /tmp/* && chown -R dcu:dcu /app
RUN apt-get remove -y gcc

WORKDIR /app
USER dcu
ENTRYPOINT ["/app/runserver.sh"]
