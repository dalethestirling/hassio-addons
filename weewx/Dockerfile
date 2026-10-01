# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM


### Install dependencies
# Copy requirements first for Docker layer caching
COPY requirements.txt /tmp/requirements.txt

# Install apk packages
RUN apk update && \
    apk add --no-cache wget git libusb python3 && \
    ln -sf python3 /usr/bin/python && \
    python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# Interceptor extension, allowing capture through DNS redirection
RUN wget -O /tmp/weewx-interceptor.zip https://github.com/matthewwall/weewx-interceptor/archive/master.zip


### Add metadata
LABEL org.opencontainers.image.authors="dale.stirling@gmail.com"
LABEL org.opencontainers.image.vendor="dalethestirling"

### Copy root filesystem
COPY rootfs /

RUN chmod +x /etc/services.d/weewx/run
RUN chmod +x /etc/services.d/weewx/finish
