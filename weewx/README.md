# Home Assistant Add-on: WeeWX
_This Addon deploys an instance of Weewx server running within the HASSIO Docker environment. This implementation is built ontop of the Official HA Base Alpine image, but leverages the work previously done by [@felddy](https://github.com/felddy)in the [weewx-docker](https://github.com/felddy/weewx-docker) project._

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-TBD-lightgrey.svg

This implementation was built with the intent to leverage the interceptor weewx [weewx-interceptor](https://github.com/matthewwall/weewx-interceptor) extension to accept the Weather Underground redirected rtupdate payloads and push them to Home Assistant using the [weewx-home-assistant](https://github.com/felddy/weewx-home-assistant) extention via MQTT. 

It is possible to do this all within HASSIO with the following:

- Adguard Home addon to enable DNS rewrites to redirect requests from the web to the weewx instance.
- MQTT integrated into Home Assistant via the MQTT integration, I leverage the Mosquitto broker addon.
- Caddy 2 addon to redirect requests to the 

This addon currently:

- Provides and installs extensions above into the container at build and provides baseline config on first boot.
- Takes in basic configuration via the Home Assistant UI before first start and applies it to the `weewx.conf` configuration file.
- DOES NOT apply updates to values defined in the addon UI to `weewx.conf` after initial configuration. Manual updates required.

See installation and configuration information in the [DOCS.md](./Docs.md) file.