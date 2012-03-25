#!/usr/bin/env python

import cherrypy
import json
from spotify_handler import *
from pulseaudio_handler import change_volume, get_volume
import os.path

PORT = 8080
HOST = '0.0.0.0'

current_dir = os.path.dirname(os.path.abspath(__file__))

class HTTPHandler:
	@cherrypy.expose
	def current(self):
		try:
			spotify = Spotify()
			return json.dumps(spotify.get_current())
		except SpotifyNotOpenError:
			return json.dumps(dict(status='NOT_PLAYING', data={}))

	@cherrypy.expose
	def action(self, action=None):
			if action in ['play', 'pause', 'next', 'prev', 'stop']:
				try:
					spotify = Spotify()
					spotify.set_status(action)
					return json.dumps(spotify.get_current())
				except SpotifyNotOpenError:
					return json.dumps(dict(status='NOT_PLAYING', data={}))
			elif action in ['volUp', 'volDown']:
				change_volume(10 if action == 'volUp' else -10)

# Server configuration
cherrypy.tree.mount(HTTPHandler(), '', config={
		'/':{
				'tools.staticfile.root': current_dir + 'static',
				'tools.staticdir.root': current_dir,
				'tools.staticdir.on': True,
				'tools.staticdir.dir': 'static',
				'tools.staticdir.index': 'pages/index.html',
		},
        '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static',
        },
})

cherrypy.config.update({'server.socket_host': HOST,
                        'server.socket_port': PORT,
                       })

# Start the server
cherrypy.quickstart()
