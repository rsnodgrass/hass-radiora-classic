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

DOMAIN = "radiora_classic"

CONF_PORT = 'port'
CONF_DIMMERS = 'dimmers'
CONF_SWITCHES = 'switches'

# FIXME: allow multiple bridges?
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
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

    tty = config.get(DOMAIN)

    radiora = get_async_radiora_controller(tty, hass.loop)
    if not radiora:
        LOG.error("Unable to connect to RadioRA Classic Smart Bridge at %s", tty)
        return False
    hass.data[RADIORA_CLASSIC] = radiora

    for component in RADIORA_CLASSIC_COMPONENTS:
       hass.async_create_task(
            discovery.async_load_platform(hass, component, DOMAIN, {}, config)
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
    #    self._radiora.add_subscriber(
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

class RadioRAClassicBridge(Entity):
    """Representation of a Lutron RadioRA Classic bridge."""

    def __init__(self, radiora, name):
        super().__init__()
        self._radiora = radioara
        self._name = "RadioRA Bridge"

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def supported_features(self):
        """Flag supported features."""
        #return SUPPORT_TURN_OFF | SUPPORT_TURN_ON
        return

    async def async_added_to_hass(self):
        """Register callbacks."""
    #    self._radiora.add_subscriber(
    #        self.device_id, self.async_schedule_update_ha_state
    #    )
        return

    async def async_turn_on(self, **kwargs):
        """Turn all lights on."""
        await self._radiora.turn_all_on()

    async def async_turn_off(self, **kwargs):
        """Turn all lights off."""
        await self._radiora.turn_all_off()

    async def async_security_flash_on(self, **kwargs):
        """Turn the security flashing lights on."""
        await self._radiora.turn_flash_on()

    async def async_security_flash_off(self, **kwargs):
        """Turn the security flashing lights off."""
        await self._radiora.turn_flash_off()

    @property
    def is_on(self):
        """Return true if any light controlled by the bridge is on."""
        return True # FIXME: for now, this is "always" on

    async def async_update(self):
        """Call when forcing a refresh of the device."""

        # we only need ONE of the light switches to update to get data for ALL the zones
        await self._radiora.update()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {}


    @property
    def should_poll(self):
        """No polling needed."""
        return True
