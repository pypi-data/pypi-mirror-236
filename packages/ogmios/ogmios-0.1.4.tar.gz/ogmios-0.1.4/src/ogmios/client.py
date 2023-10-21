from __future__ import annotations
import json

from websockets.sync.client import connect, ClientConnection

from .logger import logger
from .model.ogmios_model import Jsonrpc

from .chainsync.FindIntersection import FindIntersection
from .chainsync.NextBlock import NextBlock


class Client:
    """
    Ogmios connection client

    A subset of Ogmios functions require the use of WebSockets. Therefore a
    WebSocket connection is preferred over HTTP. If http_only is set to True,
    functions that require WebSockets will not be available.

    If secure is set to False, ws / http will be used rather than wss / https

    :param host: The host of the Ogmios server
    :type host: str
    :param port: The port of the Ogmios server
    :type port: int
    :param secure: Use secure connection
    :type secure: bool
    :param http_only: Use HTTP connection
    :type http_only: bool
    :param compact: Use compact connection
    :type compact: bool
    :param rpc_version: The JSON-RPC version to use
    :type rpc_version: Jsonrpc
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 1337,
        secure: bool = False,
        http_only: bool = False,
        compact: bool = False,
        rpc_version: Jsonrpc = Jsonrpc.field_2_0,
    ) -> None:
        if http_only:
            protocol: str = "https" if secure else "http"
            # TODO: Implement HTTP connections
            logger.error("HTTP connections not implemented")
            exit(-1)
        else:
            protocol: str = "wss" if secure else "ws"

        if compact:
            # TODO: Need to add header:
            # ("Sec-WebSocket-Protocol", "ogmios.v1:compact")
            logger.error("Compact connection not implemented")

        self.rpc_version = rpc_version

        connect_str: str = f"{protocol}://{host}:{port}"
        self.connection: ClientConnection = connect(connect_str)

        # Ogmios methods
        self.find_intersection = FindIntersection(self)
        self.next_block = NextBlock(self)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Close client connection when finished"""
        self.connection.close()

    def send(self, request: str) -> None:
        """Send a request to the Ogmios server

        :param request: The request to send
        :type request: str
        """
        self.connection.send(request)

    def receive(self) -> dict:
        """Receive a response from the Ogmios server

        :return: Request response
        """
        return json.loads(self.connection.recv())
