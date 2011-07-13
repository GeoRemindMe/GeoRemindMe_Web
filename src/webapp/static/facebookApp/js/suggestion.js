$(document).ready(function() {
    
    //Set characters counter OnKeyUp
    setRemainingCharCounter();
    
    
     //~ key: 'AIzaSyBWrR-O_l5STwv1EO7U_Y3JNOnVjexf710', // add your key here
     
     //~ google.maps.places.PlacesServices#search().
 

    
    
    //Input Autocomplete address
    $('#address').geo_autocomplete(new google.maps.Geocoder, {
		mapkey: 'ABQIAAAAr-AoA2f89U6keY8jwYAhgRSH1N1fcQdmTcucWBDBdqkgAa1-PhQhWKwe8ygo_Y3tFrHmB0jtJoQ0Bw', 
		selectFirst: false,
		minChars: 3,
		cacheLength: 50,
		width: 530,
        mapwidth:0,
        mapheight:0,
		scroll: true,
		scrollHeight: 150,
        geocoder_region:'Spain',
        geocoder_types: 'locality,street_address,sublocality,neighborhood,country',
	}).result(function(_event, _data) {
		if (_data) map.fitBounds(_data.geometry.viewport);
	});
    
    
    
    //Inicialize Google Maps
    //Buscamos la ciudad del residencia del usuario
    //~ $.get('http://maps.googleapis.com/maps/api/geocode/json?address=granada,spain&sensor=false', 
        //~ {},
        //~ function(data){
            //~ console.log(data);
        //~ }, "json"
    //~ );
    
    loadGMaps(37.176,-3.597,"map_canvas");
    
    
    
    //Set resizable canvas
        $('#address-container').resizable({
             maxWidth: 550 ,
             minWidth: 550,
             handles: 'n,s',
             alsoResize: "#map_canvas"
        });
    
    
    //FORM
    setFormBehaviour();
});

function setRemainingCharCounter(){
    $('#id_name').keyup(function(){
        $('#counter').text(500-$('#id_name').val().length);
    })
    $('#id_name').trigger('keyup');
}

function loadGMaps(defaultX,defaultY,canvas) {
    
    if(defaultX==null || defaultX==0)
        defaultX=37.176
    if(defaultY==null || defaultY==0)
        defaultY=-3.597
        
    if(canvas==null)
        canvas="map_canvas"
    
    var myOptions = {
        zoom: 17,
        center: new google.maps.LatLng(defaultX,defaultY),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControlOptions: { //Tipo: Mapa //Satelite
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        zoomControl: true,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.LARGE
        }
    }
    map = new google.maps.Map(document.getElementById(canvas), myOptions);
    geocoder = new google.maps.Geocoder();
    
    insertToolbar(map)
    
    placesAutocomplete(map);

}

function centerOnMyLocation(){
    var initialLocation;
    var granada = new google.maps.LatLng(37.176, -3.597);
    var browserSupportFlag =  new Boolean();

    // Try W3C Geolocation (Preferred)
    if(navigator.geolocation) {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position) {
            initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
            map.panTo(initialLocation);
        }, function() {
            handleNoGeolocation(browserSupportFlag);
        });
        
    // Try Google Gears Geolocation
    } else if (google.gears) {
        browserSupportFlag = true;
        var geo = google.gears.factory.create('beta.geolocation');
            geo.getCurrentPosition(function(position) {
                initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
                map.panTo(initialLocation);
        }, function() {
            handleNoGeoLocation(browserSupportFlag);
        });
    
    // Browser doesn't support Geolocation
    } else {
        browserSupportFlag = false;
        handleNoGeolocation(browserSupportFlag);
    }

    function handleNoGeolocation(errorFlag) {
        if (errorFlag == true) {
            alert("Geolocation service failed.");
            initialLocation = granada;
        } else {
            alert("Your browser doesn't support geolocation. We've placed you in Granada.");
            initialLocation = granada;
        }
        map.panTo(initialLocation);
    }
}

