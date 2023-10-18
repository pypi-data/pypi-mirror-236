from typing import List, Optional
import socket

from tej_protoc import protocol
from tej_protoc.file import File


class ResponseCallback:
    """ To use this class, you must extend available methods according to requirement. """

    client: socket.socket = None
    custom_status: int = 0
    protocol_version: int = 1

    socket_timeout: Optional[int] = None

    def connected(self, client: socket.socket):
        """
        This method is called once the incoming request is validated. The MSB bit must be 1 for valid connection.
        If MSB is not at the expected position, the `ProtocolException` will be raised.
        """

        pass

    def ping(self, files: List[File], message_data: bytes):
        """ This method is called when `PING` status code 1 is received. """

        pass

    def received(self, files: List[File], message_data: bytes):
        """
        This method will be called synchronously for the connected client. However, if it is server it will be
        called parallely if the connection is made to multiple clients.
        """

        pass

    def disconnected(self):
        """
        If the connection is broken or raised `Exception`, this method will be called. Raise `ConnectionClosed`
        exception for notifying connection is closed to the log."""

        pass

    def send(self, data: bytes) -> int:
        """
        Use `self.send(builder.build)` method to send data.
        It uses the same `timeout` set during initialization.
        """

        return protocol.send(self.client, data, self.socket_timeout)
