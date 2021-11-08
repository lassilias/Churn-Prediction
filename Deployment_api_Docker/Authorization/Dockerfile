FROM ubuntu:20.04
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests==2.26.0
ADD authorization.py /authorization.py
WORKDIR /
EXPOSE 8000
CMD python3 authorization.py
ENV LOG_AUTHORIZATION "0"
