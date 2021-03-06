"""
Lutron RadioRA Classic support for Home Assistant
See https://github.com/rsnodgrass/hass-radiora-classic
"""
import logging

from pyradiora_classic import get_async_radiora_controller

import voluptuous as vol

from homeassistant.const import CONF_HOST
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

LOG = logging.getLogger(__name__)

RADIORA_CLASSIC = "radiora_classic"
RADIORA_DOMAIN = "radiora_classic"

CONF_PORT = 'port'
CONF_DIMMERS = 'dimmers'
CONF_SWITCHES = 'switches'

# FIXME: allow multiple bridges?
CONFIG_SCHEMA = vol.Schema(
    {
        RADIORA_DOMAIN: vol.Schema(
            {
                vol.Required(CONF_PORT): cv.string,
                vol.Optional(CONF_SWITCHES): cv.string,
                vol.Optional(CONF_DIMMERS): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

RADIORA_CLASSIC_COMPONENTS = [ "light" ]

async def async_setup(hass, config):
    """Set up the Lutron component."""

    radiora_config = config.get(RADIORA_DOMAIN)
    tty = radiora_config.get(CONF_PORT)
    LOG.debug(f"Loading RadioRA for {tty}")

    radiora = await get_async_radiora_controller(tty, hass.loop)
    if not radiora:
        LOG.error("Unable to connect to RadioRA Classic RS232 at %s", tty)
        return False

    LOG.error("WHO 1 %s", radiora)
    hass.data[RADIORA_CLASSIC] = radiora
    LOG.error("WHO 3 %s", hass.data[RADIORA_CLASSIC])
    radiora.is_zone_on(1) # FIXME

    for component in RADIORA_CLASSIC_COMPONENTS:
       hass.async_create_task(
            discovery.async_load_platform(hass, component, RADIORA_DOMAIN, {}, config)
        )
    return True

class RadioRAClassicDevice(Entity):
    """Common base class for all Lutron RadioRA Classic devices."""

    def __init__(self, radiora, zone, name):
        """Set up the base class.
        [:param]radiora the RadioRA controller
        """
        self._radiora = radiora
        self._name = name
        self._zone = zone
        self._system = 1

    async def async_added_to_hass(self):
        """Register callbacks."""
    #    await self._radiora.add_subscriber(
    #        self.device_id, self.async_schedule_update_ha_state
    #    )
        return

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {}

    @property
    def should_poll(self):
        """No polling needed."""
        return True
