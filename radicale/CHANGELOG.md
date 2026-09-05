<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.0.8

- Fix service restart loop caused by `with-contenv` not propagating the `/opt/venv/bin` PATH into the s6 service environment — radicale module was not found on system Python; changed to use absolute path `/opt/venv/bin/python3 -m radicale`
- Fix `finish` script logic that was allowing any non-crash exit code to silently restart the service; now halts the add-on on any unexpected non-zero exit code to prevent infinite restart loops
- Change process execution to `exec python3 -m radicale --config "${CONFIG_FILE}"`
- Change working directory to `/config` prior to launching Radicale to align terminal and service execution contexts

## 1.0.7

- Remove redundant `RADICALE_CONFIG` environment variable export which caused double config loading and service process exit
- Remove `exec 2>&1` script-level redirection to prevent file descriptor conflicts with `bashio` and `s6-overlay` supervision

## 1.0.6

- Fix rights configuration by updating rule key from `permission` to plural `permissions` for Radicale 3.x compatibility
- Automatically migrate legacy `permission =` entries to `permissions =` in existing `/config/rights` files on startup

## 1.0.5

- Redirect stderr to stdout (`exec 2>&1`) in service `run` script so all Radicale startup errors and Python tracebacks are captured in add-on logs
- Enable unbuffered Python logging output (`PYTHONUNBUFFERED=1`)

## 1.0.4

- Remove deprecated `filesystem_locking` option from `[storage]` config section for Radicale v3 compatibility
- Purge legacy `filesystem_locking` settings from existing configuration files on startup

## 1.0.3

- Add fallback to default `info` log level in service `run` script when `log_level` option is unset or empty

## 1.0.2

- Ensure configuration file is cleanly rewritten on startup when `custom_config` is `false`
- Automatically purge deprecated logging options on existing installations

## 1.0.1

- Fix service restart loop caused by deprecated `config` option under `[logging]` in Radicale v3
- Automatically purge deprecated logging configuration lines from existing installations on startup
- Export `RADICALE_CONFIG` environment variable for service startup

## 1.0.0

- Initial release of the Radicale CalDAV & CardDAV server add-on
- Built on top of official Home Assistant Alpine base image (`hassio-addons/base:20.0.1`)
- S6-overlay v3 process supervision and lifecycle management
- CalDAV (calendars, tasks) and CardDAV (contacts) server support using Radicale 3.x
- Built-in web management interface enabled on port 5232
- User authentication with secure bcrypt password hashing
- Support for multiple storage locations (`addon_config`, `share`, `internal`)
- Automatic configuration and rights generation on first boot
- Access control list / rights configuration support for multi-user setups
- Multi-architecture support for `aarch64` and `amd64`
