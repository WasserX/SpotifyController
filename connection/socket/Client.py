
"""Module to communicate to a client using sockets to send and receive messages.

The messages transmitted will be JSON encoded and the transmission protocol is:

1. Send the message length in a (padded) string of length Client.LENGTH
2. Send the JSON-encoded message

The method 'send(self, msg)' sends a python object to the client
JSON-encoding it before sending.

The Client's __init__ method will start a new thread to receive messages.
An error in the Pipe will be treated internally. But once the pipe is broken
nothing will be sent or received.
To check if the pipe is still alive use the method is_closed.

To personalize this module extend the class Client adding
the method 'notify(self, msg)' that will receive the message emitted
by the client where msg is the object sent by the client already decoded.
By default it will print the message received.
"""

import logging
import json
import socket
from threading import Thread, Lock


class Client(Thread):
    """Communicate to a socket client. Assume atomic sends/receive."""
    LENGTH = 5
    connection = None
    address = None
    send_lock = Lock()

    def __init__(self, connection, address):
        Thread.__init__(self, target=self._receive)
        self.connection = connection
        self.address = address
        self.start()

    def notify(self, msg):
        """Print message sent by client."""
        print 'Client ' + str(self.address) + ' sent: ' + str(msg)

    def send(self, msg):
        """Try to obtain a lock to send a msg to a client and send."""
        if not self.connection:
            return False
        self.send_lock.acquire()
        try:
            encoded = json.dumps(msg)
            length = str(len(encoded))
            padded_length = length + ' ' * (Client.LENGTH - len(length))
            logging.debug('Sending padded length: %s to %s',
                          padded_length, self.address)
            self.connection.send(padded_length)
            logging.debug('Sending encoded JSON: %s to %s',
                          encoded, self.address)
            self.connection.send(encoded)
            logging.info('Sent Message: %s to %s', msg, self.address)
        except socket.error:
            logging.error('Broken Pipe to client %s', self.address)
            self.connection = None

        self.send_lock.release()
        return True

    def is_closed(self):
        """Check if the Pipe is still valid to send and receive messages."""
        return self.connection == None

    def _receive(self):
        """Runs in a separate thread. Receive json message and call notify."""
        while self.connection:
            try:
                length = int(self.connection.recv(Client.LENGTH))
                logging.debug('Received length: %s', length)
                if length:
                    encoded = self.connection.recv(length)
                    logging.debug('Received encoded JSON: %s from %s',
                                  encoded, self.address)
                    if encoded:
                        msg = json.loads(encoded)
                        logging.info('Received Message: %s from %s',
                                     msg, self.address)
                        self.notify(msg)
            except (ValueError, socket.error):
                logging.error('Broken Pipe to client %s', self.address)
                self.connection = None
