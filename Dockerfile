FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /run_data && mkdir /api_data && mkdir /log
WORKDIR /api_data
COPY ./flask /api_data
RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "run.ini"]
