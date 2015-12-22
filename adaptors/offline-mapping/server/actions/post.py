from datetime import datetime
import json

def post(path, headers, payload):

    try:
        json_data = json.loads(payload)
        print(json_data)


        return(200, "OK")

    except:
        return(500, "Error: Payload failed JSON parsing")
