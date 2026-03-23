<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.1.0

- Transitioned from using the weewx-docker project's image as the base image and moved to hassio-addons/app-base image
- Updated Dockerfile to align with Alpine tooling
- Init now uses s6 overlay for better process management

#### 1.1.1

- Updated the servicesd path from example to weewx
- Updated echo statements to use bashio in my_program

#### 1.1.2

- Updated start script to fix challenges with init of config

#### 1.1.3

- Added additional config options to addon config.yaml for initial config of weewx

#### 1.1.4

- Moved weewxd to the exec call in the run script

#### 1.1.5

- Added port configuration to expose interceptor endpoint (48080 by default)
- Added install and configuration docs to the repository 

#### 1.1.6

- Updated weewx to version 5.3.1
- Updated base container to use hassio-addons/base:20.0.1

#### 1.1.7

- Added missing dependency for usb support in in weewx (pyusb) to address https://github.com/dalethestirling/hassio-addons/issues/5

#### 1.1.8

- Update config.yaml to use UART via `uart: true`
- Update config.yaml to use UDEV via `uart: true`

## 1.0.0

- Initial release

#### 1.0.1

- Updated my_proram script to use hassio config ui
- Added use of bashio library for better access to homeassistant conventions and logging


