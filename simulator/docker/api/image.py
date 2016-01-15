#!/usr/bin/python -B

import pycurl 
import json
import os
from StringIO import StringIO


# Return first instance of image matching supplied name (on local server)
def FindImage(host, port, image_name):
    io_buffer = StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, "http://" + host + "/images/search?term=" + image_name)
    c.setopt(c.PORT, port)
    c.setopt(c.WRITEFUNCTION, io_buffer.write)
    c.perform()

    json_response = json.loads(io_buffer.getvalue())

    for i in json_response:
        if i['name'] == image_name: return i

    return False


# Pull images from known sources - DOES NOT START A CONTAINER
def PullImage(host, port, image_name, response_handler):
    c = pycurl.Curl()
    c.setopt(c.URL, "http://" + host + "/images/create?fromImage=" + image_name)
    c.setopt(c.PORT, port)
    c.setopt(c.CUSTOMREQUEST, "POST")
    c.setopt(c.WRITEFUNCTION, response_handler.writelist)
    c.perform()

    return True


# Streams TAR file to URL, tagging with provided tag - DOES NOT START A CONTAINER
def BuildImage(host, port, filepath, tag, response_handler):
    c = pycurl.Curl()
    c.setopt(c.URL, "http://" + host + "/build?t=" + tag)
    c.setopt(c.PORT, port)

    c.setopt(c.CUSTOMREQUEST, "POST")
    c.setopt(c.UPLOAD, 1)    
    c.setopt(pycurl.READFUNCTION, open(filepath, 'rb').read)

    filesize = os.path.getsize(filepath)
    c.setopt(c.INFILESIZE, filesize)

    c.setopt(c.WRITEFUNCTION, response_handler.write)
    c.perform()

    return True




    