# Brand Detection Service

FROM docker-dcu-local.artifactory.secureserver.net/grpcio
MAINTAINER DCU <DCUEng@godaddy.com>

RUN addgroup -S dcu && adduser -H -S -G dcu dcu
# apk installs
RUN apk --no-cache add build-base \
    coreutils \
    ca-certificates \
    libffi-dev \
    openssl-dev \
    linux-headers \
    python3-dev \
    py3-pip \
    && ln -s /usr/bin/python3 python \
    && pip3 --no-cache-dir install --upgrade pip

EXPOSE 5000

# Move files to new dir
COPY ./*.ini ./logging.yaml ./run.py ./runserver.sh ./settings.py ./setup.py /app/
COPY . /tmp

RUN pip3 install -U pip
RUN pip3 install cryptography==2.8

# pip install private pips staged by Makefile
RUN for entry in PyAuth; \
    do \
    pip3 install --compile "/tmp/private_pips/$entry"; \
    done

# install other requirements
RUN pip install --compile /tmp && \
    rm -rf /tmp/* && chown -R dcu:dcu /app

WORKDIR /app
ENTRYPOINT ["/app/runserver.sh"]
