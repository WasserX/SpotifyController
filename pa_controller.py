
"""
Simple module to control pulseaudio module. Does not have a lot of options
and possibly complicated setups will not work correctly.

get_volume returns the current volume [0-100]

change_volume receives a value in [0-100] to increase or decrease the volume
"""

import dbus
import os

_MAX_VOL = 65536


def _connect_pa():
    """Connect to the PulseAudio Server."""
    if 'PULSE_DBUS_SERVER' in os.environ:
        address = os.environ['PULSE_DBUS_SERVER']
    else:
        bus = dbus.SessionBus()
        server_lookup = bus.get_object("org.PulseAudio1",
                                       "/org/pulseaudio/server_lookup1")
        address = server_lookup.Get("org.PulseAudio.ServerLookup1", "Address",
                                    dbus_interface=dbus.PROPERTIES_IFACE)

    return dbus.connection.Connection(address)


def _get_devices():
    """Return a map of proxies to control each device."""
    server = _connect_pa()
    core = server.get_object(object_path="/org/pulseaudio/core1")

    return [server.get_object(object_path=x) for x in core.Get(
        'org.PulseAudio.Core1', 'Sinks', dbus_interface=dbus.PROPERTIES_IFACE)]


def get_volume():
    """Return the current volume of the first device."""
    proxy = _get_devices()[0]
    value = proxy.Get('org.PulseAudio.Core1.Device', 'Volume',
                      dbus_interface=dbus.PROPERTIES_IFACE)[0]
    print value
    return (100 * value) / _MAX_VOL


def change_volume(value):
    """Increase or decrease the volume of all devices by value in [0-100]."""
    value = ((_MAX_VOL * (get_volume() + value)) / 100)
    if value < 0:
        value = 0
    elif value > _MAX_VOL:
        value = _MAX_VOL
    value = [dbus.UInt32(value)]

    proxy = _get_devices()[0]
    proxy.Set('org.PulseAudio.Core1.Device', 'Volume', value,
              dbus_interface=dbus.PROPERTIES_IFACE)
