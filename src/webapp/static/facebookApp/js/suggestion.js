// ISO 3166-1 country names and codes from http://opencountrycodes.appspot.com/javascript
country_name= "Afghanistan Aland Islands Albania Algeria American Samoa Andorra Angola Anguilla Antarctica Antigua and Barbuda Argentina Armenia Aruba Australia Austria Azerbaijan Bahamas Bahrain Bangladesh Barbados Belarus Belgium Belize Benin Bermuda Bhutan Bolivia, Plurinational State of Bonaire, Sint Eustatius and Saba Bosnia and Herzegovina Botswana Bouvet Island Brazil British Indian Ocean Territory Brunei Darussalam Bulgaria Burkina Faso Burundi Cambodia Cameroon Canada Cape Verde Cayman Islands Central African Republic Chad Chile China Christmas Island Cocos (Keeling) Islands Colombia Comoros Congo Congo, The Democratic Republic of the Cook Islands Costa Rica Cote D'ivoire Croatia Cuba Curacao Cyprus Czech Republic Denmark Djibouti Dominica Dominican Republic Ecuador Egypt El Salvador Equatorial Guinea Eritrea Estonia Ethiopia Falkland Islands (Malvinas) Faroe Islands Fiji Finland France French Guiana French Polynesia French Southern Territories Gabon Gambia Georgia Germany Ghana Gibraltar Greece Greenland Grenada Guadeloupe Guam Guatemala Guernsey Guinea Guinea-Bissau Guyana Haiti Heard Island and McDonald Islands Holy See (Vatican City State) Honduras Hong Kong Hungary Iceland India Indonesia Iran, Islamic Republic of Iraq Ireland Isle of Man Israel Italy Jamaica Japan Jersey Jordan Kazakhstan Kenya Kiribati Korea, Democratic People's Republic of Korea, Republic of Kuwait Kyrgyzstan Lao People's Democratic Republic Latvia Lebanon Lesotho Liberia Libyan Arab Jamahiriya Liechtenstein Lithuania Luxembourg Macao Macedonia, The Former Yugoslav Republic of Madagascar Malawi Malaysia Maldives Mali Malta Marshall Islands Martinique Mauritania Mauritius Mayotte Mexico Micronesia, Federated States of Moldova, Republic of Monaco Mongolia Montenegro Montserrat Morocco Mozambique Myanmar Namibia Nauru Nepal Netherlands New Caledonia New Zealand Nicaragua Niger Nigeria Niue Norfolk Island Northern Mariana Islands Norway Oman Pakistan Palau Palestinian Territory, Occupied Panama Papua New Guinea Paraguay Peru Philippines Pitcairn Poland Portugal Puerto Rico Qatar Reunion Romania Russian Federation Rwanda Saint Barthelemy Saint Helena, Ascension and Tristan Da Cunha Saint Kitts and Nevis Saint Lucia Saint Martin (French Part) Saint Pierre and Miquelon Saint Vincent and the Grenadines Samoa San Marino Sao Tome and Principe Saudi Arabia Senegal Serbia Seychelles Sierra Leone Singapore Sint Maarten (Dutch Part) Slovakia Slovenia Solomon Islands Somalia South Africa South Georgia and the South Sandwich Islands Spain Sri Lanka Sudan Suriname Svalbard and Jan Mayen Swaziland Sweden Switzerland Syrian Arab Republic Taiwan, Province of China Tajikistan Tanzania, United Republic of Thailand Timor-Leste Togo Tokelau Tonga Trinidad and Tobago Tunisia Turkey Turkmenistan Turks and Caicos Islands Tuvalu Uganda Ukraine United Arab Emirates United Kingdom United States United States Minor Outlying Islands Uruguay Uzbekistan Vanuatu Venezuela, Bolivarian Republic of Viet Nam Virgin Islands, British Virgin Islands, U.S. Wallis and Futuna Western Sahara Yemen Zambia Zimbabwe"
countries = [{code: "AF", name: "Afghanistan"},{code: "AX", name: "Aland Islands"},{code: "AL", name: "Albania"},{code: "DZ", name: "Algeria"},{code: "AS", name: "American Samoa"},{code: "AD", name: "Andorra"},{code: "AO", name: "Angola"},{code: "AI", name: "Anguilla"},{code: "AQ", name: "Antarctica"},{code: "AG", name: "Antigua and Barbuda"},{code: "AR", name: "Argentina"},{code: "AM", name: "Armenia"},{code: "AW", name: "Aruba"},{code: "AU", name: "Australia"},{code: "AT", name: "Austria"},{code: "AZ", name: "Azerbaijan"},{code: "BS", name: "Bahamas"},{code: "BH", name: "Bahrain"},{code: "BD", name: "Bangladesh"},{code: "BB", name: "Barbados"},{code: "BY", name: "Belarus"},{code: "BE", name: "Belgium"},{code: "BZ", name: "Belize"},{code: "BJ", name: "Benin"},{code: "BM", name: "Bermuda"},{code: "BT", name: "Bhutan"},{code: "BO", name: "Bolivia, Plurinational State of"},{code: "BQ", name: "Bonaire, Sint Eustatius and Saba"},{code: "BA", name: "Bosnia and Herzegovina"},{code: "BW", name: "Botswana"},{code: "BV", name: "Bouvet Island"},{code: "BR", name: "Brazil"},{code: "IO", name: "British Indian Ocean Territory"},{code: "BN", name: "Brunei Darussalam"},{code: "BG", name: "Bulgaria"},{code: "BF", name: "Burkina Faso"},{code: "BI", name: "Burundi"},{code: "KH", name: "Cambodia"},{code: "CM", name: "Cameroon"},{code: "CA", name: "Canada"},{code: "CV", name: "Cape Verde"},{code: "KY", name: "Cayman Islands"},{code: "CF", name: "Central African Republic"},{code: "TD", name: "Chad"},{code: "CL", name: "Chile"},{code: "CN", name: "China"},{code: "CX", name: "Christmas Island"},{code: "CC", name: "Cocos (Keeling) Islands"},{code: "CO", name: "Colombia"},{code: "KM", name: "Comoros"},{code: "CG", name: "Congo"},{code: "CD", name: "Congo, The Democratic Republic of the"},{code: "CK", name: "Cook Islands"},{code: "CR", name: "Costa Rica"},{code: "CI", name: "Cote D'ivoire"},{code: "HR", name: "Croatia"},{code: "CU", name: "Cuba"},{code: "CW", name: "Curacao"},{code: "CY", name: "Cyprus"},{code: "CZ", name: "Czech Republic"},{code: "DK", name: "Denmark"},{code: "DJ", name: "Djibouti"},{code: "DM", name: "Dominica"},{code: "DO", name: "Dominican Republic"},{code: "EC", name: "Ecuador"},{code: "EG", name: "Egypt"},{code: "SV", name: "El Salvador"},{code: "GQ", name: "Equatorial Guinea"},{code: "ER", name: "Eritrea"},{code: "EE", name: "Estonia"},{code: "ET", name: "Ethiopia"},{code: "FK", name: "Falkland Islands (Malvinas)"},{code: "FO", name: "Faroe Islands"},{code: "FJ", name: "Fiji"},{code: "FI", name: "Finland"},{code: "FR", name: "France"},{code: "GF", name: "French Guiana"},{code: "PF", name: "French Polynesia"},{code: "TF", name: "French Southern Territories"},{code: "GA", name: "Gabon"},{code: "GM", name: "Gambia"},{code: "GE", name: "Georgia"},{code: "DE", name: "Germany"},{code: "GH", name: "Ghana"},{code: "GI", name: "Gibraltar"},{code: "GR", name: "Greece"},{code: "GL", name: "Greenland"},{code: "GD", name: "Grenada"},{code: "GP", name: "Guadeloupe"},{code: "GU", name: "Guam"},{code: "GT", name: "Guatemala"},{code: "GG", name: "Guernsey"},{code: "GN", name: "Guinea"},{code: "GW", name: "Guinea-Bissau"},{code: "GY", name: "Guyana"},{code: "HT", name: "Haiti"},{code: "HM", name: "Heard Island and McDonald Islands"},{code: "VA", name: "Holy See (Vatican City State)"},{code: "HN", name: "Honduras"},{code: "HK", name: "Hong Kong"},{code: "HU", name: "Hungary"},{code: "IS", name: "Iceland"},{code: "IN", name: "India"},{code: "ID", name: "Indonesia"},{code: "IR", name: "Iran, Islamic Republic of"},{code: "IQ", name: "Iraq"},{code: "IE", name: "Ireland"},{code: "IM", name: "Isle of Man"},{code: "IL", name: "Israel"},{code: "IT", name: "Italy"},{code: "JM", name: "Jamaica"},{code: "JP", name: "Japan"},{code: "JE", name: "Jersey"},{code: "JO", name: "Jordan"},{code: "KZ", name: "Kazakhstan"},{code: "KE", name: "Kenya"},{code: "KI", name: "Kiribati"},{code: "KP", name: "Korea, Democratic People's Republic of"},{code: "KR", name: "Korea, Republic of"},{code: "KW", name: "Kuwait"},{code: "KG", name: "Kyrgyzstan"},{code: "LA", name: "Lao People's Democratic Republic"},{code: "LV", name: "Latvia"},{code: "LB", name: "Lebanon"},{code: "LS", name: "Lesotho"},{code: "LR", name: "Liberia"},{code: "LY", name: "Libyan Arab Jamahiriya"},{code: "LI", name: "Liechtenstein"},{code: "LT", name: "Lithuania"},{code: "LU", name: "Luxembourg"},{code: "MO", name: "Macao"},{code: "MK", name: "Macedonia, The Former Yugoslav Republic of"},{code: "MG", name: "Madagascar"},{code: "MW", name: "Malawi"},{code: "MY", name: "Malaysia"},{code: "MV", name: "Maldives"},{code: "ML", name: "Mali"},{code: "MT", name: "Malta"},{code: "MH", name: "Marshall Islands"},{code: "MQ", name: "Martinique"},{code: "MR", name: "Mauritania"},{code: "MU", name: "Mauritius"},{code: "YT", name: "Mayotte"},{code: "MX", name: "Mexico"},{code: "FM", name: "Micronesia, Federated States of"},{code: "MD", name: "Moldova, Republic of"},{code: "MC", name: "Monaco"},{code: "MN", name: "Mongolia"},{code: "ME", name: "Montenegro"},{code: "MS", name: "Montserrat"},{code: "MA", name: "Morocco"},{code: "MZ", name: "Mozambique"},{code: "MM", name: "Myanmar"},{code: "NA", name: "Namibia"},{code: "NR", name: "Nauru"},{code: "NP", name: "Nepal"},{code: "NL", name: "Netherlands"},{code: "NC", name: "New Caledonia"},{code: "NZ", name: "New Zealand"},{code: "NI", name: "Nicaragua"},{code: "NE", name: "Niger"},{code: "NG", name: "Nigeria"},{code: "NU", name: "Niue"},{code: "NF", name: "Norfolk Island"},{code: "MP", name: "Northern Mariana Islands"},{code: "NO", name: "Norway"},{code: "OM", name: "Oman"},{code: "PK", name: "Pakistan"},{code: "PW", name: "Palau"},{code: "PS", name: "Palestinian Territory, Occupied"},{code: "PA", name: "Panama"},{code: "PG", name: "Papua New Guinea"},{code: "PY", name: "Paraguay"},{code: "PE", name: "Peru"},{code: "PH", name: "Philippines"},{code: "PN", name: "Pitcairn"},{code: "PL", name: "Poland"},{code: "PT", name: "Portugal"},{code: "PR", name: "Puerto Rico"},{code: "QA", name: "Qatar"},{code: "RE", name: "Reunion"},{code: "RO", name: "Romania"},{code: "RU", name: "Russian Federation"},{code: "RW", name: "Rwanda"},{code: "BL", name: "Saint Barthelemy"},{code: "SH", name: "Saint Helena, Ascension and Tristan Da Cunha"},{code: "KN", name: "Saint Kitts and Nevis"},{code: "LC", name: "Saint Lucia"},{code: "MF", name: "Saint Martin (French Part)"},{code: "PM", name: "Saint Pierre and Miquelon"},{code: "VC", name: "Saint Vincent and the Grenadines"},{code: "WS", name: "Samoa"},{code: "SM", name: "San Marino"},{code: "ST", name: "Sao Tome and Principe"},{code: "SA", name: "Saudi Arabia"},{code: "SN", name: "Senegal"},{code: "RS", name: "Serbia"},{code: "SC", name: "Seychelles"},{code: "SL", name: "Sierra Leone"},{code: "SG", name: "Singapore"},{code: "SX", name: "Sint Maarten (Dutch Part)"},{code: "SK", name: "Slovakia"},{code: "SI", name: "Slovenia"},{code: "SB", name: "Solomon Islands"},{code: "SO", name: "Somalia"},{code: "ZA", name: "South Africa"},{code: "GS", name: "South Georgia and the South Sandwich Islands"},{code: "ES", name: "Spain"},{code: "LK", name: "Sri Lanka"},{code: "SD", name: "Sudan"},{code: "SR", name: "Suriname"},{code: "SJ", name: "Svalbard and Jan Mayen"},{code: "SZ", name: "Swaziland"},{code: "SE", name: "Sweden"},{code: "CH", name: "Switzerland"},{code: "SY", name: "Syrian Arab Republic"},{code: "TW", name: "Taiwan, Province of China"},{code: "TJ", name: "Tajikistan"},{code: "TZ", name: "Tanzania, United Republic of"},{code: "TH", name: "Thailand"},{code: "TL", name: "Timor-Leste"},{code: "TG", name: "Togo"},{code: "TK", name: "Tokelau"},{code: "TO", name: "Tonga"},{code: "TT", name: "Trinidad and Tobago"},{code: "TN", name: "Tunisia"},{code: "TR", name: "Turkey"},{code: "TM", name: "Turkmenistan"},{code: "TC", name: "Turks and Caicos Islands"},{code: "TV", name: "Tuvalu"},{code: "UG", name: "Uganda"},{code: "UA", name: "Ukraine"},{code: "AE", name: "United Arab Emirates"},{code: "GB", name: "United Kingdom"},{code: "US", name: "United States"},{code: "UM", name: "United States Minor Outlying Islands"},{code: "UY", name: "Uruguay"},{code: "UZ", name: "Uzbekistan"},{code: "VU", name: "Vanuatu"},{code: "VE", name: "Venezuela, Bolivarian Republic of"},{code: "VN", name: "Viet Nam"},{code: "VG", name: "Virgin Islands, British"},{code: "VI", name: "Virgin Islands, U.S."},{code: "WF", name: "Wallis and Futuna"},{code: "EH", name: "Western Sahara"},{code: "YE", name: "Yemen"},{code: "ZM", name: "Zambia"},{code: "ZW", name: "Zimbabwe"},]
placeReference=null;

