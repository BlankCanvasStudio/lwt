#!/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Define the directory containing the file
directory = os.path.expanduser('/home/blankcanvas')
file_name = 'rand-file'

# Define the address and port to serve on
address = ('', 80)

# Custom request handler to serve the file
class FileServingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = os.path.join(directory, file_name)
        print('path:', file_path, os.path.join(directory, file_name))
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'File not found')

# Create an HTTP server with the custom handler
httpd = HTTPServer(address, FileServingHandler)

# Print a message indicating the server is running
print(f'Serving {file_name} at http://localhost:{address[1]}/')

# Start the server
httpd.serve_forever()

