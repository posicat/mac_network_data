import json
import os
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .constants import DOMAIN, LOGGER

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Network Data integration."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Network Data from a config entry."""
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    return True
