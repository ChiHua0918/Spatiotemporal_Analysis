FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /run_data && mkdir /api_data && mkdir && mkdir /log
WORKDIR /api_data
COPY ./flask /api_data \
     ./sis /api_data/static/image/sis \
     ./other/make_gif/image /api_data/static/image/gif \
     ./contrast/image/contrast/image /api_data/static/image/contrast \
     ./make_GEI/picture /api_data/static/image/GEI \
     ./GEI_clustering/clustering ./api_data/static/data/clustering \
     ./make_GEI/data/2018/GEI_regular ./api_data/static/data/GEI_regular \
     ./make_GEI/2018micro.csv ./api_data/static/data/ \
     ./make_GEI/2018level.csv ./api_data/static/data/ \
     ./make_GEI/KMeans.csv ./api_data/static/data/ \
     ./make_GEI/HCED1.csv ./api_data/static/data/ \
     ./make_GEI/RasterScan4.csv ./api_data/static/data/

RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "run.ini"]
