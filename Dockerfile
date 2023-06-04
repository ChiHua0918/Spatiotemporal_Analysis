FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /run_data && mkdir /api_data && mkdir /log
WORKDIR /api_data
COPY ./flask /api_data
COPY ./sis /api_data/static/image/sis
COPY ./other/make_gif/image /api_data/static/image/gif
COPY ./contrast/image /api_data/static/image/contrast
COPY ./make_GEI/picture /api_data/static/image/GEI
COPY ./GEI_clustering/clustering /api_data/static/data/clustering
COPY ./make_GEI/data/2018/GEI_regular /api_data/static/data/GEI_regular
COPY ./make_GEI/2018micro.csv /api_data/static/data
COPY ./make_GEI/2018level.csv /api_data/static/data
COPY ./make_GEI/KMeans.csv /api_data/static/data
COPY ./make_GEI/HCED1.csv /api_data/static/data
COPY ./make_GEI/RasterScan4.csv /api_data/static/data

RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "run.ini"]
