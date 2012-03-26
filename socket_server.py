#!/usr/bin/env python

"""
Create a server to serve Spotify properties and accept Spotify Commands
over the network using sockets.

The communication protocol is: lengthJSON, where length is a fixed size
string of length 5 with the length of JSON and JSON is an JSON object
as defined by the API.

The client can send the following commands:
command: "PLAY" | "PAUSE" | "NEXT" | "PREV" | "VOLUP" | "VOLDOWN" | "GET_TRACK"
encapsuled in an object: {command: command}

Once connected, the client should expect a regular message from the server in
that will be
{
status: "Playing" | "Paused" | "Stopped",
metadata:
    {
    album: <String>
    length: <int>
    title: <String>
    artUrl: <String>
    artist: <String>
    }
}
status and metadata are not mandatory and any of them can be absent.
"""

import controller

import socket
import json
from threading import Thread, Lock


HOST = ''
PORT = 15000
ACCEPTED_LENGTH = 5


class Client(Thread):
    """Communicate to a socket client. Assume atomic sends/receive."""
    connection = None
    send_lock = Lock()

    def __init__(self, connection):
        Thread.__init__(self, target=self._receive)
        self.connection = connection
        self.start()

    def notify(self, msg):
        """Execute action sent by client."""
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

    def send(self, msg):
        """Try to obtain a lock to send a msg to a client and send."""
        if not self.connection:
            return False
        self.send_lock.acquire()
        try:
            encoded = json.dumps(msg)
            length = str(len(encoded))
            padded_length = length + ' ' * (ACCEPTED_LENGTH - len(length))
            self.connection.send(padded_length)
            self.connection.send(encoded)
        except socket.error:
            print 'Broken Pipe'
            self.connection = None

        self.send_lock.release()
        return True

    def _receive(self):
        """Runs in a separate thread. Receive json message and call notify."""
        while self.connection:
            try:
                length = int(self.connection.recv(ACCEPTED_LENGTH))
                if length:
                    encoded = self.connection.recv(length)
                    if encoded:
                        msg = json.loads(encoded)
                        self.notify(msg)
            except (ValueError, socket.error):
                print 'Error Receiving message from client'
                self.connection = None


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
        client = Client(client)
        print address
        sp_listener.add_client(client)


if __name__ == '__main__':
    run_server()
