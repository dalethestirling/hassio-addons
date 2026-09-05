# Home Assistant Add-on: Radicale

Radicale is a lightweight CalDAV (calendars, todo-lists) and CardDAV (contacts) server.

## Table of Contents

- [Installation](#installation)
- [Configuration Options](#configuration-options)
- [Web Interface](#web-interface)
- [Client Setup Guide](#client-setup-guide)
  - [iOS and macOS (Apple Calendar, Reminders, Contacts)](#ios-and-macos-apple-calendar-reminders-contacts)
  - [Android (DAVx5 and Tasks.org)](#android-davx5-and-tasksorg)
  - [Mozilla Thunderbird](#mozilla-thunderbird)
  - [Home Assistant CalDAV Integration](#home-assistant-caldav-integration)
  - [Windows / Outlook](#windows--outlook)
- [Access Control and Rights Management](#access-control-and-rights-management)
  - [Default Rights](#default-rights)
  - [Shared and Read-Only Calendars](#shared-and-read-only-calendars)
- [Storage Locations and Backups](#storage-locations-and-backups)
- [Reverse Proxy and HTTPS / SSL](#reverse-proxy-and-https--ssl)
- [Troubleshooting and Logs](#troubleshooting-and-logs)

---

## Installation

1. Add this repository to your Home Assistant instance following the instructions in the root [README.md](../README.md).
2. Navigate to **Settings** -> **Add-ons** -> **Add-on Store**.
3. Locate **Radicale** in the store list and select **Install**.
4. Configure initial user accounts in the **Configuration** tab before starting (see [Configuration Options](#configuration-options) below).
5. Start the add-on and check the **Log** tab to verify that the service started successfully.

---

## Configuration Options

Configuration can be set using the Home Assistant UI in the add-on's **Configuration** tab.

| Option | Type | Default | Description |
|---|---|---|---|
| `log_level` | Choice | `info` | Logging verbosity for Radicale. Options: `debug`, `info`, `warning`, `error`. |
| `storage_location` | Choice | `addon_config` | Where collections are stored. Options: `addon_config` (`/config/collections`), `share` (`/share/radicale/collections`), or `internal` (`/data/collections`). |
| `custom_config` | Boolean | `false` | When set to `true`, disables automatic overwriting of user/rights files from the UI and respects `/config/config`, `/config/rights`, and `/config/users` directly. |
| `users` | List | `[{username: "admin", password: ""}]` | List of user accounts to create in the `htpasswd` file. Passwords are automatically hashed using `bcrypt`. |

### Example Add-on Configuration

```yaml
log_level: info
storage_location: addon_config
custom_config: false
users:
  - username: alice
    password: SuperSecretPassword123!
  - username: bob
    password: AnotherSecurePassword456!
```

---

## Web Interface

Radicale includes a built-in web management interface accessible at:

```
http://<HOME_ASSISTANT_IP>:5232/
```

From this web interface, you can:
- Authenticate with any user configured in `users`.
- Create new calendars and address books.
- Rename or delete existing collections.
- Obtain CalDAV and CardDAV collection URLs to paste into your client apps.

---

## Client Setup Guide

### iOS and macOS (Apple Calendar, Reminders, Contacts)

1. Open **Settings** on iOS (or **System Settings** -> **Internet Accounts** on macOS).
2. Select **Calendar** (or **Contacts**) -> **Accounts** -> **Add Account**.
3. Select **Other**, then **Add CalDAV Account** (for calendars/reminders) or **Add CardDAV Account** (for contacts).
4. Enter your connection details:
   - **Server**: `<HOME_ASSISTANT_IP>:5232` (or your reverse proxy domain name)
   - **User Name**: Your configured username (e.g., `alice`)
   - **Password**: Your user password
   - **Description**: `Home Assistant CalDAV`
5. In **Advanced Settings**:
   - Set **Use SSL**: Off (if connecting directly over HTTP) or On (if using a reverse proxy with HTTPS).
   - **Port**: `5232` (or `443` for HTTPS reverse proxy).
   - **Account URL**: `http://<HOME_ASSISTANT_IP>:5232/alice/`

### Android (DAVx5 and Tasks.org)

1. Install **DAVx5** from F-Droid or Google Play Store.
2. Open DAVx5 and tap **+** to add an account.
3. Select **Login with URL and user name**:
   - **Base URL**: `http://<HOME_ASSISTANT_IP>:5232/`
   - **User name**: Your username (e.g., `alice`)
   - **Password**: Your password
4. Tap **Login**. DAVx5 will discover all calendars and address books belonging to your user.
5. Select the collections you wish to sync.

### Mozilla Thunderbird

1. Open Thunderbird and switch to the **Calendar** tab.
2. Under the calendar list on the left, right-click and select **New Calendar...**
3. Select **On the Network** and click **Next**.
4. Enter your credentials:
   - **Username**: Your username (e.g., `alice`)
   - **Location**: `http://<HOME_ASSISTANT_IP>:5232/alice/<calendar_id>/`
5. Click **Find Calendars** and enter your password when prompted.

### Home Assistant CalDAV Integration

You can connect Home Assistant to your Radicale add-on to view and automate against calendar events:

1. In Home Assistant, go to **Settings** -> **Devices & Services** -> **Add Integration**.
2. Search for and select **CalDAV**.
3. Enter the following parameters:
   - **Username**: Your username (e.g., `alice`)
   - **Password**: Your password
   - **URL**: `http://127.0.0.1:5232/alice/` (or `http://localhost:5232/alice/`)
4. Home Assistant will discover the calendars and create calendar entities (e.g., `calendar.personal`).

### Windows / Outlook

Microsoft Outlook does not natively support CalDAV/CardDAV. You can use the free open-source plugin **Outlook CalDav Synchronizer**:
1. Download and install [Outlook CalDav Synchronizer](https://caldavsynchronizer.org/).
2. Open Outlook, select the **CalDav Synchronizer** ribbon tab, and click **Synchronization Profiles**.
3. Add a new profile and configure:
   - **DAV URL**: `http://<HOME_ASSISTANT_IP>:5232/alice/<calendar_id>/`
   - **Username**: `alice`
   - **Password**: Your password

---

## Access Control and Rights Management

Radicale uses a `rights` configuration file located at `/config/rights` (accessible via the `addon_config` folder) to define permissions using regular expressions.

### Default Rights

On first run, Radicale creates the following default rules:

```ini
# Allow root CalDAV/CardDAV discovery
[root]
user = .+
collection =
permissions = r

# Allow internal web interface access
[web]
user = .+
collection = \.web
permissions = r

# Allow users full read/write access to their own collections
[owner-write]
user = .+
collection = {user}(/.*)?
permissions = rw
```

### Shared and Read-Only Calendars

To share a calendar between users, you can edit `/config/rights` and set `custom_config: true` in your add-on options:

```ini
# Allow Alice to read and write to Bob's family calendar
[family-shared]
user = alice
collection = bob/family(/.*)?
permissions = rw

# Allow public or read-only view of a specific calendar for user 'guest'
[guest-readonly]
user = guest
collection = alice/public_events(/.*)?
permissions = r
```

---

## Storage Locations and Backups

The add-on supports three storage location options configured via `storage_location`:

1. **`addon_config`** (Default, Recommended):
   - Path: `/config/collections`
   - Accessible alongside configuration files in Home Assistant's `addon_config/radicale` directory.
   - Included in Home Assistant add-on backups.
2. **`share`**:
   - Path: `/share/radicale/collections`
   - Shared with other add-ons (such as Samba share, Nextcloud, or automated backup scripts).
3. **`internal`**:
   - Path: `/data/collections`
   - Private storage internal to the add-on container.

---

## Reverse Proxy and HTTPS / SSL

When accessing Radicale from outside your local network or when SSL/TLS encryption is required, use a reverse proxy such as Caddy 2, NGINX Home Assistant SSL proxy, or Traefik.

### Caddy 2 Example

Add the following block to your `Caddyfile`:

```caddy
radicale.yourdomain.com {
    reverse_proxy <HOME_ASSISTANT_IP>:5232 {
        header_up X-Forwarded-Port {server_port}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

### NGINX Example

```nginx
server {
    listen 443 ssl http2;
    server_name radicale.yourdomain.com;

    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location / {
        proxy_pass http://<HOME_ASSISTANT_IP>:5232;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_pass_header Authorization;
    }
}
```

---

## Troubleshooting and Logs

- **Viewing logs**: In Home Assistant, open the Radicale add-on page and select the **Log** tab.
- **Increasing log verbosity**: Set `log_level: debug` in the **Configuration** tab and restart the add-on.
- **Authentication failures**: Ensure passwords match what was configured in the UI or `/config/users`. When editing `/config/users` manually, use the `htpasswd -B` command to create bcrypt hashes.
- **Calendar discovery not working**: Verify that your client supports CalDAV discovery at the user root (e.g. `http://<IP>:5232/username/`).
