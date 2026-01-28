<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.1.0

- Transitioned from using the weewx-docker project's image as the base image and moved to hassio-addons/app-base image
- Updated Dockerfile to align with Alpine tooling
- Init now uses s6 overlay for better process management

## 1.0.1

- Updated my_proram script to use hassio config ui
- Added use of bashio library for better access to homeassistant conventions and logging

## 1.0.0

- Initial release
