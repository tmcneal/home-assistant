"""
Support for the Apple TV media player.
"""
import logging

import voluptuous as vol
import traceback

from homeassistant.components.media_player import (
    MEDIA_TYPE_VIDEO, SUPPORT_NEXT_TRACK, SUPPORT_PLAY_MEDIA,
    SUPPORT_PREVIOUS_TRACK, SUPPORT_VOLUME_MUTE, SUPPORT_VOLUME_SET,
    SUPPORT_SELECT_SOURCE, SUPPORT_PLAY, MediaPlayerDevice, PLATFORM_SCHEMA,
    SUPPORT_NAVIGATION)
from homeassistant.const import (
    CONF_HOST, STATE_IDLE, STATE_PLAYING, STATE_UNKNOWN, STATE_HOME)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = []

KNOWN_HOSTS = []

_LOGGER = logging.getLogger(__name__)

SUPPORT_APPLE_TV = SUPPORT_PREVIOUS_TRACK | SUPPORT_NEXT_TRACK |\
    SUPPORT_PLAY_MEDIA | SUPPORT_VOLUME_SET | SUPPORT_VOLUME_MUTE |\
    SUPPORT_SELECT_SOURCE | SUPPORT_PLAY | SUPPORT_NAVIGATION

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST): cv.string,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Apple TV platform."""
    hosts = []

    print("APPLETV2 Discovery Info....")
    print(discovery_info)
    traceback.print_tb
    if discovery_info and discovery_info in KNOWN_HOSTS:
        print("Apple tv returning")
        print(KNOWN_HOSTS)
        return

    if discovery_info is not None:
        print("hioe")
        print(discovery_info)
        _LOGGER.debug('Discovered Apple TV: %s', discovery_info)
        hosts.append(discovery_info)
    elif CONF_HOST in config:
        hosts.append(config.get(CONF_HOST))

    appletvs = []
    print("APPLETV2 hostssss")
    print(hosts)
    for host in hosts:
        print("apple tv...")
        new_appletv = AppleTVDevice(host)
        print(new_appletv)

        if new_appletv.name is None:
            _LOGGER.error("Unable to initialize Apple TV at %s", host)
        else:
            appletvs.append(new_appletv)
            KNOWN_HOSTS.append(host)

    print("Adding these devices...")
    print(appletvs)
    add_devices(appletvs)

class AppleTVDevice(MediaPlayerDevice):
    """Representation of a Apple TV device on the network."""

    def __init__(self, device):
        """Initialize the Apple TV device."""
        from bluefang import connection
        from bluefang import commands

        self.device = device
        self.bluetooth = connection.Bluefang()
        try:
            self.bluetooth.registerProfile("/omnihub/profile")
        except:
            print("Profile already exists. Skipping...")
        print("APPLE TV CONNECTING")
        print(device.address)
        self.bluetooth._scan_timeout()
        self.bluetooth.connect(device.address)
        print("APPLE TV CONNECTION ESTABLISHED")
        self.commands = commands

    def update(self):
        """Retrieve latest state."""
        print("APPLETV2 Update")

    def get_source_list(self):
        """Get the list of applications to be used as sources."""
        print("APPLETV2 getsource")
        return ["TODO SOURCE LIST"]

    @property
    def should_poll(self):
        """Device should be polled."""
        print("APPLETV2 shouldpoll")
        return True

    @property
    def name(self):
        """Return the name of the device."""
        print("APPLETV2 name")
        return "APPLE TVizzle"

    @property
    def state(self):
        """Return the state of the device."""
        print("APPLETV2 state")
        return STATE_UNKNOWN #TODO

    @property
    def supported_media_commands(self):
        """Flag of media commands that are supported."""
        print("APPLETV2 supportedmedia")
        return SUPPORT_APPLE_TV

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        print("APPLETV2 mediacontenttype")
        return None #TODO

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        print("APPLETV2 mediaimageurl")
        return None #TODO

    @property
    def source(self):
        """Return the current input source."""
        print("APPLETV2 source")
        return None #TODO

    @property
    def source_list(self):
        """List of available input sources."""
        print("APPLETV2 sourcelist")
        return None #TODO

    def media_play_pause(self):
        """Send play/pause command."""
        print("APPLETV2 mediaplaypause")
        self.bluetooth.send_command(self.commands.PLAY)

    def media_previous_track(self):
        """Send previous track command."""
        print("APPLETV2 mediaprevioustrack")
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
        print("APPLETV2 Select source")
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
