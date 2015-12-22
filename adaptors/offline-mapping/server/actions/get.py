from datetime import datetime

def test(path, query=None):
    request_time = datetime.utcnow()

    try:
        
        return(200, "OK")

    except:
        return(500, "Error: Payload failed JSON parsing")
