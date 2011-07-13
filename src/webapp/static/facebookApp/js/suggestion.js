$(document).ready(function() {
    
    //Set characters counter OnKeyUp
    setRemainingCharCounter();
    
    //Inicialize Google Maps
    //Buscamos la ciudad del residencia del usuario
    //~ $.get('http://maps.googleapis.com/maps/api/geocode/json?address=granada,spain&sensor=false', 
        //~ {},
        //~ function(data){
            //~ console.log(data);
        //~ }, "json"
    //~ );
    $('#address').geo_autocomplete(new google.maps.Geocoder, {
		mapkey: 'ABQIAAAAbnvDoAoYOSW2iqoXiGTpYBTIx7cuHpcaq3fYV4NM0BaZl8OxDxS9pQpgJkMv0RxjVl6cDGhDNERjaQ', 
		selectFirst: false,
		minChars: 3,
		cacheLength: 50,
		width: 300,
		scroll: true,
		scrollHeight: 330
	}).result(function(_event, _data) {
		if (_data) map.fitBounds(_data.geometry.viewport);
	});
    
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
        //mapTypeId: 'satellite'
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
