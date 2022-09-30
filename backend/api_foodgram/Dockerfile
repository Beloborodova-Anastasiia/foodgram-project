FROM python:3.7-slim

WORKDIR /app

# COPY backend/api_foodgram/ .
COPY ./ .


RUN pip3 install -r requirements.txt --no-cache-dir

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
