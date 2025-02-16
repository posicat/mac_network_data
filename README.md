# mac_network_data Integration for Home Assistant

This custom integration fetches network data from a specified URL and creates sensors for devices based on their MAC addresses.

## Installation

1. Install this integration via HACS or manually.
2. When adding the instegration, you will need a URL to retrieve the .json data from
    Ex https://server.lan/network_ping.cgi?mode=load

See sample_data.json for an idea of what data is in the .json file pulled from that URL
