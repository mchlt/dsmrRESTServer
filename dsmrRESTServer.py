#!/usr/bin/env python3
# dsmr_rest-py - Starts a vert small multi-threaded web server that continuously reads 
# current values from a DSMR (Dutch Smart Meter Requirements), or Slimme Meter, device 
# and serves them in a REST json response.
# The meter reasing is a blocking request, hence the reparate threads for handling
# the http requests.
# requires dsmr_parser from ndokter: https://github.com/ndokter/dsmr_parser 

import json
from re import sub
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5
from dsmr_parser.objects import CosemObject, MBusObject, Telegram
from dsmr_parser.parsers import TelegramParser

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import time

def camelCase(string):
  string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
  return string[0].lower() + string[1:]

serial_reader = SerialReader(
    device='/dev/ttyUSB0',
    serial_settings=SERIAL_SETTINGS_V5,
    telegram_specification=telegram_specifications.V4
)

dsmr_json=''

def d():
    global dsmr_json
    for telegram in serial_reader.read_as_object():
        new_dsmr_json={}
        temp_json = json.loads(telegram.to_json())
        for key in temp_json.keys():
            new_key = camelCase(key)
            new_dsmr_json[new_key] = temp_json[key]
        dsmr_json=json.dumps(new_dsmr_json,indent=3)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.end_headers()
        self.wfile.write(bytes(dsmr_json,"utf-8"))
        self.wfile.write(bytes("\n","utf-8"))
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':

    d = threading.Thread(name='daemon', target=d)
    d.setDaemon(True)

    d.start()
	
    server = ThreadedHTTPServer(('', 8080), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

