# Brand Detection Service

FROM docker-dcu-local.artifactory.secureserver.net/grpcio
MAINTAINER DCU <DCUEng@godaddy.com>

RUN addgroup -S dcu && adduser -H -S -G dcu dcu
# apk installs
RUN apk --no-cache add build-base \
    coreutils \
    ca-certificates \
    openssl-dev \
    linux-headers \
    python-dev \
    py-pip

EXPOSE 5000

# Move files to new dir
COPY ./*.ini ./logging.yaml ./run.py ./runserver.sh ./settings.py ./setup.py /app/
COPY . /tmp

# install other requirements
RUN pip install --compile /tmp && \
    rm -rf /tmp/* && chown -R dcu:dcu /app

WORKDIR /app
ENTRYPOINT ["/app/runserver.sh"]
