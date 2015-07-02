function changeMarkerPosition(id, marker) {
    var positions = {};
    var data = {};
    positions["po08m3u5"] = [51.448298, -2.146085];
    data["po08m3u5"] = "unitID: po08m3u5";
    positions["fy776wj0"] = [51.449501, -2.146074];
    data["fy776wj0"] = "unitID: fy776wj0";
    positions["d166ce06"] = [51.448298, -2.146085];
    data["d166ce06"] = "unitID: d166ce06";

    for (var key in positions) {
       if (id == key) {
          var lat = positions[key][0];
          var long = positions[key][1];
          var latlng = new google.maps.LatLng(lat, long);
          marker.setPosition(latlng);
          bounds.extend(latlng);

          for (var datakey in data) {
              if (id == datakey) {
                  var infowindow = new google.maps.InfoWindow({ content: data[datakey] });
                  google.maps.event.clearInstanceListeners(marker);
                  google.maps.event.addListener(marker, 'click', function() {infowindow.open(map, marker);});
              }
          }
       }
    }
    map.fitBounds(bounds);
    map.setZoom(16);

}
