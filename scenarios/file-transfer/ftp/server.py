#!/bin/python3

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Define a user with read-only access
authorizer = DummyAuthorizer()
authorizer.add_user("user", "password", "/home/blankcanvas", perm="elr")
# authorizer.add_user("user", "password", "/home/adam", perm="elr")

# Instantiate FTP handler and server
handler = FTPHandler
handler.authorizer = authorizer
handler.permit_foreign_addresses = True


server = FTPServer(("0.0.0.0", 21), handler)


# Start the FTP server
server.serve_forever()

