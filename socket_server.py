#!/usr/bin/env python

"""
Create a server to serve Spotify Notifications and accept Spotify Commands
over the network using sockets.

Protocol Configuration: padded length = 5 (see socket.Client for more info).

A Spotify Command is:
command: "PLAY" | "PAUSE" | "NEXT" | "PREV" | "VOLUP" | "VOLDOWN" | "GET_TRACK"
encapsuled in an object: {command: command}

Once connected, the client should expect a regular Spotify Notification:
{
status: "Playing" | "Paused" | "Stopped",
metadata:
    {
    title:  <String>
    artist: <String>
    album:  <String>
    artUrl: <String>
    length: <int>
    }
}
status and metadata are not mandatory and any of them can be absent.
"""

import controller
import logging
import socket
from connection.socket.Client import Client

HOST = ''
PORT = 15000


class SpotifyClient(Client):
    """Override notify method to receive data and take an action."""

    def __init__(self, client, address):
        Client.__init__(self, client, address)

    def notify(self, msg):
        """Receive command from client and execute it."""
        try:
            command = msg['command']
            if command in ['PLAY', 'PAUSE', 'NEXT', 'PREV']:
                controller.send_command(command)
            elif command == 'GET_TRACK':
                properties = controller.get_current()
                if properties:
                    self.send(properties)
        except KeyError:
            pass


class SpotifyNotifier(controller.SpotifyListener):
    """Catch Properties from Spotify and send to clients."""

    _clients = list()

    def __init__(self):
        controller.SpotifyListener.__init__(self)

    def add_client(self, client):
        """add client to list of clients."""
        self._clients.append(client)

    def notify(self, msg):
        """Inform all clients of a change in properties and remove broken."""
        self._clients = [x for x in self._clients if x.send(msg)]


def run_server():
    """Run the server. Clients are notified of events and can send commands."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    sp_listener = SpotifyNotifier()
    while True:
        client, address = server.accept()
        client = SpotifyClient(client, address)
        logging.info('Client %s connected', address)
        sp_listener.add_client(client)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run_server()
