# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM


### Install dependencies
# Install apk packages
RUN apk update && \
    apk add --no-cache wget && \
    apk add --no-cache git && \
    apk add --no-cache python3 && ln -sf python3 /usr/bin/python && \
# Setup python virtual environment
    python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
# Install weewx
    pip install --no-cache weewx   
ENV PATH="/opt/venv/bin:$PATH"
    
# Interceptor extension, allowing capture through DNS redirection
RUN  wget -O /tmp/weewx-interceptor.zip https://github.com/matthewwall/weewx-interceptor/archive/master.zip && \
# Install weewx homeassistant extension     
     pip install --no-cache git+https://github.com/felddy/weewx-home-assistant@v1.0.0


### Add metadata
LABEL org.opencontainers.image.authors="dale.stirling@gmail.com"
LABEL org.opencontainers.image.vendor="dalethestirling"

### Copy root filesystem
COPY rootfs /

