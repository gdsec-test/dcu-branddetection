# Brand Detection Service

FROM python:3.7.10-slim
LABEL MAINTAINER=dcueng@godaddy.com

RUN addgroup dcu && adduser --disabled-password --disabled-login --no-create-home --ingroup dcu --system dcu

EXPOSE 5000

# Move files to new dir
COPY ./*.ini ./run.py ./runserver.sh ./settings.py ./setup.py /app/
COPY . /tmp

RUN apt-get update && apt-get install gcc -y
RUN pip install --compile /tmp/private_pips/PyAuth
RUN pip install --compile /tmp/private_pips/dcu-structured-logging-flask
# install other requirements
RUN pip install --compile /tmp && rm -rf /tmp/* && chown -R dcu:dcu /app
RUN apt-get remove -y gcc

WORKDIR /app
ENTRYPOINT ["/app/runserver.sh"]
