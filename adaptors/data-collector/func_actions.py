import pymongo
import json
import isodate

from datetime import datetime


MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "rover_collector"


def postData(path, headers, payload):
    request_time = datetime.utcnow()

    required_fields = ['vehicle_id', 'vehicle_data']

    # Validate payload
    try:
        json_data = json.loads(payload)

        for field in required_fields:
            if field not in json_data: return(500, "Error: Payload invalid, missing " + field)        

    except:
        return(500, "Error: Payload failed JSON parsing")

    try:
        vehicle_collection = _mongo_db[json_data['vehicle_id']]
        vehicle_collection.insert({"timestamp":request_time, "vehicle_data": json_data['vehicle_data']})
        return(200, "OK")
    except:
        return(500, "Error: Failed to add vehicle data")


def getMap(query=None):
    date_from = today = datetime.now().strftime('%Y-%m-%d')
    date_to = date_from
    time_from = "00:00:00"
    time_to = "23:59:59"
    
    # Get params from query string
    if query != None:
        params = query.split("?")
        for param in params:
            if "=" in param: 
                key, value = param.split("=")
                if key == "vehicle_id": vehicle_id = value
                if key == "date_from": date_from = value.replace("%20", " ")  
                if key == "date_to": date_to = value.replace("%20", " ")
                if key == "time_from": time_from = value.replace("%20", " ")  
                if key == "time_to": time_to = value.replace("%20", " ")

    else:
        return(500, "Error: Missing query string")
    
    # HTML Header
    html_header = "<!DOCTYPE html>\n\
<html>\n\
  <head>\n\
    <style>\n\
      html, body, #map-canvas {\n\
        width: 600px;\n\
        height: 600px;\n\
      }\n\
    </style>\n\
    <script src=\"https://maps.googleapis.com/maps/api/js\"></script>\n\
    <script>\n\
	function initialize() {\n\
  var bounds = new google.maps.LatLngBounds();\n\
  var mapOptions = {\n\
    zoom: 12,\n\
    center: new google.maps.LatLng(0, 0),\n\
    mapTypeId: google.maps.MapTypeId.ROADMAP\n\
  };\n\
  var map = new google.maps.Map(document.getElementById('map-canvas'),\n\
      mapOptions);\n\
  var flightPlanCoordinates = ["

    # HTML Footer
    html_footer = "var flightPath = new google.maps.Polyline({\n\
    path: flightPlanCoordinates,\n\
    geodesic: true,\n\
    strokeColor: '#FF0000',\n\
    strokeOpacity: 1.0,\n\
    strokeWeight: 2\n\
  });\n\
  flightPath.setMap(map);\n\
}\n\
google.maps.event.addDomListener(window, 'load', initialize);\n\
    </script>\n\
  </head>\n\
  <body>\n\
    <div id=\"map-canvas\"></div>\n\
  </body>\n\
</html>"


    try:
        # Adjust formats
        isodatetime_from = datetime.strptime(date_from + " " + time_from, '%Y-%m-%d %H:%M:%S')
        isodatetime_to = datetime.strptime(date_to + " " + time_to, '%Y-%m-%d %H:%M:%S')

        polygon_cords = ""
        markers = ""

        # Query collection and print
        vehicle_data = _mongo_db[vehicle_id].find({"timestamp" : {"$gte" : isodatetime_from, "$lte" : isodatetime_to}}).sort("timestamp", 1)
    
        for entry in vehicle_data:
            # Build Polgon entries
            response_section = "new google.maps.LatLng(" + str(entry['vehicle_data']['lat']) + "," + str(entry['vehicle_data']['long']) + "),\n"
            polygon_cords = polygon_cords + response_section

            # Build marker entries
            response_section = "var position = new google.maps.LatLng(" + str(entry['vehicle_data']['lat']) + "," + str(entry['vehicle_data']['long']) + ");\n\
            marker = new google.maps.Marker({position: position,\n\
                                      map: map,\n\
                                     title:'" + str(entry['timestamp']) + "',\n\
                                     icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'});\n\
            bounds.extend(position)\n"
            markers = markers + response_section

        # Section closures
        polygon_cords = polygon_cords + "];\n"
        markers = markers + "map.fitBounds(bounds);"

        # Build response
        response = html_header + polygon_cords + markers + html_footer
        return(200, str(response))

    except:
        return(500, "Error: Failed to generate response ")



def _mongoConnect():
    try:
        mongo_client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        mongo_db = mongo_client[MONGO_DB]
        return(mongo_client, mongo_db)

    except:
        assert False, "Error: Unknown error occured while connecting to MongoDB"

_mongo_client, _mongo_db = _mongoConnect()
