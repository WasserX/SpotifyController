
"""
Module with objects to listen to events from Spotify and methods to control it.

SpotifyListener is a class that needs to be subclassed overriding the method
'notify' that receives a dictionary with properties. This method is called each
time Spotify signals there is a change of a status. The contents of the dict
can be a 'status' (Playing, Paused or Stopped) and/or 'metadata' with another
dictionary inside containing track metadata.

send_command receives one of: 'play', 'pause', 'next', 'prev' or 'stop' and
sends the command to Spotify to execute the action. This MAY trigger a 'notify'
in SpotifyListener, but is not always the case.

get_current returns a dictionary with current metadata and/or status of Spotify.
It can be called at any moment. If Spotify is not running, will return an empty
dictionary.
"""

import gobject
from threading import Thread
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from dbus.exceptions import DBusException


SPOTIFY_NS = 'org.mpris.MediaPlayer2.spotify'
GLOBAL_NS = 'org.freedesktop.DBus'

SPOTIFY_OBJ = '/org/mpris/MediaPlayer2'
GLOBAL_OBJ = '/org/freedesktop/DBus'

MEDIAPLAYER_NS = 'org.mpris.MediaPlayer2.Player'
MEDIAPLAYER_OBJ = '/org/mpris/MediaPlayer2'


class SpotifyListener(Thread):
    """Listen for Spotify events and inform updated status to 'notify'."""

    def notify(self, updated):
        """Override this method to receive updated status."""
        pass

    def __init__(self):
        Thread.__init__(self)
        self.bus = dbus.SessionBus(private=True, mainloop=DBusGMainLoop())
        self.listen()
        self.start()

    def run(self):
        loop = gobject.MainLoop()
        gobject.threads_init()
        loop.run()

    def listen(self):
        """Listen for Spotify Metadata, wait if it's not open."""
        try:
            proxy = self.bus.get_object(SPOTIFY_NS, SPOTIFY_OBJ)
            print 'Spotify is running'
            proxy.connect_to_signal('PropertiesChanged', self._props_changed)
        except DBusException:
            print 'Spotify is not running, waiting'
            self._wait_spotify()

    def _wait_spotify(self):
        """Activate a signal to notify when Spotify opens."""
        proxy = self.bus.get_object(GLOBAL_NS, GLOBAL_OBJ)
        proxy.connect_to_signal('NameOwnerChanged', self._name_changed,
        arg0=SPOTIFY_NS)

    def _props_changed(self, *args):
        """When spotify properties changes, parse metadata and notifies."""
        updated = _parse_properties(args[1])
        if updated:
            self.notify(updated)

    def _name_changed(self, *args):
        """When spotify is opened, start listening for changes."""
        self.listen()


def get_current():
    """Return current properties."""
    proxy = _get_proxy()
    properties = {}
    if proxy:
        prop_manager = dbus.Interface(proxy, dbus.PROPERTIES_IFACE)
        properties = _parse_properties(prop_manager.GetAll(MEDIAPLAYER_NS))
    return properties


def send_command(action):
    """Send a command to Spotify."""
    proxy = _get_proxy()
    if proxy:
        if action == 'PLAY':
            proxy.PlayPause()
        elif action == 'PAUSE':
            proxy.Pause()
        elif action == 'NEXT':
            proxy.Next()
        elif action == 'PREV':
            proxy.Previous()
        elif action == 'STOP':
            proxy.Stop()


def _parse_properties(properties):
    """Parse dbus properties and return a normalized dictionary."""
    parsed_properties = {}

    metadata = properties.get('Metadata', {})
    track = {}
    try:
        track['artist'] = unicode(metadata['xesam:artist'][0]).encode('utf8')
        track['album'] = unicode(metadata['xesam:album']).encode('utf8')
        track['title'] = unicode(metadata['xesam:title']).encode('utf8')
        track['artUrl'] = str(metadata['mpris:artUrl'])
        track['length'] = int(metadata['mpris:length'] / 1000)
        parsed_properties['metadata'] = track
    except KeyError:
        pass

    status = properties.get('PlaybackStatus')
    if status == 'Stopped':
        parsed_properties['status'] = 'Stopped'
    elif status == 'Playing':
        parsed_properties['status'] = 'Playing'
    elif status == 'Paused':
        parsed_properties['status'] = 'Paused'

    return parsed_properties


def _get_proxy():
    """Get Spotify dbus proxy."""
    try:
        bus = dbus.SessionBus()
        proxy = bus.get_object(SPOTIFY_NS, MEDIAPLAYER_OBJ)
        return proxy
    except DBusException:
        print 'Spotify is not running'
        return None


if __name__ == "__main__":
    class SpotifyNotifier(SpotifyListener):
        """Class that prints properties when they are changed."""
        def notify(self, updated):
            print updated

    SpotifyNotifier()