function insertToolbar(map){
    
    
    //Creamos el boton de la mirilla
    //------------------------------------------------------------------
    var mirilla = document.createElement('DIV');
    $(mirilla).addClass("btnGmaps")
    $(mirilla).attr('title','My location');
    $(mirilla).html('<img src="/static/webapp/img/mirilla.png">');
    
    //Asignamos el comportamiento
    google.maps.event.addDomListener(mirilla, 'click', function() {   
        centerOnMyLocation()
    });
    
    //Creamos el boton del pollo
    //------------------------------------------------------------------
    var btnPollo = document.createElement('DIV');
    $(btnPollo).addClass("btnGmaps")
    $(btnPollo).attr('title','Get the marker');
    $(btnPollo).html('<img src="/static/webapp/img/marcador03.png">');
    
    //Creamos el contenedor del marcador
    var marker;
    
    //Asignamos el comportamiento
    google.maps.event.addDomListener(btnPollo, 'click', function() {   
        var pos = map.getCenter();   
        var myLatlng = new google.maps.LatLng(pos.lat(),pos.lng());
        
        if(marker==undefined){
            //En caso de que no se haya inicializado nunca creamos un
            //nuevo marcador
            marker = new google.maps.Marker({
                map: map,
                draggable: false,
                position: myLatlng,
                icon: new google.maps.MarkerImage("/static/webapp/img/marcador02.png")
            });
            google.maps.event.addListener(marker, 'dragend', function(){updateAddressByMarker(this);});
        }else{
            //Sino tan solo actualizamos la posición
            marker.setPosition(myLatlng);
        }
            
        //Centramos el marcador
        marker.setIcon(new google.maps.MarkerImage("/static/webapp/img/marcador03.png"));
        marker.setAnimation(google.maps.Animation.DROP);
        marker.setDraggable(true);
        marker.setFlat(false);
    });
    

    //Creamos el contenedor del toolbar
    var toolbar = document.createElement('DIV');
    $(toolbar).css('padding', '5px');
    //Le añadimos los botones
    $(toolbar).append(btnPollo);
    $(toolbar).append(mirilla);
    //Los metemos en el mapa
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(toolbar);
}

function updateAddressByMarker(marker)
{
    geocoder.geocode({'latLng': marker.getPosition()}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results && results[0]) {
          $('#address').val(results[0].formatted_address);
        }
      }
    });
}

function activateTab(tab){
    if(tab=='address'){
        $('#address-form').css('display','block');
        $('#place-form').css('display','none');
        $('#place-tab').removeClass('active');
        $('#address-tab').addClass('active');
    }else{
        $('#address-form').css('display','none');
        $('#place-form').css('display','block');
        $('#place-tab').addClass('active');
        $('#address-tab').removeClass('active');
    }
}

function setFormBehaviour(){
    $("form").submit(function() {
        $('#submit-button').val("Enviado...")
        $('#submit-button').addClass("waiting")
        
        var params = { 
            name: $('#id_name').val(), 
            place_id: $('#id_place_id').val(), 
            description: $('#id_description').val(),
            starts_month: $('#id_starts_month').val(),
            starts_day: $('#id_starts_day').val(),
            starts_year: $('#id_starts_year').val(),
            ends_month: $('#id_ends_month').val(),
            ends_day: $('#id_ends_day').val(),
            ends_year: $('#id_ends_year').val(),
            visibility: $('#id_visibility').val()
        };
        
        $.ajax({
            type: "POST",
            url: "/ajax/add/suggestion/",
            data: jQuery.param(params),
            complete: function(msg){
                if (msg.status !=200){
                    $('#error-msg').text("Error "+msg.status)
                    $('#error-msg').fadeIn('slow').delay(2000).fadeOut('slow')
                }
                $('#submit-button').val("Enviar")
                $('#submit-button').removeClass("waiting")
            }
        });
         
        return false;
    });
}


function placesAutocomplete(map){
    var input = document.getElementById('place');
    var autocomplete = new google.maps.places.Autocomplete(input);

    autocomplete.bindTo('bounds', map);

    var infowindow = new google.maps.InfoWindow();
    var marker = new google.maps.Marker({
        map: map
    });

    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        infowindow.close();
        var place = autocomplete.getPlace();
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);  // Why 17? Because it looks good.
        }

        var image = new google.maps.MarkerImage(
            place.icon,
            new google.maps.Size(71, 71),
            new google.maps.Point(0, 0),
            new google.maps.Point(17, 34),
            new google.maps.Size(35, 35));
            marker.setIcon(image);
            marker.setPosition(place.geometry.location);

            var address = '';
            if (place.address_components) {
                address = [(place.address_components[0] &&
                place.address_components[0].short_name || ''),
                (place.address_components[1] &&
                place.address_components[1].short_name || ''),
                (place.address_components[2] &&
                place.address_components[2].short_name || '')
            ].join(' ');
        }

        infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
        infowindow.open(map, marker);
    });

    // Sets a listener on a radio button to change the filter type on Places
    // Autocomplete.
    function setupClickListener(id, types) {
        var radioButton = document.getElementById(id);
        google.maps.event.addDomListener(radioButton, 'click', function() {
            autocomplete.setTypes(types);
        });
    }

    setupClickListener('changetype-all', []);
    setupClickListener('changetype-establishment', ['establishment']);
    setupClickListener('changetype-geocode', ['geocode']);
}

