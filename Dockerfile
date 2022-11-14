FROM python:3.10.8-alpine3.16

RUN mkdir app
WORKDIR /app
COPY ./app/* /app/
COPY ./requirements.txt /app/requirements.txt 

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "python3", "/app/bot.py" ]
