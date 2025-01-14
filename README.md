# mac_json Integration for Home Assistant

This custom integration fetches network data from a specified URL and creates sensors for devices based on their MAC addresses.

## Installation

1. Install this integration via HACS or manually.
2. Add the following to your `configuration.yaml`:

```yaml
sensor:
  - platform: mac_json
    url: "https://server.lan/network_ping.cgi?mode=load"
