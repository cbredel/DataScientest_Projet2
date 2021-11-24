FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
ADD test.py /test.py
CMD python3 /test.py


