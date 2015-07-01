function changeMarkerPosition(id, marker) {
    var positions = {};
    positions["po08m3u5"] = [51.448806, -2.145816];
    positions["fy776wj0"] = [51.449147, -2.1466];
    positions["d166ce06"] = [51.448806, -2.145816];

    for (var key in positions) {
       if (id == key) {
          var lat = positions[key][0];
          var long = positions[key][1];
          var latlng = new google.maps.LatLng(lat, long);
          marker.setPosition(latlng);
          map.setCenter(latlng);
       }
    }
}
