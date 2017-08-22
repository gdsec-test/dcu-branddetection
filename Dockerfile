# Brand Detection Service
#

FROM alpine:3.5
MAINTAINER DCU <DCUEng@godaddy.com>

RUN addgroup -S dcu && adduser -H -S -G dcu dcu
# apk installs
RUN apk --no-cache add build-base \
    coreutils \
    python-dev \
    py-pip

# Move files to new dir
COPY ./logging.yml ./run.py ./runserver.sh ./settings.py ./setup.py /app/
COPY . /tmp

# pip install private pips staged by Makefile
RUN entry in blindAl; \
    do \
    pip install --compile "/tmp/private_pips/$entry"; \
    done

# install other requirements
RUN pip install --compile /tmp

# cleanup
RUN rm -rf /tmp/* && chown -R dcu:dcu /app

WORKDIR /app
ENTRYPOINT ["/app/runserver.sh"]