scales=[
        {'meters':100,'zoom': 19},
        {'meters':250,'zoom': 18},
        {'meters':500,'zoom': 17},
        {'meters':1000,'zoom': 16},
        {'meters':1750,'zoom': 15},
        {'meters':2500,'zoom': 14},
        {'meters':5000,'zoom': 13},
        {'meters':10000,'zoom': 12},
    ]

function loadCountryNames(format){
    if(format==null)
        format='array'
    else
        format='string'
    
    //~ var data=""
    var data=[]
    $.each(countries,function(index, value){
        if(format=='string')
            data=data+" "+value.name
        else
            data.push(value.name)
    })
    return data;
}
function getCountryCode(name){
    index=jQuery.inArray(name, loadCountryNames() )
    if(index!=-1)
        return countries[index].code;
    else
        return null;
}

function getCountryName(code){
    countryName=null;
    $.each(countries,function(index, value){
        
        if(value.code==code)
            countryName=value.name
    })
    return countryName;
}




$(document).ready(function() {
    
    //Set characters counter OnKeyUp
    setRemainingCharCounter('#id_name','#counter');
    
    // remove \n
	$('#id_name').bind('keypress',function(e) { if (e.keyCode==13) return false; });
    
     //~ key: 'AIzaSyBWrR-O_l5STwv1EO7U_Y3JNOnVjexf710', // add your key here    
    //Google Maps - Direction Input Autocomplete address
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
    
    //Set resizable canvas
    $('#address-container').resizable({
        maxWidth: 550 ,
        minWidth: 550,
        handles: 'n,s',
        alsoResize: "#map_canvas",
        stop: function(event, ui) {
            resizeIframe()     
        }
    });

    
    //FORM
    //~ setFormBehaviour();
    
    //~ 
    instanceMap();
    
    
    var time=[];
    for(hours=0; hours<24; hours++){
        for(minutes=0; minutes<60; minutes=minutes+30)
            time.push(FormatNumberLength(hours,2)+":"+FormatNumberLength(minutes,2))
    }
    
    $( "#start-hour,#end-hour" ).autocomplete({
        minLength:0,
        source: function(req, add){ req.term = ''; add(time); }
    });
    
    $( "#start-hour,#end-hour" ).focus(function(){ $(this).autocomplete("search"); });
	
});

