from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
import asyncio
import logging
import socket
import time
from datetime import timedelta
from .const import DOMAIN, CONF_NAME, CONF_IP_ADDRESS, CONF_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    name = entry.data[CONF_NAME]
    host = entry.data[CONF_IP_ADDRESS]
    interval = entry.data[CONF_INTERVAL]

    async def ping():
        try:
            start = time.time()
            await asyncio.get_event_loop().getaddrinfo(host, None)
            latency = round((time.time() - start) * 1000, 2)
            return {"reachable": True, "latency": latency}
        except Exception as e:
            _LOGGER.warning(f"Ping to {host} failed: {e}")
            return {"reachable": False, "latency": None}

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"Ping {host}",
        update_method=ping,
        update_interval=timedelta(seconds=interval),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([PingSensor(coordinator, name, host)], True)

class PingSensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, name, host):
        super().__init__(coordinator)
        self._name = name
        self._host = host

    @property
    def name(self):
        return f"{self._name}"

    @property
    def state(self):
        return "on" if self.coordinator.data["reachable"] else "off"

    @property
    def extra_state_attributes(self):
        return {
            "latency_ms": self.coordinator.data["latency"],
            "host": self._host,
        }

    @property
    def icon(self):
        return "mdi:lan-connect" if self.state == "on" else "mdi:lan-disconnect"
