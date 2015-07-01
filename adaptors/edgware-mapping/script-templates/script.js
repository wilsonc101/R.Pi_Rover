var map;
var bounds;


var timer = setInterval(function (){
                   
                   // Re-add script
                   var script = document.createElement("script");
                   script.type = "text/javascript";
                   script.src = "update.js";
                   document.getElementsByTagName("head")[0].appendChild(script);}, 4000);

function initialize() {
    bounds = new google.maps.LatLngBounds();
    var mapCanvas = document.getElementById('map-canvas');
    var mapOptions = {
      center: new google.maps.LatLng(0, 0),
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    map = new google.maps.Map(mapCanvas, mapOptions);
    map.fitBounds(bounds);

    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        this.setZoom(16);
        google.maps.event.removeListener(boundsListener);

        // Populate array of initial markers
        var markers = addMarker();
 
        // Update marker positions every 5 seconds 
        var timer = setInterval(function (){
            for (var key in markers){
                changeMarkerPosition(key, markers[key]);
            }                   
          }, 5000);
    });
  }



  google.maps.event.addDomListener(window, 'load', initialize);

