import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .constants import DOMAIN, CONF_URL

@config_entries.HANDLERS.register(DOMAIN)
class MacNetworkDataConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MAC Network Data."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Validate the user input
            url = user_input[CONF_URL]
            if self._is_valid_url(url):
                return self.async_create_entry(title="MAC Network Data", data=user_input)
            else:
                errors["base"] = "invalid_url"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_URL): str,
            }),
            errors=errors,
        )

    def _is_valid_url(self, url):
        """Validate the URL."""
        # Add your URL validation logic here
        return True

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MacNetworkDataOptionsFlowHandler(config_entry)

class MacNetworkDataOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for MAC Network Data."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_URL, default=self.config_entry.data.get(CONF_URL)): str,
            }),
        )

