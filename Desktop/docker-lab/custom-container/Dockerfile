FROM ubuntu

RUN apt-get update

RUN apt-get -y install python3

COPY hello_inwk.py /hello_inwk.py

RUN ["chmod", "+x", "/hello_inwk.py"]

CMD ["/hello_inwk.py"]
