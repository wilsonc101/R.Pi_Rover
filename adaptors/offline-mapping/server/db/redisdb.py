#!/usr/bin/python -B

import redis
import json

import ast

REDIS_SERVER = "localhost"
REDIS_SERVER_PORT = 6379
REDIS_DB = 0

REDIS_CONNECTION = redis.StrictRedis(host=REDIS_SERVER, 
                                     port=REDIS_SERVER_PORT, 
                                     db=REDIS_DB)

def deleteObject(id):
    REDIS_CONNECTION.delete(id)

    return True

    
def createObject(id, type, data):
    json_data = json.loads(data)

    object_data = {}
    object_data['type'] = str(type)
    object_data['coordinates'] = json_data['geometry']['coordinates']
    
    if object_data['type'] == "circle":
        object_data['radius'] = json_data['radius']
    
    REDIS_CONNECTION.set(id,object_data)
    
    return True
    
    
def updateObject(id, type, data):
    json_data = json.loads(data)

    # Get type property from original object
    #original_object = REDIS_CONNECTION.get(id)
    #type = dict(ast.literal_eval(original_object))['type']

    object_data = {}
    object_data['type'] = str(type)
    object_data['coordinates'] = json_data['geometry']['coordinates']
    
    if object_data['type'] == "circle":
        object_data['radius'] = json_data['radius']
    
    REDIS_CONNECTION.set(id,object_data)
    
    return True


def getObjects():
    geoobjects = {}
    object_ids = REDIS_CONNECTION.keys()
    
    for id in object_ids:
        geoobject = dict(ast.literal_eval(REDIS_CONNECTION.get(id)))
        geoobjects[id] = geoobject
        
    return json.dumps(geoobjects)
