function addMarker() {
    var markers = {};
    //po08m3u5
    var position = new google.maps.LatLng(51.448298,-2.146085);
    bounds.extend(position);
    marker0 = new google.maps.Marker({position: position,
                                     map: map,
                                     title: 'po08m3u5',
                                     icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'});

    markers["po08m3u5"] = marker0;

    //fy776wj0
    var position = new google.maps.LatLng(51.448659,-2.14646);
    bounds.extend(position);
    marker1 = new google.maps.Marker({position: position,
                                     map: map,
                                     title: 'fy776wj0',
                                     icon: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'});

    markers["fy776wj0"] = marker1;

    map.fitBounds(bounds);
    map.setZoom(16);

    //d166ce06
    var position = new google.maps.LatLng(51.448806,-2.145816);
    bounds.extend(position);
    marker2 = new google.maps.Marker({position: position,
                                     map: map,
                                     title: 'd166ce06',
                                     icon: 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png'});

    markers["d166ce06"] = marker2;

    return markers;
}