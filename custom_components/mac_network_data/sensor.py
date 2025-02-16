import aiohttp
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

from .constants import DOMAIN, CONF_URL, LOGGER

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform using config entry."""
    url = config_entry.data[CONF_URL]

    # Store the URL in global data
    hass.data[DOMAIN] = {
        "url": url,
        "network_data": {},  # Initially empty, will be filled after the first fetch
        "entities": []  # List to store sensor entities
    }

    # Update network data for the first time
    await update_network_data(hass, async_add_entities)

    # Update the data every minute
    async_track_time_interval(hass, lambda now: update_network_data(hass, async_add_entities), timedelta(minutes=1))

    return True

async def fetch_network_data(url):
    """Fetch the JSON data from the URL."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("networkData", {})
                else:
                    LOGGER.error("Failed to fetch data: HTTP %s", response.status)
    except Exception as e:
        LOGGER.error("Error fetching network data: %s", e)
  
    return {}

async def update_network_data(hass, async_add_entities):
    """Fetch new network data and update all sensors."""
    url = hass.data[DOMAIN]["url"]
    network_data = await fetch_network_data(url)
    
    if not network_data:
        LOGGER.error("Failed to fetch updated network data.")
        return
    
    # Get the current list of sensor MAC addresses
    existing_macs = {sensor._mac for sensor in hass.data[DOMAIN]["entities"]}

    # Update global data store
    hass.data[DOMAIN]["network_data"] = network_data

    # Process the new network data
    new_sensors = []
    for mac, details in network_data.items():
        if mac not in existing_macs:
            # New sensor, create it and add to the list
            new_sensor = MacNetworkSensor(mac, details)
            new_sensors.append(new_sensor)
            existing_macs.add(mac)

        # Update existing sensors
        for sensor in hass.data[DOMAIN]["entities"]:
            if sensor._mac == mac:
                sensor._details = details
                sensor._state = details.get("ip", "Unknown")
                LOGGER.info(f"Updated sensor {sensor._name}: {sensor._state}")

    # Add new sensors if there are any
    if new_sensors:
        async_add_entities(new_sensors)

class MacNetworkSensor(Entity):
    """Representation of a network device as a sensor."""

    def __init__(self, mac, details):
        """Initialize the sensor."""
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
        # Get the latest data from the global data store
        network_data = self.hass.data[DOMAIN]["network_data"]
        
        if self._mac in network_data:
            self._details = network_data[self._mac]
            self._state = self._details.get("ip", "Unknown")
            LOGGER.info(f"Updated sensor {self._name}: {self._state}")
