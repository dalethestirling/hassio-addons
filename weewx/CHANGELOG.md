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

## 1.0.0

- Initial release

#### 1.0.1

- Updated my_proram script to use hassio config ui
- Added use of bashio library for better access to homeassistant conventions and logging


