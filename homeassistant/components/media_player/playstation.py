"""
Support for Playstation 3.
"""
import logging

import voluptuous as vol
import traceback

from homeassistant.components.media_player import (
    SUPPORT_NEXT_TRACK, SUPPORT_PLAY_MEDIA,
    SUPPORT_PREVIOUS_TRACK, SUPPORT_VOLUME_MUTE, SUPPORT_VOLUME_SET,
    SUPPORT_SELECT_SOURCE, SUPPORT_PLAY, MediaPlayerDevice, PLATFORM_SCHEMA)
from homeassistant.const import (
    CONF_HOST, STATE_ON)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = []

KNOWN_HOSTS = []

_LOGGER = logging.getLogger(__name__)

SUPPORT_PLAYSTATION_3 = SUPPORT_PREVIOUS_TRACK | SUPPORT_NEXT_TRACK |\
    SUPPORT_PLAY_MEDIA | SUPPORT_VOLUME_SET | SUPPORT_VOLUME_MUTE |\
    SUPPORT_SELECT_SOURCE | SUPPORT_PLAY

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Playstation 3 platform."""
    hosts = []

    print("PS3 Discovery Info.. NEW!!!")
    print(discovery_info)
    print(add_devices)
    print(config)
    traceback.print_tb
    if discovery_info and discovery_info in KNOWN_HOSTS:
        print("PS3 returning")
        print(KNOWN_HOSTS)
        return

    if discovery_info is not None:
        print("hioe")
        print(discovery_info)
        _LOGGER.debug('Discovered PS3: %s', discovery_info)
        hosts.append(discovery_info)
    elif CONF_HOST in config:
        hosts.append(config.get(CONF_HOST))

    ps3s = []
    print("PS3 hostssss")
    print(hosts)
    for host in hosts:
        print("PS3...")
        new_ps3 = PS3Device(host)
        print(new_ps3)

        if new_ps3.name is None:
            _LOGGER.error("Unable to initialize PS3 at %s", host)
        else:
            print("ADDING THIS PS3")
            print(new_ps3)
            ps3s.append(new_ps3)
            KNOWN_HOSTS.append(host)

    print("Adding these devices...")
    print(ps3s)
    add_devices(ps3s)


class PS3Device(MediaPlayerDevice):
    """Representation of a PS3 device on the network."""

    def __init__(self, device):
        """Initialize the PS3 device."""
        import bluefang
        from bluefang import commands

        self.device = device
        self.bluetooth = bluefang.Bluefang()
        try: 
            self.bluetooth.register_profile("/omnihub/profile")
        except:
            print("Profile already exists. Skipping...")

        print("PS3 CONNECTING")
        self.bluetooth._scan_timeout()
        self.bluetooth.connect(device.address)
        print("PS3 CONNECTION ESTABLISHED")
        self.commands = commands

    def update(self):
        """Retrieve latest state."""
        print("PS3 Update")

    @property
    def should_poll(self):
        """Device should be polled."""
        print("PS3 shouldpoll")
        return True

    @property
    def name(self):
        """Return the name of the device."""
        return "Playstation 3"

    @property
    def state(self):
        """Return the state of the device."""
        print("PS3 state")
        self.bluetooth.send_command("up")
        self.bluetooth.send_command("left")
        self.bluetooth.send_command("enter")
        return STATE_ON

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        print("PS3 supportedmedia")
        return SUPPORT_PLAYSTATION_3

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        return None

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        return None

    @property
    def source(self):
        """Return the current input source."""
        return None

    @property
    def source_list(self):
        """List of available input sources."""
        return None

    def media_play_pause(self):
        """Send play/pause command."""
        print("PS3 mediaplaypause")
        self.bluetooth.send_command(self.commands.PLAY)

    def media_previous_track(self):
        """Send previous track command."""
        print("PS3 mediaprevioustrack")
        self.bluetooth.send_command(self.commands.PREV_TRACK)

    def media_next_track(self):
        """Send next track command."""
        self.bluetooth.send_command(self.commands.NEXT_TRACK)

    def mute_volume(self, mute):
        """Mute the volume."""
        self.bluetooth.send_command(self.commands.MUTE_VOLUME)

    def volume_up(self):
        """Volume up media player."""
        self.bluetooth.send_command(self.commands.VOLUME_UP)

    def volume_down(self):
        """Volume down media player."""
        self.bluetooth.send_command(self.commands.VOLUME_DOWN)

    def select_source(self, source):
        """Select input source."""
        print("PS3 Select source")
        print(source)

    def navigate(self, command):
        """Navigate up/down/left/right."""
        if command == "up":
            self.bluetooth.send_command(self.commands.UP)
        elif command == "left":
            self.bluetooth.send_command(self.commands.LEFT)
        elif command == "right":
            self.bluetooth.send_command(self.commands.RIGHT)
        elif command == "down":
            self.bluetooth.send_command(self.commands.DOWN)
        elif command == "enter":
            self.bluetooth.send_command(self.commands.ENTER)
        elif command == "cancel":
            self.bluetooth.send_command(self.commands.CANCEL)
        else:
            _LOGGER.warn('Unknown direction: %s', command)
