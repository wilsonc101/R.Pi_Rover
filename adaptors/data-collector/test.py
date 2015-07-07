html_header = "<!DOCTYPE html>\n\
<html>\n\
  <head>\n\
    <meta name=\"viewport\" content=\"initial-scale=1.0, user-scalable=no\">\n\
    <meta charset=\"utf-8\">\n\
    <title>Simple Polylines</title>\n\
    <style>\n\
      html, body, #map-canvas {\n\
        height: 100%;\n\
        margin: 0px;\n\
        padding: 0px\n\
      }\n\
    </style>\n\
    <script src=\"https://maps.googleapis.com/maps/api/js?v=3.exp&signed_in=true\"></script>\n\
    <script>\n\
	function initialize() {\n\
  var mapOptions = {\n\
    zoom: 12,\n\
    center: new google.maps.LatLng(0, 0),\n\
    mapTypeId: google.maps.MapTypeId.TERRAIN\n\
  };\n\
  var map = new google.maps.Map(document.getElementById('map-canvas'),\n\
      mapOptions);\n\
  var flightPlanCoordinates = ["



print html_header
