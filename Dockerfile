FROM python:3.13.1-slim

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY ./resources/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /usr/src/app/temp
COPY ./resources/properties.yaml ./temp
COPY ./sources .

VOLUME /data

COPY resources/entrypoint.sh ./
RUN chmod +x entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
