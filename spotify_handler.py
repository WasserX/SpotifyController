#!/usr/bin/env python

# Inspired by chakal http://redirc.org/irc/index.php/foros/46-x-chat/116-controla-el

import os
import dbus

class Spotify:
	
	def __init__(self):
		self.bus = dbus.SessionBus()
		try:
			self.proxy = self.bus.get_object('org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
		except:
			raise SpotifyNotOpenError
			
	# Gets the current playing track information
	def get_current(self):
		propManager = dbus.Interface(self.proxy, dbus.PROPERTIES_IFACE)
		metadata =  propManager.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
		
		track = {}
		_data = {}

		try:
			track['artist'] = str(metadata['xesam:artist'][0])
			track['album'] = str(metadata['xesam:album'])
			track['title'] = str(metadata['xesam:title'])
			track['artUrl'] = str(metadata['mpris:artUrl'])
		except KeyError as strerror:
		#An error getting one of the parameters means it's not playing
			_data['status'] = 'NOT_PLAYING'
			track = {}
		else:
			_data['status'] = 'PLAYING'
		
		_data['data'] = track
		return _data

	def set_status(self, action):
		if action == 'play':
			self.proxy.PlayPause()
		elif action == 'pause':
			self.proxy.Pause()
		elif action == 'next':
			self.proxy.Next()
		elif action == 'prev':
			self.proxy.Previous()
		elif action == 'stop':
			self.proxy.Stop()

class SpotifyNotOpenError(Exception):
	def __str__(self):
		return 'Cannot open Bus to Spotify. Spotify is closed'			
