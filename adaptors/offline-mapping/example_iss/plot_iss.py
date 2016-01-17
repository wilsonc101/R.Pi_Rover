#!/usr/bin/python -B

import redis
import json
import pycurl
import time
import sys

from StringIO import StringIO


REDIS_SERVER = "localhost"
REDIS_SERVER_PORT = 6379
REDIS_DB = 0

REDIS_CONNECTION = redis.StrictRedis(host=REDIS_SERVER, 
                                     port=REDIS_SERVER_PORT, 
                                     db=REDIS_DB)


OBJECT_ID = "iss"

API_URL = "http://api.open-notify.org/iss-now.json"


def createObject(id, type, lat, long):
    object_data = {}
    object_data['type'] = str(type)
    object_data['coordinates'] = [long, lat]
        
    REDIS_CONNECTION.set(id, object_data)
    
    return True


def updateObject(id, type, lat, long):
    object_data = {}
    object_data['type'] = str(type)
    object_data['coordinates'] = [long, lat]
    
    REDIS_CONNECTION.set(id, object_data)
    
    return True


def getAPIData(url):
    io_buffer = StringIO()
    
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.PORT, 80)
    c.setopt(c.WRITEFUNCTION, io_buffer.write)
    c.perform()
    
    # Parse response, convert to XML tree
    try:
        json_response = json.loads(io_buffer.getvalue())
        return json_response

    except:
        return False


def main():
    api_data = getAPIData(API_URL)['iss_position']
    createObject(OBJECT_ID, "marker", api_data['latitude'], api_data['longitude'])    


    while 1:
        time.sleep(5)
        api_data = getAPIData(API_URL)['iss_position']
        updateObject(OBJECT_ID, "marker", api_data['latitude'], api_data['longitude'])    
        print str(api_data)



if __name__ == '__main__':
#    try: 
        main()
#    except (KeyboardInterrupt, SystemExit) as err:
#        print str(err) + " -- Exiting..."

#    except AssertionError as err:
#        print str(err)

#    except:
#        print "Error: unknown error - " + str(sys.exc_info()[0])


# EXAMPLE: 
#{
#  "iss_position": {
#    "latitude": 7.731156008334548, 
#    "longitude": 76.9468962835585
#  }, 
#  "message": "success", 
#  "timestamp": 1453052626
#}






