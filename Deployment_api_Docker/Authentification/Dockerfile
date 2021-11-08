FROM ubuntu:20.04
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests==2.26.0
ADD authentification.py /authentification.py
WORKDIR /
EXPOSE 8000
CMD python3 authentification.py
ENV LOG_AUTHENTIFICATION "0"
