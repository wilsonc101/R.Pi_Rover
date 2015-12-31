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
    original_object = REDIS_CONNECTION.get(id)
    type = dict(ast.literal_eval(original_object))['type']

    object_data = {}
    object_data['type'] = type
    object_data['coordinates'] = json_data['geometry']['coordinates']
    
    REDIS_CONNECTION.set(id,object_data)
    
    return True


def getObjects():
    geoobjects = {}
    object_ids = REDIS_CONNECTION.keys()
    
    for id in object_ids:
        geoobject = dict(ast.literal_eval(REDIS_CONNECTION.get(id)))
        geoobjects[id] = geoobject
        
    return json.dumps(geoobjects)


def _correctcoords(data):
    if data['type'] == "marker":
        coordinates = str(data['data']['geometry']['coordinates'])
    
    elif data['type'] == "polyline":
        coordinates =  str(data['data']['geometry']['coordinates'])

    elif data['type'] == "polygon":
        coordinates =  str(data['data']['geometry']['coordinates'][0])
    
    elif data['type'] == "rectangle":
        coordinates =  str(data['data']['geometry']['coordinates'][0])

    elif data['type'] == "circle": 
        coordinates =  str(data['data']['geometry']['coordinates'])
    
    return 
    
#{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-2.14583158493042,51.44720046655099]}}
#{"type":"Feature","properties":{},"geometry":{"type":"LineString","coordinates":[[-2.1425271034240723,51.448083088192334],
#                                                                                 [-2.1448874473571777,51.44694637534],
#                                                                                 [-2.1454238891601562,51.44564915080628]]}}