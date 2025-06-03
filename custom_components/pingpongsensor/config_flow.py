from homeassistant import config_entries
import voluptuous as vol
from homeassistant.core import callback
import socket
import ipaddress
from .const import DOMAIN, CONF_NAME, CONF_IP_ADDRESS, CONF_INTERVAL

class PingPongSensorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            name = user_input[CONF_NAME]
            ip_or_host = user_input[CONF_IP_ADDRESS]
            interval = user_input[CONF_INTERVAL]

            try:
                # Validate IP or DNS
                try:
                    ipaddress.ip_address(ip_or_host)
                except ValueError:
                    socket.gethostbyname(ip_or_host)

                return self.async_create_entry(title=name, data=user_input)
            except Exception:
                errors["base"] = "invalid_host"

        schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_IP_ADDRESS): str,
            vol.Required(CONF_INTERVAL, default=60): int,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
