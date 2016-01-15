#!/usr/bin/python -B

import pycurl 
import json
from StringIO import StringIO


# Return a JSON document listing all containers
def GetAllContainers(host, port):
    io_buffer = StringIO()
    
    c = pycurl.Curl()
    c.setopt(c.URL, "http://" + host + "/containers/json?all=1")
    c.setopt(c.PORT, port)
    c.setopt(c.WRITEFUNCTION, io_buffer.write)
    c.perform()
    
    # Parse response, convert to XML tree
    try:
        json_response = json.loads(io_buffer.getvalue())
        return json_response

    except:
        return False