function instanceMap(){
    //Esta función crea un mapa nuevo
    if((typeof(default_marker_X) != "undefined") && (typeof(default_marker_Y) != "undefined"))
        var latlngStr=[default_marker_X,default_marker_Y]
    else if(typeof eventID == 'undefined' && typeof (searchconfig_google['location']) != undefined){
        var latlngStr = searchconfig_google['location'].split(",",2);
    }
    else
        var latlngStr = eventLocation.split(",",2);
        
    var lat = parseFloat(latlngStr[0]);
    var lng = parseFloat(latlngStr[1]);
    
    loadGMaps(lat,lng,"map_canvas");
}

function loadCityField(region){
    $('#google-city').geo_autocomplete(new google.maps.Geocoder, {
        mapkey: 'ABQIAAAAr-AoA2f89U6keY8jwYAhgRSH1N1fcQdmTcucWBDBdqkgAa1-PhQhWKwe8ygo_Y3tFrHmB0jtJoQ0Bw', 
        selectFirst: false,
        minChars: 3,
        cacheLength: 50,
        width: 340,
        mapwidth:0,
        mapheight:0,
        scroll: true,
        scrollHeight: 150,
        geocoder_region:region,
        geocoder_types: 'locality,sublocality',
    }).result(function(_event, _data) {
        if (_data) 
            map.fitBounds(_data.geometry.viewport);
        //~ console.log(_data)
    });
}

