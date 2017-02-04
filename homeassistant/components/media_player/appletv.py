"""
Support for the roku media player.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/media_player.roku/
"""
import logging

import voluptuous as vol

from homeassistant.components.media_player import (
    MEDIA_TYPE_VIDEO, SUPPORT_NEXT_TRACK, SUPPORT_PLAY_MEDIA,
    SUPPORT_PREVIOUS_TRACK, SUPPORT_VOLUME_MUTE, SUPPORT_VOLUME_SET,
    SUPPORT_SELECT_SOURCE, SUPPORT_PLAY, MediaPlayerDevice, PLATFORM_SCHEMA,
    SUPPORT_NAVIGATION)
from homeassistant.const import (
    CONF_HOST, STATE_IDLE, STATE_PLAYING, STATE_UNKNOWN, STATE_HOME)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = []

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

    print("Discovery Info....")
    print(discovery_info)
    if discovery_info and discovery_info in KNOWN_HOSTS:
        return

    if discovery_info is not None:
        print("hi")
        print(discovery_info)
        _LOGGER.debug('Discovered Roku: %s', discovery_info[0])
        hosts.append(discovery_info[0])

    elif CONF_HOST in config:
        hosts.append(config.get(CONF_HOST))

    rokus = []
    for host in hosts:
        new_roku = RokuDevice(host)
        print("roku...")
        print(new_roku)

        if new_roku.name is None:
            _LOGGER.error("Unable to initialize roku at %s", host)
        else:
            rokus.append(RokuDevice(host))
            KNOWN_HOSTS.append(host)

    add_devices(rokus)

class AppleTVDevice(MediaPlayerDevice):
    """Representation of a Roku device on the network."""

    def __init__(self, host):
        """Initialize the Roku device."""
        from bluefang import connection
        from bluefang import commands

        self.bluetooth = connection.Bluefang()
        self.bluetooth.registerProfile("/omnihub/profile")
        self.bluetooth.start_server()
        self.commands = commands

    def update(self):
        """Retrieve latest state."""
        print("Update")

    def get_source_list(self):
        """Get the list of applications to be used as sources."""
        return ["TODO SOURCE LIST"]

    @property
    def should_poll(self):
        """Device should be polled."""
        return True

    @property
    def name(self):
        """Return the name of the device."""
        return "TODO NAME"

    @property
    def state(self):
        """Return the state of the device."""
        return STATE_UNKNOWN #TODO

    @property
    def supported_media_commands(self):
        """Flag of media commands that are supported."""
        return SUPPORT_APPLE_TV

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        return None #TODO

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        return None #TODO

    @property
    def source(self):
        """Return the current input source."""
        return None #TODO

    @property
    def source_list(self):
        """List of available input sources."""
        return None #TODO

    def media_play_pause(self):
        """Send play/pause command."""
        self.bluetooth.send_command(self.commands.PLAY)

    def media_previous_track(self):
        """Send previous track command."""
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
        print("Select source")
        print(source)

    def navigate(self, command):
        """Navigate up/down/left/right."""
        if self.current_app is not None:
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
            else:
                _LOGGER.warn('Unknown direction: %s', direction)
