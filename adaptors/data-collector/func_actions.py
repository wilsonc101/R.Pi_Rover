from datetime import datetime
import json

import isodate
import pymongo

import sys

import pygal
from pygal.style import LightStyle


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
            if field not in json_data: 
                return(500, "Error: Payload invalid, missing " + field)

    except:
        return(500, "Error: Payload failed JSON parsing")

    try:
        vehicle_collection = _mongo_db[json_data['vehicle_id']]
        vehicle_collection.insert({"timestamp":request_time, "vehicle_data": json_data['vehicle_data']})
        return(200, "OK")
    except:
        return(500, "Error: Failed to add vehicle data")


def getMap(query=None, handler=None):
    date_from = datetime.now().strftime('%Y-%m-%d')
    date_to = date_from
    time_from = "00:00:00"
    time_to = "23:59:59"

    # Get params from query string
    if query != None:
        params = query.split("?")
        for param in params:
            if "=" in param:
                key, value = param.split("=")
                if key == "vehicle_id": 
                    vehicle_id = value
                if key == "date_from": 
                    date_from = value.replace("%20", " ")
                if key == "date_to": 
                    date_to = value.replace("%20", " ")
                if key == "time_from": 
                    time_from = value.replace("%20", " ")
                if key == "time_to": 
                    time_to = value.replace("%20", " ")

    else:
        return(500, "Error: Missing query string")

    # HTML Start Header
    html_head_start = "<!DOCTYPE html>\n\
<html>\n\
  <head>\n\
    <style>\n\
      html, body, #map-canvas {\n\
        width: 600px;\n\
        height: 600px;\n\
      }\n\
    </style>\n\
    <script src=\"https://maps.googleapis.com/maps/api/js\"></script>\n\
    <script type=\"text/javascript\" src=\"http://kozea.github.com/pygal.js/javascripts/svg.jquery.js\"></script>\n\
   <script type=\"text/javascript\" src=\"http://kozea.github.com/pygal.js/javascripts/pygal-tooltips.js\"></script>\n\
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

    # HTML End Header
    html_head_end = "var flightPath = new google.maps.Polyline({\n\
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
  </head>\n"


    #HTML Body
    html_body_start = "  <body>\n\
    <div id=\"map-canvas\"></div>\n"

    html_body_end = "  </body>\n\
</html>"


    try:
        # Adjust formats
        isodatetime_from = datetime.strptime(date_from + " " + time_from, '%Y-%m-%d %H:%M:%S')
        isodatetime_to = datetime.strptime(date_to + " " + time_to, '%Y-%m-%d %H:%M:%S')

        polygon_cords = ""
        markers = ""

        xaxis_labels = []
        throttle_positions = []
        direction_positions = []

        # Query collection and print
        vehicle_data = _mongo_db[vehicle_id].find({"timestamp" : {"$gte" : isodatetime_from, "$lte" : isodatetime_to}}).sort("timestamp", 1)

        for entry in vehicle_data:
            # Only add point if postion data is present
            if 'latitude' in entry['vehicle_data'] and 'longitude' in entry['vehicle_data']:
                # Build Polgon entries
                response_section = "new google.maps.LatLng(" + str(entry['vehicle_data']['latitude']) + "," + str(entry['vehicle_data']['longitude']) + "),\n"
                polygon_cords = polygon_cords + response_section

                # Build marker entries
                response_section = "var position = new google.maps.LatLng(" + str(entry['vehicle_data']['latitude']) + "," + str(entry['vehicle_data']['longitude']) + ");\n\
                marker = new google.maps.Marker({position: position,\n\
                                          map: map,\n\
                                         title:'" + str(entry['timestamp']) + "',\n\
                                         icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'});\n\
                bounds.extend(position)\n"
                markers = markers + response_section

            # Populate local arrys with other vehicle data
            xaxis_labels.append(str(entry['timestamp']))
            if 'throttle' in entry['vehicle_data']:
                if entry['vehicle_data']['throttle'] is not None:
                    throttle_positions.append(entry['vehicle_data']['throttle'])
                else:
                    throttle_positions.append(0)

            if 'direction' in entry['vehicle_data']:
                if entry['vehicle_data']['direction'] is not None:
                    direction_positions.append(entry['vehicle_data']['direction'])
                else:
                    direction_positions.append(0)



        # Generate graphs
        if len(throttle_positions) > 0:
            throttle_graph = _createChart(throttle_positions, xaxis_labels)
            throttle_graph = "<br>\n<br>\n<figure>" + throttle_graph + "\n<br></figure>"
        else:
            throttle_graph = ""

        if len(direction_positions) > 0:
            direction_graph = _createChart(direction_positions, xaxis_labels)




        # Section closures
        polygon_cords = polygon_cords + "];\n"
        markers = markers + "map.fitBounds(bounds);"

        # Build response
        response = html_head_start + polygon_cords + markers + html_head_end + html_body_start + throttle_graph + html_body_end
        return(200, str(response))

    except TypeError as e:
        print e
    except NameError as e:
        print e

    except:
        print str(sys.exc_info()[0])
        return(500, "Error: Failed to generate response ")




def _createChart(data, labels):
    throttle_line_chart = pygal.Line(width=700, height=400, show_legend=False, style=LightStyle, x_label_rotation=20, label_font_size=12)
    throttle_line_chart.title = "Throttle %age"
    throttle_line_chart.x_labels = labels
    throttle_line_chart.add('', data)
    raw_graph = throttle_line_chart.render()    
    return raw_graph


def getPlatforms(query=None, handler=None):
    # Get collection list from current DB
    collection_list = _mongo_db.collection_names(include_system_collections=False)

    # HTML Header
    html_header = "<html>\n\
    <head>\n\
        <meta http-equiv=\"refresh\" content=\"20\">\n\
        <meta http-equiv=\"X-UA-Compatible\" content=\"chrome=1\">\n\
    </head>\n\
    <body>\n"

    # HTML Footer
    html_footer = "</body>\n</html>"

    # Add to each returned collection
    link_prefix = "http://" + str(handler.headers['Host']) + "/action/getmap?vehicle_id="

    html_body = "Display all data recorded within the last 24hrs:<br>\n<br>\n"
    for collection in collection_list:
        html_body = html_body + "<a href=" + link_prefix + str(collection) + ">" + str(collection) + "</a><br>\n"

    response = html_header + html_body + html_footer

    return(200, response)



def _mongoConnect():
    try:
        mongo_client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        mongo_db = mongo_client[MONGO_DB]
        return(mongo_client, mongo_db)

    except:
        assert False, "Error: Unknown error occurred while connecting to MongoDB"

_mongo_client, _mongo_db = _mongoConnect()
