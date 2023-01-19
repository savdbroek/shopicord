FROM python:3.12.0a3-alpine3.16

RUN apk add --no-cache --update \
    && python3 -m ensurepip \
    && rm -rf /var/cache/apk/*

RUN mkdir app
WORKDIR /app

COPY ./app/ /app/
COPY ./requirements.txt /app/requirements.txt

RUN python3 -m pip install --upgrade pip --no-cache-dir
RUN python3 -m pip install -r requirements.txt --no-cache-dir

CMD [ "python3", "/app/bot.py" ]