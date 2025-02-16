import aiohttp
import logging
from homeassistant.helpers.entity import Entity

DOMAIN = "network_data"

_LOGGER = logging.getLogger(__name__)

async def fetch_network_data():
    """Fetch the JSON data from the URL."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DATA_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("networkData", {})
                else:
                    _LOGGER.error("Failed to fetch data: HTTP %s", response.status)
    except Exception as e:
        _LOGGER.error("Error fetching network data: %s", e)

    return {}

async def async_setup_entry(hass, entry):
    """Set up the integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["data_url"] = "some_value"
    return True

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensors for network data."""
    network_data = await fetch_network_data(hass)
    sensors = []

    for mac, details in network_data.items():
        sensors.append(NetworkDeviceSensor(mac, details))

    async_add_entities(sensors, update_before_add=True)
    
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
        
async def async_update(self):
    """Fetch new data for the sensor."""
    network_data = await fetch_network_data()
    if self._mac in network_data:
        self._details = network_data[self._mac]
        self._state = self._details.get("ip", "Unknown")
