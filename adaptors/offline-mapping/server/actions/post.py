from datetime import datetime
import json

def post(path, headers, payload):

    try:
        json_data = json.loads(payload)
        
        action = str(json_data['action'])
        type = str(json_data['type'])
        id = str(json_data['id'])
        
        if action == "create":
            if json_data['type'] == "marker":
                coordinates = str(json_data['data']['geometry']['coordinates'])
            
            elif json_data['type'] == "polyline":
                coordinates =  str(json_data['data']['geometry']['coordinates'])
    
            elif json_data['type'] == "polygon":
                coordinates =  str(json_data['data']['geometry']['coordinates'][0])
            
            elif json_data['type'] == "rectangle":
                coordinates =  str(json_data['data']['geometry']['coordinates'][0])
    
            elif json_data['type'] == "circle": 
                coordinates =  str(json_data['data']['geometry']['coordinates'])
                
            object_data = {"id":id, "type":type, "coordinates":coordinates}     

            print str(action + " -- " + str(object_data))

        elif action == "delete":
            object_data = {"id":id}     

            print str(action + " -- " + str(object_data))
            

        
        
        return(200, "OK")

    except:
        return(500, "Error: Payload failed JSON parsing")



#{u'action': u'create', 
# u'data': {u'geometry': {u'type': u'Polygon', 
#                         u'coordinates': [[[-2.147269248962402, 51.446250960584905], 
#                                           [-2.147269248962402, 51.44741443700041], 
#                                           [-2.143428325653076, 51.44741443700041], 
#                                           [-2.143428325653076, 51.446250960584905], 
#                                           [-2.147269248962402, 51.446250960584905]]]}, 
#                         u'type': u'Feature', 
#                         u'properties': {}}, 
# u'type': u'rectangle', 
# u'id': u'b01689f6-8397-4cbb-938c-baaed1b27910'}
