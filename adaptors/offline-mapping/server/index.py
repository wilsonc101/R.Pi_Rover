#!/usr/bin/env python
from pprint import pprint 


from mod_python import apache

db = apache.import_module('db/redisdb')

def index(req):
    method = req.method
    with open("/tmp/test.log", "a") as temp_log:

        if method == "POST":
            data = req.form
            temp_log.write(" ---------- " + str(req.method) + " ---------- \n" +
                           data['action'] + "\n" +
                           data['id'] + "\n" +
                           data['type'] + "\n" +
                           data['data'] + "\n" +
                           "-----------------------------\n") 
            return "POST OK"


        elif method == "GET":
            temp_log.write(" ---------- " + str(req.method) + " ---------- \n" +
                           "-----------------------------\n") 
            return "GET OK"
