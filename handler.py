#!/usr/bin/env python
# coding: utf-8

# Inspired by chakal http://redirc.org/irc/index.php/foros/46-x-chat/116-controla-el

import os

__module_autor__ = "Wasser"
__module_description__ = "Control and get info from Spotify using JSON"
__module_name__ = "spotifyHandler"
__module_version__ = "1.0"

class Spotify:
	# Gets the current playing track information
	def get_current(self):
		info = os.popen("qdbus org.mpris.MediaPlayer2.spotify \
		/org/mpris/MediaPlayer2 \
		org.freedesktop.DBus.Properties.Get \
		org.mpris.MediaPlayer2.Player \
		Metadata")
		
	  	track = {}
		data = {}
		if info:
			for line in info:
				if ':artist:' in line:
					track['artist'] = line.split(":", 1)[1].rstrip("\n").replace("artist: ", "")
				elif ':album:' in line:
					track['album'] = line.split(":", 1)[1].rstrip("\n").replace("album: ", "")
				elif ':title:' in line:
					track['title'] = line.split(":", 1)[1].rstrip("\n").replace("title: ", "")
				elif ':artUrl:' in line:
					track['artUrl'] = line.split(":", 1)[1].rstrip("\n").replace("artUrl: ", "")
			data['status'] = 'PLAYING'
		else:
			data['status'] = 'NOT_PLAYING'
		
		data['data'] = track
		return data

	def set_status(self, action):
		identifier = "qdbus org.mpris.MediaPlayer2.spotify \
			/org/mpris/MediaPlayer2 \
			org.mpris.MediaPlayer2.Player."
			
		if action == 'play':
			os.popen(identifier +"PlayPause")
		elif action == 'pause':
			os.popen(identifier + "Pause")
		elif action == 'next':
			os.popen(identifier + "Next")
		elif action == 'prev':
			os.popen(identifier + "Previous")
		elif action == 'stop':
			os.popen(identifier + "Stop")
