import json
import os
from homeassistant.helpers.entity import Entity

DOMAIN = "network_data"
DATA_FILE_PATH = "/config/network_data.json"

def load_network_data():
    """Load the JSON file with network data."""
    if os.path.exists(DATA_FILE_PATH):
        with open(DATA_FILE_PATH, "r") as file:
            return json.load(file).get("networkData", {})
    return {}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensors for network data."""
    network_data = load_network_data()
    sensors = []

    for mac, details in network_data.items():
        sensors.append(NetworkDeviceSensor(mac, details))

    async_add_entities(sensors, True)

class NetworkDeviceSensor(Entity):
    """Representation of a network device as a sensor."""

    def __init__(self, mac, details):
        self._mac = mac
        self._details = details
        self._name = f"Device {mac}"
        self._state = details.get("ip", "Unknown")

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the attributes of the sensor."""
        return {
            "mac": self._mac,
            "network": self._details.get("net", "Unknown"),
            "time": self._details.get("time", "Unknown"),
            "ago": self._details.get("ago", "Unknown"),
            "message": self._details.get("msg", "Unknown"),
        }
