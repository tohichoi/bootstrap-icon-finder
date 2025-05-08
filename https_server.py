#!/usr/bin/env python
#

from ssl import wrap_socket, PROTOCOL_TLSv1_2  as p
from http.server import HTTPServer, SimpleHTTPRequestHandler as h
import argparse
from pathlib import Path
import tomli
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser('Simple HTTPS Server')
parser.add_argument('--config', '-c', type=Path)
parser.add_argument('--ip', type=str)
parser.add_argument('--port', type=int)
args = parser.parse_args()

def read_config(p):
    with open(p, 'rb') as fd:
        return tomli.load(fd)

if args.config:
    config = read_config(args.config)
else:
    config = config = vars(args)

s = HTTPServer((config['ip'], config['port']), h)
s.socket = wrap_socket(s.socket, server_side=True, certfile=config['certfile'], keyfile=config['keyfile'], ssl_version=p)
logging.info('Serving HTTPS on {ip}:{port} ...')
s.serve_forever()
