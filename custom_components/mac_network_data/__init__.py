import json
import os
import logging

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import discovery
from .constants import DOMAIN, LOGGER, CONF_URL

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Network Data integration globally (if needed)."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the mac_network_data integration when a config entry is created."""
    url = entry.data[CONF_URL]

    # Store the URL in global data
    hass.data[DOMAIN] = {
        "url": url,
        "network_data": {},  # Initially empty, will be filled after the first fetch
        "entities": []  # List to store sensor entities
    }

    # Forward the setup to the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    return True
