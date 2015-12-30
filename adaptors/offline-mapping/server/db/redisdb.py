import redis

REDIS_SERVER = "localhost"
REDIS_SERVER_PORT = 6379
REDIS_DB = 0

REDIS_CONNECTION = redis.StrictRedis(host=REDIS_SERVER, 
                                     port=REDIS_SERVER_PORT, 
                                     db=REDIS_DB)

def deleteObject(id):
    nothing = None
    
def createObject(id):
    nothing = None
    return "Things"
    
def updateObject(id):
    nothing = None

    