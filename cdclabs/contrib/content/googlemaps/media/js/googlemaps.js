$(document).ready(function initialize() {
    var geocoder;
    var map;
    var marker;
    var address = "{{ object.address }}, {{ object.zipcode }} {{ object.city }}";
    var latlng;
    var infowindow = new google.maps.InfoWindow();

    {% if object.get_lat_lng %}
    latlng = new google.maps.LatLng({{ object.lat }}, {{ object.lng }});
    {% else %}
    geocoder = new google.maps.Geocoder();
    if(geocoder) {
	geocoder.geocode({'address': address}, function(results, status) {
	    if (status == google.maps.GeocoderStatus.OK) {
			map.setCenter(results[0].geometry.location);
			var marker = new google.maps.Marker({
				map: map,
				position: results[0].geometry.location
			});
			{% if object.title %}
			infowindow.setContent('{{ object.title }} <br> {{ object.address }}');
            infowindow.open(map, marker);
            {% endif %}
	    } else {
		alert("Geocode was not successful for the following reason: " + status);
	    }
	});
    }
    {% endif %}


    var options = {
		zoom : {{ object.zoom }},

		streetViewControl: false,
		navigationControl: true,
		navigationControlOptions: {
			style: google.maps.NavigationControlStyle.SMALL,
		},
		mapTypeControl: true,
		mapTypeControlOptions: {
			style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
		},
		mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("google-map-{{ object.id }}"), options);
});

