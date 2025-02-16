import aiohttp
import logging
from homeassistant.helpers.entity import Entity

DOMAIN = "network_data"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.url,  # Ensure the URL is valid
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform using YAML."""
    url = config[CONF_URL]

    # Fetch JSON data once to discover available keys
    json_data = await fetch_network_data(url)
    if not json_data:
        _LOGGER.error("Failed to fetch JSON data, skipping sensor creation")
        return

    # Create a sensor for each key in the JSON response
    sensors = [MacNetworkSensor(hass, url, key) for key in json_data.keys()]
    async_add_entities(sensors, True)


async def async_setup(hass, config, async_add_entities):
    """Set up the sensor platform using YAML."""
    if DOMAIN not in config:
        return False

    sensors = []
    for entry in config[DOMAIN]:
      url = entry.get("url", "")

      if not url:
          _LOGGER.error("No URL provided for mac_network_data")
          continue

      # Fetch JSON data once to discover keys
      network_data = await fetch_network_data(url)
      if not json_data:
          _LOGGER.error("Failed to fetch JSON data, skipping sensor creation")
          continue

      # Create a sensor for each key in the JSON response
      for mac, details in network_data.items():
        sensors.append(MacNetworkSensor(mac, details))

    async_add_entities(sensors, update_before_add=True)
    return True

async def fetch_network_data(url):
    """Fetch the JSON data from the URL."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("networkData", {})
                else:
                    _LOGGER.error("Failed to fetch data: HTTP %s", response.status)
    except Exception as e:
        _LOGGER.error("Error fetching network data: %s", e)
  
    return {}
    
class MacNetworkSensor(Entity):
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
