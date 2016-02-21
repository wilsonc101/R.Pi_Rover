#!/usr/bin/python -B

import redis

class redisdbConnection():
    def __init__(self, host, port, db):
        self.connection = redis.StrictRedis(host=host, 
                                            port=port, 
                                            db=db)


    def createObject(self, id, type, lat, long):
        object_data = {}
        object_data['type'] = str(type)
        object_data['coordinates'] = [long, lat]
            
        self.connection.set(id, object_data)
        
        return True


    def updateObject(self, id, type, lat, long):
        object_data = {}
        object_data['type'] = str(type)
        object_data['coordinates'] = [long, lat]
        
        self.connection.set(id, object_data)
        
        return True


# Example:
# createObject(OBJECT_ID, "marker", api_data['latitude'], api_data['longitude'])    
# updateObject(OBJECT_ID, "marker", api_data['latitude'], api_data['longitude'])
