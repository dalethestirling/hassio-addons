# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
# Interceptor extension, allowing capture through DNS redirection
RUN apt-get update && apt-get install -y wget && \
    wget -O weewx-interceptor.zip https://github.com/matthewwall/weewx-interceptor/archive/master.zip && \
    pip install git+https://github.com/felddy/weewx-home-assistant@v1.0.0

# Update entrypoint,sh to use addon /config directory
RUN sed -i 's/\/data/\/config/g' /home/weewx/entrypoint.sh && \
    sed -i '/  echo \"A new set of configurations was created.\"/a\\n  weectl extension install /home/weewx/weewx-interceptor.zip --yes --config=${CONF_FILE}\n\
  weectl station reconfigure --driver=user.interceptor --no-prompt --config=${CONF_FILE}\n\
  echo \"Installed interceptor extension with default config\"' /home/weewx/entrypoint.sh

# Copy root filesystem
COPY rootfs /
