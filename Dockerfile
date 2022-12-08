# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000
EXPOSE 27017
CMD ["python", "app.py"]