function loadGoogleSettings(){
    
    $("input[name='place-type']:checked").removeAttr('checked')
    if(searchconfig_google['type']=='establishment')
        $($("input[name='place-type']")[0]).attr("checked","checked");
    else if(searchconfig_google['type']=='geocode')
        $($("input[name='place-type']")[1]).attr("checked","checked");
    else
        $($("input[name='place-type']")[2]).attr("checked","checked");
    
    $("input[name='place-type']").change()
    
    //LOAD AND INITIALIZE COUNTRY OPTIONS
    //~ var countryOptions="";
    //~ $.each(countries,function(index, item){
        //~ countryOptions=countryOptions+'<option value="'+item.code+'">'+item.name+'</option>';
    //~ })
    //~ $('#google-region').append(countryOptions)
    //~ $('#google-region').val(searchconfig_google['region_code'])
    
    
    //LOAD CITY NAME USING LAT,LON on #google-city input field
    var input = searchconfig_google['location'];
    var latlngStr = input.split(",",2);
    var lat = parseFloat(latlngStr[0]);
    var lng = parseFloat(latlngStr[1]);
    var latlng = new google.maps.LatLng(lat, lng);
    geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {

            $.each(results,function(key,value){
                if(jQuery.inArray('locality', value.types )!=-1)
                    $('#google-city').val(value.formatted_address)
            });
            
        } else {
            alert(gettext("Geocoder failed due to: ") + status);
        }
    });
    
    //Acción al cambiar el nombre de la ciudad
    $('#google-city').change(function(){
        
        //Sobreescribimos la variable global location para que para las
        //nuevas búsquedas use ese valor
        centerMap();
        
    })
    
    //LOAD THE AUTOCOMPLETE CITY FIELD
    loadCityField($(this).val())
    
    $("#radius").change(function(){
        searchconfig_google['radius']=$(this).val();
        resetMapZoom();
    });
    //RELOAD IT WHE THE COUNTRY CHANGES
    //~ $("#google-region").change(function(){
        //~ loadCityField($(this).val())
    //~ })
}

