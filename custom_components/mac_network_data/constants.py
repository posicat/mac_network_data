# constants.py

DOMAIN = "mac_network_data"
CONF_URL = "url"
LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = vol.Schema({
    vol.Required(CONF_URL): cv.url,
})
