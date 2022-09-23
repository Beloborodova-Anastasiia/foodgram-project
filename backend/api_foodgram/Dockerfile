FROM python:3.7-slim

WORKDIR /app

# COPY ./api_foodgram/ .

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
