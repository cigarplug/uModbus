#!/usr/bin/env python
# scripts/examples/simple_data_store.py
import logging
from socketserver import TCPServer
from collections import defaultdict

from umodbus import get_server, RequestHandler, conf
from umodbus.utils import log_to_stream

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# A very simple data store which maps addresses against their values.
data_store = defaultdict(int)

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

app = get_server(TCPServer, ('localhost', 502), RequestHandler)


@app.route(slave_ids=[1], function_codes=[3, 4], addresses=list(range(0, 10)))
def read_data_store(slave_id, address):
    """" Return value of address. """
    return data_store[address]


@app.route(slave_ids=[1], function_codes=[6, 16], addresses=list(range(0, 10)))
def write_data_store(slave_id, address, value):
    """" Set value for address. """
    data_store[address] = value

if __name__ == '__main__':
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
