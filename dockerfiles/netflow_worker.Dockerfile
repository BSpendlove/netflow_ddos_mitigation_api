FROM ubuntu:22.04

COPY ./requirements.txt /app/requirements.txt

RUN apt update && \
    apt-get -y upgrade && \
    apt-get install -y python3.9 python3-pip && \
    apt-get -y install nfdump && \
    mkdir /tmp/nfcap_files

# Install Requirements
RUN pip3 install -r /app/requirements.txt

WORKDIR /app
COPY . /app

RUN chmod +x worker_entrypoint.sh

# ENTRYPOINT ["/bin/nfcapd", "-p", "9995", "-s", "500", "-l", "/tmp/nfcap_files/"]
ENTRYPOINT ["./worker_entrypoint.sh"]