#!/usr/bin/env python
from pprint import pprint 


from mod_python import apache

db = apache.import_module('db/redisdb')

def index(req):
    method = req.method
    
    # Method specific actions
    if method == "POST":
        # Extract HTTP form data
        data = req.form

        action = data['action']
        object_id = data['id']
        object_type = data['type']
        geo_data = data['data']

        # Map object actions  
        if action == "create":
            db.createObject(id=object_id, 
                            type=object_type,
                            data=geo_data)
            
        elif action == "delete":
            db.deleteObject(id=object_id)
            
            
        elif action == "edit":
            db.updateObject(id=object_id, 
                            type=object_type,
                            data=geo_data)
            
        return "POST OK"


    elif method == "GET":
        response_data = db.getObjects()
        return response_data
