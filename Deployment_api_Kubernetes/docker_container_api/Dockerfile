FROM ubuntu:20.04

ADD . ./

RUN apt update  && apt install python3-pip -y && pip install -r requirements.txt


CMD python3 main.py
