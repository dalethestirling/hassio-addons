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

## 1.0.0

- Initial release

#### 1.0.1

- Updated my_proram script to use hassio config ui
- Added use of bashio library for better access to homeassistant conventions and logging


