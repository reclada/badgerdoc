FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        curl \
        tar \
        gzip \
        python3 \
        python3-pip \
        python3-opencv && \
    python3 -m pip install --upgrade pip setuptools wheel

RUN apt-get install -y --no-install-recommends \
       libgl1-mesa-glx \
       tesseract-ocr-all \
       pkg-config \
       libtesseract-dev \
       libleptonica-dev

RUN  \
    apt-get install -y --no-install-recommends \
        poppler-utils libpoppler-cpp-dev poppler-data \
        cmake make g++ python3-dev git wget libreoffice


RUN pip install gdown==3.12.2 torch==1.7.0 torchvision==0.8.1 pillow==7.2.0 click==7.1.2 scipy==1.5.4
RUN pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cpu/1.7.0/index.html

RUN pip install 'git+https://github.com/open-mmlab/mmdetection.git@v2.7.0'
RUN pip install awscli

COPY . .
RUN ln -s "$PWD/reclada-run.sh" /usr/bin/reclada-run.sh && \
    ln -s "$(which python3)" /usr/bin/python && \
    pip install -r .requirements.txt && \
    ./download.sh

ENTRYPOINT ["bash"]