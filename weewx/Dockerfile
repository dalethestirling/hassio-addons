# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
ARG BASHIO_VERSION="v0.17.5"

FROM $BUILD_FROM

USER root

# Install dependencies
# Interceptor extension, allowing capture through DNS redirection
RUN apt-get update && apt-get install -y wget && \
    wget -O weewx-interceptor.zip https://github.com/matthewwall/weewx-interceptor/archive/master.zip && \
    pip install git+https://github.com/felddy/weewx-home-assistant@v1.0.0

# Install bashio 
RUN wget -O /tmp/bashio.tar.gz "https://github.com/hassio-addons/bashio/archive/refs/tags/${BASHIO_VERSION}.tar.gz" && \
    mkdir /tmp/bashio && \
    tar zxvf /tmp/bashio.tar.gz --strip 1 -C /tmp/bashio && \
    mv /tmp/bashio/lib /usr/lib/bashio && \
    ln -s /usr/lib/bashio/bashio /usr/bin/bashio

# Copy root filesystem
COPY rootfs /

# Update entrypoint to my_program script to leverage params
ENTRYPOINT ["/usr/bin/my_program"]
