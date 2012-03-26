#!/usr/bin/env python

import cherrypy
import json
import os.path

import controller
import pa_controller

PORT = 8080
HOST = '0.0.0.0'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class HTTPHandler:
    """Handle requests from clients."""
    def __init__(self):
        pass

    @cherrypy.expose
    def current(self):
        """Client asked for current information."""
        return json.dumps(controller.get_current())

    @cherrypy.expose
    def action(self, action=None):
        """Received action. Parse it and send to correct module."""
        if action in ['play', 'pause', 'next', 'prev', 'stop']:
            controller.send_command(action)
            return json.dumps(controller.get_current())
        elif action in ['volUp', 'volDown']:
            pa_controller.change_volume(10 if action == 'volUp' else -10)

# Server configuration
cherrypy.tree.mount(HTTPHandler(), '', config={
     '/': {
        'tools.staticfile.root': CURRENT_DIR + 'static',
        'tools.staticdir.root': CURRENT_DIR,
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