function saveSettings(engine){
    if(engine=='google-places'){
        $('#savingSettings').text("Guardando...")
        //Primero buscamos la latitud y longitud de la ciudad
        geocoder.geocode( 
            {
                'address':$('#google-city').val(),
                'region':searchconfig_google['region_code']
            }, 
            function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    
                    //Si todo va correcto enviamos los datos al servidor
                    var latlong=results[0].geometry.location.Ja+','+results[0].geometry.location.Ka;
                    $.ajax({
                        async: false,
                        type: 'POST',
                        url: '/ajax/searchconfgoogle/',
                        data: {
                            'type': $('input[name="place-type"]:checked').val(),
                            'radius': Number($('#radius').val()),
                            'location': latlong,
                            //~ 'region_code': searchconfig_google['region_code']
                        },
                        complete: function(msg){
                            if (msg.status !=200){
                                $('#answerMessage').removeClass('success');
                                $('#answerMessage').addClass('error');
                                $('#answerMessage').text(gettext("Ha habido un error al añadir la sugerencia, estamos trabajando para solucionarlo.")).fadeIn('slow').delay(2000).fadeOut('slow');
                            }else{
                                $('#answerMessage').removeClass('error');
                                $('#answerMessage').text(gettext("La sugerencia ha sido añadida con éxito")).fadeIn('slow').delay(2000).fadeOut('slow');
                                $('#answerMessage').addClass('success');
                                
                                //Sobreescribimos los valores anteriores para que cuando volvamos
                                //a desplegar la configuración salga bien
                                searchconfig_google['location']=latlong
                                searchconfig_google['type']=$('input[name="place-type"]:checked').val();
                                searchconfig_google['radius']=$('#radius').val();
                                
                                //Minimizamos el menu de configuración
                                showSettings()
                                
                            }
                            $('#savingSettings').text("Guardar")
                        }
                    });//End AJAX
                } else {
                    alert(gettext("Geocode was not successful for the following reason: ") + status);
                }
            }
        );
        
        
        
    }
    
    
}

