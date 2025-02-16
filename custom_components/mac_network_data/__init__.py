import json
import os
import logging

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .sensor import async_setup_platform
from .constants import DOMAIN, LOGGER

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Network Data integration globally (if needed)."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the mac_network_data integration when a config entry is created."""
    config = entry.data
    
    # Here, instead of using discovery.load_platform, directly call async_setup_platform
    await async_setup_platform(hass, config, async_add_entities, discovery_info=None)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    return True
