FROM ubuntu:22.04

# Install required packages
RUN apt update \
    && apt-get -y upgrade \
    && apt-get install -y build-essential git golang \
    && go version \
    && apt-get install -y libtool pkgconf flex libcurl4-openssl-dev libpcap-dev \
    && apt-get install -y libbz2-dev bison byacc

# Clone and Build nfdump (unicorn branch - 1.7.0)
RUN git clone --branch unicorn https://github.com/phaag/nfdump.git \
    && cd nfdump \
    && bash ./autogen.sh \
    && bash ./configure --enable-nfpcapd --enable-influxdb --enable-shared=false \
    && make \
    && make install \
    && mkdir /tmp/nfcapfiles

# Clone and Build nfinflux data interface
RUN cd ~ \
    && git clone https://github.com/phaag/nfinflux.git \
    && cd nfinflux \
    && go mod tidy \
    && go build \
    && ./nfinflux -socket /tmp/nfdump -host http://influxdb:8086 -org Netflowapi -bucket Flows -token 109a3f01-f6ae-49b4-8027-024b46caaede

# CMD ["nfcapd", "-p", "9995", "-s", "500", "-l", "/tmp/nfcap_files/", "-m", "/tmp/nfdump"]
#RUN chmod +x worker_entrypoint.sh
#ENTRYPOINT ["./worker_entrypoint.sh"]