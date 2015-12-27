#!/usr/bin/env python
from pprint import pprint 

def index(req):

    with open("/tmp/test.log", "a") as temp_log:
        data = req.form
        temp_log.write(" ------ " + str(req.method) + " ------ \n" +
                       data['action'] + "\n" +
                       data['id'] + "\n" +
                       data['type'] + "\n" +
                       data['data'] + "\n") 

    return "OK"

