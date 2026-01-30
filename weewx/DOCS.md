# Home Assistant Add-on: WeeWX
## Installation

Once the repository has been added following the instructions in the [README.md](../README.md) at the root of this Git Repository, the Addon can be reinstalled via the Home Assistant Addon Store. 

Creation of the `weewx.conf` configuration file is completed on the first run of the Addon using the `weectl` command embedded in the run script. This activity requires that the initial parameters be entered into the Addon's Configuration UI form. **NOTE**: these Configuration parameters are for the initial creation of the `weewx.conf` file only.

The following information is required:

| Field | Type | Description |
|---|---|---|
| location | String | String that defines the PWS device and where it's located (eg. Home PWS) |
| altitude | Integer | Height of the weather station above sea level |
| altitude_format | Choice | Unit of measurement `altitude`field is expressed in. Either feet or meters |
| latitude | Float | Latitude of the weather station expressed in decimal degrees |
| longitude | Float | Longitude of the weather station expressed in decimal degrees |
| display_units | Choice | Unit of measurement used by reports by default. Options are US, METRIC and METRICWX. More information [here](https://weewx.com/docs/5.2/reference/units/).|

Once these parameters are configured, the Addon can be started, and the required configuration will be created. ALL future changes will need to be done in the `weewx.conf` file directly. This file can be found in the Addon's directory in `addons_config`.

## Setup weewx-interceptor for Weather Underground

###Configure Interceptor
Most of the configuration for the interceptor extension is done through the `weectl station reconfigure` command in the Addon's run script.
 
In addition to this automated configuration, the device type needs to be adjusted to support the Weather Underground. This is done by updating the `device_type` config option in `weewx.conf` to `wu-client`. This will then require a restart of the Addon.

###DNS Redirection 

Traffic needs to be rewritten by the DNS server within your network; this may mean that you need to deploy and manage a DNS server within your environment.  

For Weather Underground, the DNS hostname that requires rewriting is `rtupdate.wunderground.com`, which needs to point to the reverse web proxy listening on port 80 in front of the addon.

###HTTP Reverse Proxy
You can use any HTTP Reverse proxy of your personal preference. Currenly testing is done using Caddy 2, as there is a stable Addon developed by [@einschmidt](https://github.com/einschmidt). This is required as WeeWX listens by default on port 48080. 

The following is added to the `Caddyfile` to enable forwarding. This example is to support accepting Weather Underground data to their `rtupdate`subdomain endpoint. 

```
http://rtupdate.wunderground.com {
	file_server
	reverse_proxy <Home Assistant IP>:48080 {
		transport http {
			dial_timeout 2s
			response_header_timeout 30s
		}
	}
}
```

## Setup integration with Home Assistant

Integration between Home Assistant and WereWX is achieved through MQTT. The most common solution to this is the [Mosquitto Broker Addon](https://github.com/home-assistant/addons/blob/master/mosquitto/DOCS.md), which can be shared by other MQTT integrations such as zigbee2mqtt etc.

You will need user credentials for your MQTT broker. The example below using Mosquitto broker: 

```
[HomeAssistant]
    node_id = weewx
    [[mqtt]]
        hostname = core-mosquitto
        port = 1883
        password = weewx
        username = weewx
        use_tls = False
    [[station]]
        name = Weather Station
        model = XYZ
        manufacturer = ABC
```
This block is added to the root of the `weewx.conf` file. 

Now that the config is defined for the extension, it needs to be added to the `[[Services]]` configuration to be run as a component of the application. This is done by adding `weewx_ha.Controller` to the `report_services` service register (comma delimited list).