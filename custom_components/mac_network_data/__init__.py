import json
import os
import logging

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .sensor import async_setup_platform
from .constants import DOMAIN, LOGGER

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Network Data integration."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the mac_network_data integration."""
    # This will register the platform with Home Assistant
    hass.data[DOMAIN] = {}

    # Register platform
    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    return True
