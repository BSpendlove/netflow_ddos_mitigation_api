FROM python:3.10-slim-buster

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

WORKDIR /app
COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "consume.py" ]