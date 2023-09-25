# Brand Detection Service
FROM gdartifactory1.jfrog.io/docker-dcu-local/dcu-python3.11:1.1
LABEL MAINTAINER=dcueng@godaddy.com

USER root
RUN apt-get update && apt-get install -y gcc

RUN mkdir -p /tmp/build
RUN apt-get update && apt-get install gcc libffi-dev -y
COPY requirements.txt /tmp/build/
COPY pip_config /tmp/build/pip_config
RUN PIP_CONFIG_FILE=/tmp/build/pip_config/pip.conf python -m pip install --upgrade pip
RUN PIP_CONFIG_FILE=/tmp/build/pip_config/pip.conf pip install -r /tmp/build/requirements.txt

# Move files to new dir

COPY *.py /tmp/build/
RUN apt-get update && apt-get install gcc libffi-dev -y
COPY test_requirements.txt /tmp/build/
COPY README.md /tmp/build/
COPY branddetection /tmp/build/branddetection
COPY pb /tmp/build/pb
RUN PIP_CONFIG_FILE=/tmp/build/pip_config/pip.conf pip install --compile /tmp/build
RUN apt-get remove gcc libffi-dev -y

EXPOSE 5000

COPY ./*.ini ./run.py ./runserver.sh ./settings.py ./setup.py /app/
# cleanup
RUN apt-get remove -y gcc
RUN rm -rf /tmp/build
RUN chown -R dcu:dcu /app
WORKDIR /app
USER dcu

ENTRYPOINT ["/app/runserver.sh"]
