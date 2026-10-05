FROM alpine:3.20

# Install lightweight exploration utilities
RUN apk add --no-cache \
    bash \
    curl \
    jq \
    figlet \
    htop \
    nano \
    iproute2 \
    procps

WORKDIR /root

COPY welcome.sh /usr/local/bin/welcome.sh
RUN chmod +x /usr/local/bin/welcome.sh

CMD ["/usr/local/bin/welcome.sh"]