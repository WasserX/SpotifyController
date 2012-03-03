import dbus
import os

_PROP_IFACE = 'org.freedesktop.DBus.Properties'
_MAX_VOL = 65536

def _connect_pa():
    if 'PULSE_DBUS_SERVER' in os.environ:
        address = os.environ['PULSE_DBUS_SERVER']
    else:
        bus = dbus.SessionBus()
        server_lookup = bus.get_object("org.PulseAudio1", "/org/pulseaudio/server_lookup1")
        address = server_lookup.Get("org.PulseAudio.ServerLookup1", "Address", dbus_interface=_PROP_IFACE)

    return dbus.connection.Connection(address)


def _get_devices():
	server = _connect_pa() 
	core = server.get_object(object_path="/org/pulseaudio/core1")
	
	_get_proxy = lambda x: server.get_object(object_path=x)
	
	return map(_get_proxy, core.Get('org.PulseAudio.Core1', 'Sinks', dbus_interface=_PROP_IFACE))
	

def get_volume():
	proxy =  _get_devices()[0]
	value = proxy.Get('org.PulseAudio.Core1.Device', 'Volume', dbus_interface=_PROP_IFACE)[0]
	print value
	return (100*value)/_MAX_VOL
	
	
def change_volume(value):
	value = ((_MAX_VOL*(get_volume() + value))/100)
	if value < 0 :
		value = 0
	elif value > _MAX_VOL:
		value = _MAX_VOL
	value = [dbus.UInt32(value)]
	
	proxy = _get_devices()[0]
	proxy.Set('org.PulseAudio.Core1.Device', 'Volume', value, dbus_interface=_PROP_IFACE)
