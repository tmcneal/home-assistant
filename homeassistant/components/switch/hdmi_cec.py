"""
Support for HDMI CEC devices as switches.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/hdmi_cec/
"""
import logging

from homeassistant.components.hdmi_cec import CecDevice, ATTR_NEW
from homeassistant.components.switch import SwitchDevice, DOMAIN
from homeassistant.const import STATE_OFF, STATE_STANDBY, STATE_ON
from homeassistant.core import HomeAssistant

DEPENDENCIES = ['hdmi_cec']

_LOGGER = logging.getLogger(__name__)

ENTITY_ID_FORMAT = DOMAIN + '.{}'


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Find and return HDMI devices as switches."""
    if ATTR_NEW in discovery_info:
        _LOGGER.info("Setting up HDMI devices %s", discovery_info[ATTR_NEW])
        add_devices(CecSwitchDevice(hass, hass.data.get(device),
                                    hass.data.get(device).logical_address) for
                    device in discovery_info[ATTR_NEW])


class CecSwitchDevice(CecDevice, SwitchDevice):
    """Representation of a HDMI device as a Switch."""

    def __init__(self, hass: HomeAssistant, device, logical):
        """Initialize the HDMI device."""
        CecDevice.__init__(self, hass, device, logical)
        self.entity_id = "%s.%s_%s" % (
            DOMAIN, 'hdmi', hex(self._logical_address)[2:])
        self.update()

    def turn_on(self, **kwargs) -> None:
        """Turn device on."""
        #self._device.turn_on()
        self.testing()
        self._state = STATE_ON

    def turn_off(self, **kwargs) -> None:
        """Turn device off."""
        #self._device.turn_off()
        self.testing()
        self._state = STATE_ON
    
    def testing(self):
        print("TRYING A TEST mute")
        from pycec.commands import CecCommand
        # HACK! Second octet gets overwritten with Logical Address gets overwritten in pycec.  For now
        # we overwrite it before sending
        self._device._logical_address = 15
        print("ENTITY ID")
        print(self.entity_id)
        print("DOMAIN")
        print(DOMAIN)
        if 'hdmi_4' in self.entity_id:
            self._device.send_command(CecCommand("EF:82:10:00"))
        elif 'hdmi_8' in self.entity_id:
            self._device.send_command(CecCommand("EF:82:20:00"))
        elif 'hdmi_b' in self.entity_id:
            self._device.send_command(CecCommand("EF:82:30:00"))
        else:
            print("DONT KNOW WHAT TO DO")
        #self.send_keypress(KEY_MUTE_TOGGLE)

    def send_keypress(self, key):
        """Send keypress to CEC adapter."""
        from pycec.commands import KeyPressCommand, KeyReleaseCommand
        _LOGGER.debug("Sending keypress %s to device %s", hex(key),
                      hex(self._logical_address))
        self._device.send_command(
            KeyPressCommand(key, dst=self._logical_address))
        self._device.send_command(
            KeyReleaseCommand(dst=self._logical_address))

    def toggle(self):
        """Toggle the entity."""
        self._device.toggle()
        if self._state == STATE_ON:
            self._state = STATE_OFF
        else:
            self._state = STATE_ON

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        return self._state == STATE_ON

    @property
    def is_standby(self):
        """Return true if device is in standby."""
        return self._state == STATE_OFF or self._state == STATE_STANDBY

    @property
    def state(self) -> str:
        """Cached state of device."""
        return self._state
