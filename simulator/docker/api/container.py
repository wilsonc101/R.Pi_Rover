#!/usr/bin/python -B

import pycurl
import json
from StringIO import StringIO

# Start a container using ID provided
def StartContainer(host, port, container_id):
    io_buffer = StringIO()
    
    c = pycurl.Curl()
    c.setopt(c.URL, "http://" + host + "/containers/" + str(container_id) + "/start")
    c.setopt(c.PORT, port)
    c.setopt(c.CUSTOMREQUEST, "POST")
    c.setopt(c.WRITEFUNCTION, io_buffer.write)
    c.perform()

    if c.getinfo(c.RESPONSE_CODE) == 204:
        return True

    else:
        return False


# Use supplied JSON data to create a container
def CreateContainer(host, port, container_config):
    io_buffer = StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, "http://" + host + "/containers/create")
    c.setopt(c.PORT, port)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
    c.setopt(c.POSTFIELDS, container_config)
    c.setopt(c.CUSTOMREQUEST, "POST")
    c.setopt(c.WRITEFUNCTION, io_buffer.write)
    c.perform()

    # Parse response, convert to XML tree
    try:
        json_response = json.loads(io_buffer.getvalue())
        return json_response['Id']

    except:
        return False
