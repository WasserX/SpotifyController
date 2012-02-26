#!/usr/bin/env python

import cherrypy
import json
from handler import *
import os.path

PORT = 8080
HOST = '0.0.0.0'

current_dir = os.path.dirname(os.path.abspath(__file__))

class HTTPHandler:
	@cherrypy.expose
	def current(self):
		spotify = Spotify()
		return json.dumps(spotify.get_current())

	@cherrypy.expose
	def action(self, action=None):
		spotify = Spotify()
		if action in ['play', 'pause', 'next', 'prev', 'stop']:
			spotify.set_status(action)
		return json.dumps(spotify.get_current())

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
