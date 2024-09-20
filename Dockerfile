FROM ubuntu:20.04

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata

RUN apt install python3 python3-pip python3-dev libssl-dev libffi-dev build-essential \
    ipython3 python3-pyatspi -y 

COPY ./ /code

WORKDIR /code

RUN <<EOF
set -eux
pip3 install --upgrade pip setuptools
python3 setup.py build
python3 setup.py install
EOF

# https://ldtp.freedesktop.org/ldtp-tutorial.pdf