# Home Assistant add-on repository - by dalethestirling

This repository contains Home Assistant add-ons I have created to support my SmartHome implementation. Feel free to use them in your own Home Assistant setup and contribute if you like.

### Install this addon Repo.

Select the button below to redirect you to the addon install.

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fdalethestirling%2Fhassio-addons)

To install this addon repository manually, you need to first log in to your Home Assistant instance and navigate to `Settings -> Addons -> Addon Store`. Once in the Addon Store, you need to select the options button (three dots) in the top right corner and select the `Repositories` menu item. 

In the pop-up window, enter [https://github.com/dalethestirling/hassio-addons/tree/main](https://github.com/dalethestirling/hassio-addons/tree/main) into the `Add` text field at the bottom, then select the `Add` button. This will take a second to update, and then you can close the window. 

## Add-ons

This repository contains the following add-ons. Current addons are only built for ARM (aarch64) as I do not have an amd64 environment at this time to validate the builds with.

### [WeeWX add-on](./weewx)

_Weewx implementation with Home Assistant and inteceptor extentions installed and enabled._

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-TBD-lightgrey.svg
