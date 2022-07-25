#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

from concurrent.futures import thread
import logging
import socketserver
import time

from custom_camera import Cam
from streaming_server import StreamingServer, server
from utils import get_html_from_page_name


class StreamingHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
        global output,useNoir
        if self.path == "/":
            self.send_response(301)
            self.send_header("Location", "/index.html")
            self.end_headers()
        elif self.path == "/index.html":
            content = get_html_from_page_name(self.path).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == "/toggle_profile":
            if(useNoir):
                useNoir = False
            else:
                useNoir = True
            setupCamera()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == "/stream.mjpg":
            self.send_response(200)
            self.send_header("Age", 0)
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header(
                "Content-Type", "multipart/x-mixed-replace; boundary=FRAME"
            )
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b"\r\n")
            except Exception as e:
                logging.warning(
                    "Removed streaming client %s: %s", self.client_address, str(e)
                )
        else:
            self.send_error(404)
            self.end_headers()

def setupCamera():
    global ccam, useNoir, output
    try:
        ccam.__del__()
    except:
        logging.warning("Could not release ccam")
    ccam = Cam(useNoir=useNoir)
    output = ccam.jpeg_streaming_output()

ccam = 0
output = 0
useNoir = False
setupCamera()

try:
    address = ("", 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    logging.info("Done...")
