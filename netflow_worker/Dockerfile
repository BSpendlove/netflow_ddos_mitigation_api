FROM ubuntu:20.04

RUN apt update && \
    apt-get -y upgrade && \
    apt-get -y install nfdump && \
    mkdir /tmp/nfcap_files

ENTRYPOINT ["/bin/nfcapd", "-p", "9995", "-s", "500", "-l", "/tmp/nfcap_files/"]