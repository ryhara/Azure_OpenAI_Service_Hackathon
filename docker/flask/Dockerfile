FROM python:3.9.6

RUN apt-get clean && \
	apt-get update && \
	apt-get install -y sqlite3
RUN mkdir -p /app && \
	mkdir -p /app/instance
COPY ./docs/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm
EXPOSE 5001

ENTRYPOINT ["flask", "run"]