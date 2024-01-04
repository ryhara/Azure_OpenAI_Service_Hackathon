FROM python:3.9.6

RUN mkdir -p /app
RUN mkdir -p /app/instance
COPY ./requirements.txt /app/requirements.txt
COPY ./instance/config.py /app/instance/config.py

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["flask", "run"]