function centerMap(address,region) {
    var data={};
    
    data['address']=$('#google-city').val();
    data['region']=searchconfig_google['region_code'];

    geocoder.geocode( 
        data, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var LatLon=results[0].geometry.location.Ja+','+results[0].geometry.location.Ka;
                var value={'Latlon':LatLon, 'result':results[0]}
                //~ console.log(value)
                map.fitBounds(results[0].geometry.viewport);

            } else {
                alert("Geocode was not successful for the following reason: " + status);
                
            }
        }
    );
}




function loadGMaps(defaultX,defaultY,canvas) {
    
    if( (typeof(default_marker_X) != "undefined") && (typeof(default_marker_Y) != "undefined") ){
        //Se ha entrado desde añadir una sugerencia a un sitio (vista sitio)
        defaultX=default_marker_X
        defaultY=default_marker_Y
    }else{
    
        if(defaultX==null || defaultX==0)
            defaultX=37.176
        if(defaultY==null || defaultY==0)
            defaultY=-3.597
    }    
    
    var meters=searchconfig_google['radius']
    var zoom=11;
    $.each(scales,function(index,value){
        if(meters<value.meters){
            zoom=value.zoom;
            return false;
        }
    });
    //~ if(canvas==null)
        //~ canvas="map_canvas"
    
    var myOptions = {
        zoom: zoom,
        center: new google.maps.LatLng(defaultX,defaultY),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControlOptions: { //Tipo: Mapa //Satelite
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        scaleControl: true,
        scrollwheel:false,
        zoomControl: true,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.LARGE
        }
    }
    map = new google.maps.Map(document.getElementById(canvas), myOptions);
    geocoder = new google.maps.Geocoder();
    insertToolbar(map)
    
    // DEFAULT MARKER
    if( (typeof(default_marker_X) != "undefined") && (typeof(default_marker_Y) != "undefined") ){
        var spaceLocation = new google.maps.LatLng(default_marker_X, default_marker_Y);

        if (typeof(GRM.marker) == "undefined"){
            GRM['marker'] = createMarker(default_marker_X, default_marker_Y);
        }
        else{
            GRM.marker.setPosition(spaceLocation);
        }
    }
    
    placesAutocomplete();
}

function createMarker(x,y)
{
    var icon = new google.maps.MarkerImage("/static/webapp/img/marcador02.png"); // or /static/webapp/img/marcador03.png
    var myLatlng = new google.maps.LatLng(x,y);
    
    var marker = new google.maps.Marker({
        map: map,
        draggable: false,
        position: myLatlng,
        icon: icon
    });
    marker.setVisible(true);
    marker.setDraggable(true);
    marker.setAnimation(google.maps.Animation.DROP);
    // set marker events
    google.maps.event.addListener(marker, 'dragend', function(){updateAddressByMarker(this);});
    
    return marker;
}

function codeLatLng(input) {
    var latlngStr = input.split(",",2);
    var lat = parseFloat(latlngStr[0]);
    var lng = parseFloat(latlngStr[1]);
    var latlng = new google.maps.LatLng(lat, lng);
    geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (results[1]) {
                map.setZoom(11);
                marker = new google.maps.Marker({
                position: latlng,
                map: map
            });
                infowindow.setContent(results[1].formatted_address);
                infowindow.open(map, marker);
            }
        } else {
            alert("Geocoder failed due to: " + status);
        }
    });
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
    $(mirilla).attr('title',gettext('Posición actual'));
    $(mirilla).html('<img src="/static/webapp/img/mirilla.png">');
    
    //Asignamos el comportamiento
    google.maps.event.addDomListener(mirilla, 'click', function() {   
        centerOnMyLocation()
    });
    
    //Creamos el boton del pollo
    //------------------------------------------------------------------
    //~ var btnPollo = document.createElement('DIV');
    //~ $(btnPollo).addClass("btnGmaps")
    //~ $(btnPollo).attr('title','Get the marker');
    //~ $(btnPollo).html('<img src="/static/webapp/img/marcador03.png">');
    
    //Creamos el contenedor del marcador
    //~ var marker;
    
    //Asignamos el comportamiento
    //~ google.maps.event.addDomListener(btnPollo, 'click', function() {   
        //~ var pos = map.getCenter();   
        //~ var myLatlng = new google.maps.LatLng(pos.lat(),pos.lng());
        //~ 
        //~ if(marker==undefined){
            //~ //En caso de que no se haya inicializado nunca creamos un
            //~ //nuevo marcador
            //~ marker = new google.maps.Marker({
                //~ map: map,
                //~ draggable: false,
                //~ position: myLatlng,
                //~ icon: new google.maps.MarkerImage("/static/webapp/img/marcador02.png")
            //~ });
            //~ google.maps.event.addListener(marker, 'dragend', function(){updateAddressByMarker(this);});
        //~ }else{
            //~ //Sino tan solo actualizamos la posición
            //~ marker.setPosition(myLatlng);
        //~ }
            
        //Centramos el marcador
        //~ marker.setIcon(new google.maps.MarkerImage("/static/webapp/img/marcador03.png"));
        //~ marker.setAnimation(google.maps.Animation.DROP);
        //~ marker.setDraggable(true);
        //~ marker.setFlat(false);
    //~ });
    

    //Creamos el contenedor del toolbar
    var toolbar = document.createElement('DIV');
    $(toolbar).css('padding', '5px');
    //Le añadimos los botones
    //$(toolbar).append(btnPollo);
    $(toolbar).append(mirilla);
    //Los metemos en el mapa
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(toolbar);
}

