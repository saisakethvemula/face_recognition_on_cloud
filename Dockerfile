FROM python:3.8

USER root

WORKDIR /home/

COPY images ./images
copy templates ./templates
COPY docker-entrypoint.sh ./docker-entrypoint.sh
COPY frs.py ./frs.py
COPY processing.jpg ./processing.jpg
COPY requirements.txt ./requirements.txt
COPY test_server.py ./test_server.py
COPY train_server.py ./train_server.py 
COPY msdv.mp4 ./msdv.mp4

RUN chmod +x docker-entrypoint.sh

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y  

RUN apt-get update -y

RUN apt-get install -y libturbojpeg0

EXPOSE 9000
CMD ["./docker-entrypoint.sh"]