function updateAddressByMarker(marker){
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

function saveSuggestion(){
    
    
        if($('#suggestion-item textarea').val()==$('#suggestion-item textarea').attr('placeholder')){
            showMessage(gettext('Por favor introduce primero la sugerencia'),"error");
            $('#suggestion-item textarea').focus()
            return false;
        }
        
        if(placeReference==null){
            showMessage(gettext('Por favor indique el campo "¿Donde?" para continuar'),"error");
            $('#place').focus()
            return false;
        }
        
        if($('#date [type="checkbox"]').is(':checked')==false){
            if($('#start-date').val()!="mm/dd/aa" && $('#end-date').val()!="mm/dd/aa"){
                //Hacemos las comparaciones cuando están la fecha de inicio y la de fin
                var startDate = new Date($('#start-date').val());
                var endDate = new Date($('#end-date').val());
                
                if (startDate > endDate){
                    //Comprobamos que inicio < fin
                    showMessage(gettext('Por favor revise que la fecha de inicio sea anterior a la de fin'),"error");
                    return false;
                }else if(startDate == endDate && $('#start-hour').val() !="hh:mm" && $('#end-hour').val() !="hh:mm"){
                    //Comprobamos que si inicio < fin -> hora inicio < hora fin
                    var startHour=$('#start-hour').val().split(":");
                    var endHour=$('#end-hour').val().split(":");
                    if(startHour[0]>endHour[0]){
                        showMessage(gettext('Por favor revise que la hora de inicio sea anterior a la de fin'),"error");
                        return false;
                    }else if(startHour[0]==endHour[0]){
                        if(startHour[1]>endHour[1]){
                            showMessage(gettext('Por favor revise que la hora de inicio sea anterior a la de fin'),"error");
                            return false;
                        }
                    }
                }
            }
        }
        
        
        $('#submit-button').text(gettext("Enviando..."))
        $('#submit-button').addClass("waiting")
        GRM.wait();
        
        var params = { 
            name: $('#id_name').val(), 
            place_reference: placeReference,
			
			// esto envia el campo vacío si tiene el mismo valor que el placeholder
            description: ($('#id_description').val() == $('#id_description').attr('placeholder'))?'':$('#id_description').val(),
			
            visibility: $('#id_visibility').val(),
            tags: $('#id_tags').val()
        };
        if($('#date [type="checkbox"]').is(':checked')==false){
            //console.log("Entro por el checkbox no marcado");
            tmp=$('#date [type="checkbox"]');
            splittedDate=$('#start-date').val().split("/")
            params['starts_month']=splittedDate[0]
            params['starts_day']=splittedDate[1]
            params['starts_year']=splittedDate[2]
            params['starts_hour']=$('#start-hour').val()
            splittedDate=$('#end-date').val().split("/")
            params['ends_month']=splittedDate[0]
            params['ends_day']=splittedDate[1]
            params['ends_year']=splittedDate[2]
            params['ends_hour']=$('#end-hour').val()
        }
        if($('#visibility span[value="public"]').css('display')!="none")
            params['visibility']= "public";
        else
            params['visibility']= "private";
        
        if( $('#lists span.checked').length > 0 ){
            params['list_id']="";
            $('#lists span.checked').each(function(i,elem){
                params['list_id']=$(elem).attr('value')+','+params['list_id'];
            });
        }
        var shareThrough=$('#social-share ul li:not(.inactive)');
        if(shareThrough.length > 0){
            $(shareThrough).each(function(i,elem){
                params['to_'+$(elem).attr("data-network")]=true;
            });
        }
        
        //Si estamos editando una sugerencia añadimos el ID.
        if(typeof eventID != 'undefined')
            params['eventid']=eventID;
        
        $.ajax({
            type: "POST",
            url: "/ajax/add/suggestion/",
            data: jQuery.param(params),
            complete: function(msg){
                GRM.nowait();
                if (msg.status !=200){
                    showMessage(gettext("Error")+" "+msg.status,"error")
                }else{
                    showMessage(gettext("La sugerencia ha sido añadida con éxito"),"success")

                    
                    //Restablecemos los campos
                    $('#id_name').val("").blur();
                    $('#id_description').val("");
                    $('#id_tags').val("");
                    $('#place').val("").blur();
                    //~ $('#start-date').val("mm/dd/aa");
                    //~ $('#start-hour').val("").blur();
                    //~ $('#end-date').val("mm/dd/aa");
                    //~ $('#end-hour').val("").blur();
                    $('#lists span.checked').each(function(i,elem){
                        $(elem).removeClass('checked');
                    })
                    
                    //Reseteamos el mapa
                    instanceMap();
                }
                $('#submit-button').text(gettext("Enviar"))
                $('#submit-button').removeClass("waiting")
            }
        });
        
        return false;
    
}
function showSettings(){
    loadGoogleSettings()
    
    //Primero cerramos cualquier settings abierto
    $("input[name='engine']").each(function(){
        engine=$(this).val()
        if(engine!=$("input[name='engine']:checked").val())
            if($('#'+engine+'-settings').css('display')=='block')
                $('#'+engine+'-settings').fadeOut('slow')
    })
    
    //Luego cambiamos el estado del pulsado
    var engine=$("input[name='engine']:checked").val()
    //$('#'+engine+'-settings').fadeToggle('slow')
    
    $('#'+engine+'-settings').toggle('slow',function(){
        resizeIframe();
        }
    );
    
}

//Asociamos al elemento #place el autocompletar
function placesAutocomplete(){
    
    var input = document.getElementById('place');
    
    //Cargamos nuestras opciones de búsqueda
    var options = {
        region: searchconfig_google['region_code'] 
    }
    
    if(searchconfig_google['type']!='all')
      options['types']=[ searchconfig_google['type'] ];

    //Fin cargamos opciones
    autocomplete = new google.maps.places.Autocomplete(input,options);
    autocomplete.bindTo('bounds', map);

    var infowindow = new google.maps.InfoWindow();
    var marker = new google.maps.Marker({
        map: map
    });
    //Añadimos un listener al campo
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        infowindow.close();
        var place = autocomplete.getPlace();
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17);  // Why 17? Because it looks good.
        }
        
        placeReference=place.reference;

        var image = new google.maps.MarkerImage(
            '/static/webapp/img/marcador03.png',
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
        
        marker.setIcon(image);
        marker.setPosition(place.geometry.location);
        
        //~ console.log(marker)

        infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
        infowindow.open(map, marker);
    });

    // Sets a listener on a radio button to change the filter type on Places
    // Autocomplete.
    /*
    function setupClickListener(id, types) {
        var radioButton = document.getElementById(id);
        google.maps.event.addDomListener(radioButton, 'click', function() {
            autocomplete.setTypes(types);
        });
    }

    setupClickListener('changetype-all', []);
    setupClickListener('changetype-establishment', ['establishment']);
    setupClickListener('changetype-geocode', ['geocode']);*/
}

function getEventPlace(){
    var latlngStr = eventLocation.split(",",2);
    var pyrmont = new google.maps.LatLng(latlngStr[0],latlngStr[1]);

    var request = {
        reference:poi_reference,
        location: pyrmont,
        radius: '50',
        //~ types: ['store']
    };
    
    service = new google.maps.places.PlacesService(map);
    service.search(request, function callback(results, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
            for (var i = 0; i < results.length; i++) {
                var place = results[i];
                //~ createMarker(results[i]); 
                if(results[i].reference==poi_reference)
                    console.log(results[i])
            }
        }
    });
}

function resetMapZoom(val){
    var meters=searchconfig_google['radius']
    var zoom=11;
    if(val){
        meters=val;
        //~ console.log('Meter='+val);
    }

    $.each(scales,function(index,value){
        if(meters<value.meters){
            //~ console.log('Zoom='+)
            zoom=value.zoom;
            map.setZoom(value.zoom);
            return false;
        }
    });
    return zoom;
    
}

function showMoreDetails(){
    $('#more-details').toggle('fast',function(){
            resizeIframe()
        }
    )
    
}
/*
 * Baul de sugerencias
 */

