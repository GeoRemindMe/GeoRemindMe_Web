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
    
    
function onLiClick(obj){
    var checkbox=$(obj).find("span.name");
    if($(checkbox).hasClass("checked"))
        $(checkbox).removeClass("checked");
    else
        $(checkbox).addClass("checked");
}

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
    
    //AÃ±adimos el comportamiento
    $('span.btn.dropDownBtn').menuList({
        onLiClick: function(){
            //Buscamos el checkbox y lo marcamos/desmarcamos
            onLiClick(this);
        },
        onNewList: function(listname){
           
            $.ajax({
                type: "POST",
                url: url["modify_suggestion_list"],
                data: {
                    name: listname
                },
                dataType:'json',
                success: function(data){
                    //AÃ±adimos la lista al desplegable
                    $("<li id=\"listid-"+data.id+"\"><span class=\"checkbox name\" value=\""+data.id+"\">"+data.name+"</span> (<span class=\"list-"+data.id+"-counter\">"+data.keys.length+"</span> "+gettext(sugerencias)+"</li>").insertBefore('.new-list-btn');
                    $('#listid-'+data.id).click(function(){onLiClick(this)});
                    $('#listid-'+data.id).click();
                    //AÃ±adimos la lista en la pestaÃ±a listas
                    
                    //Reordenamos alfabÃ©ticamente la lista desplegable
                    $('.submenu li').not('li.new-list-btn').sortElements(function(a, b){
                        return $(a).text().toLowerCase() > $(b).text().toLowerCase() ? 1 : -1;
                    });
                    
                    $("#dropdown-list").removeClass('visible-display');
                }
            });
        }
    });

    
    
    
    
    /*Set date picket behaviour*/
        
        //Set initial values
        var currentTime = new Date()
        var month = FormatNumberLength(currentTime.getMonth() + 1,2)
        var day = FormatNumberLength(currentTime.getDate(),2)
        var year = currentTime.getFullYear()
        var today = month+"/"+day+"/"+year;
        $("#start-date,#end-date").attr('placeholder',today);
        
        //Setting interval from now to next hour (rounded to 0/30min)
        var minutes=currentTime.getMinutes();
        var hours= currentTime.getHours();
        var hoursInt= hours;
        if(minutes>30){
            minutes="00";
            hours=FormatNumberLength(hours+1,2);
            hoursInt=hoursInt+1;
        }else if(minutes<30){
            minutes="30";
        }
        var now = hours+":"+minutes;
        var tmp=FormatNumberLength(hoursInt+1,2);
        var nextHour = tmp+":"+minutes;

        $("#start-hour").attr('placeholder',now);
        $("#end-hour").attr('placeholder',nextHour);
        //End setting interval
        
        $('#date [type="checkbox"]').attr('checked',true)
        
        
        //Change disabled style
        $('input[disabled="true"]').css('background-color','#ddd')
    
        $( ".date-type" ).datepicker();
        
        //This code avoid to have inverted dates
        $("#start-date,#end-date").change(function(){
            var startDate=$('#start-date').val();
            var endDate=$('#end-date').val();
            if(!validateDates(startDate,endDate)){
                if($(this).attr('id')=="start-date")
                    $('#end-date').val(startDate);
                else
                    $('#start-date').val(endDate);
            }
        })
        
        //This code avoid to have inverted dates
        //$("#start-hour,end-hour").change(function(){
        //    var startHour=$('#start-hour').val();
        //    var endHour=$('#end-hour').val();
        //    if(!validateTimes(startHour,endHour)){
        //        if($(this).attr('id')=="start-hour")
        //            $('#end-hour').val(startHour);
        //        else
        //            $('#start-hour').val(endHour);
        //    }
        //})
        
        
        //Enable/disable "All day suggestion"
        $('#date [type="checkbox"]').change(function(){
            //$("#start-date,#end-date").val(today);
            //$("#start-hour,#end-hour").val(now)
            
            if($('#date [type="checkbox"]').is(':checked')==false){
                $('#date input:not([type="checkbox"])').attr('disabled',false);
                $('#date input:not([type="checkbox"])').css('background-color','#FFFFFF');
            }else{
                $('#date input:not([type="checkbox"])').attr('disabled',true);
                $('#date input:not([type="checkbox"])').css('background-color','#DDDDDD');
            }
        });
        
        $('#date [type="checkbox"]').parent().find('span').click(function(){
            $('#date [type="checkbox"]').click();
            $('#date [type="checkbox"]').change();
        });
        
        

    /*End set date picket behaviour*/
    
    /*** placeholding ***/
    $("[placeholder]").placeholder();
    
    $("#add-details").toggle(function(){
        $('#description').slideDown('slow',function(){
            $("#add-details").addClass('used');
            
        });
        },function(){
            $('#description').slideUp('slow',function(){
                $("#add-details").removeClass('used');
                
        });
    });
    
    
    $("#add-tags").toggle(function(){
        $('#tags').slideDown('slow',function(){
            $("#add-tags").addClass('used');
            
        });
        },function(){
            $('#tags').slideUp('slow',function(){
                $("#add-tags").removeClass('used');
                
            });
    });
    
    
    $("#add-date").toggle(function(){
        $('#date').slideDown('slow',function(){
            $("#add-date").addClass('used');
            
        });
    },function(){
        $('#date').slideUp('slow',function(){
            $("#add-date").removeClass('used');
            
        });
    });
    
    
    $("#add-to-lists").toggle(function(){
        $('#lists').slideDown('slow',function(){
            $("#add-to-lists").addClass('used');
            
        });
    },function(){
        $('#lists').slideUp('slow',function(){
            $("#add-to-lists").removeClass('used');
            
        });
    });
    
    $('#visibility span').click(function(){
        var element=$(this).parent().find("span[value='private']");
        var publicElement=$(this).parent().find("span[value='public']");
        if($(element).css("display")=="none"){
            $(element).show()
            publicElement.hide()
            $('#social-share').fadeOut('slow');
        }else{
            $(element).hide()
            publicElement.show()
            $('#social-share').fadeIn('slow');
        }
        
    });
    
    //Toggle share suggestion on social networks
    $('#social-share ul li span').click(function(){
        if($(this).hasClass("facebook-active")){
            $(this).removeClass("facebook-active").addClass("facebook-inactive");
            $(this).parent().addClass("inactive");
        }
        else if($(this).hasClass("facebook-inactive") && ! $(this).hasClass("request-access")){
            $(this).removeClass("facebook-inactive").addClass("facebook-active");
            $(this).parent().removeClass("inactive");
        }
        else if($(this).hasClass("twitter-active")){
            $(this).removeClass("twitter-active").addClass("twitter-inactive");
            $(this).parent().addClass("inactive");
        }
        else if($(this).hasClass("twitter-inactive") && ! $(this).hasClass("request-access")){
            $(this).removeClass("twitter-inactive").addClass("twitter-active");
            $(this).parent().removeClass("inactive");
        }
    })
    
    
    //Show perms
    $('.request-access').each(function(i,elem){
        if($(elem).hasClass("twitter-inactive"))
            $(elem).click(function(){
                $('#'+$(this).attr('id')+'-text').dialog("open");
            });
        else if($(elem).hasClass("facebook-inactive"))
            $(elem).click(function(){
                $('#'+$(this).attr('id')+'-text').dialog("open");
            });
    });
            
    
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
    /*$('#address-container').resizable({
        maxWidth: 550 ,
        minWidth: 550,
        handles: 'n,s',
        alsoResize: "#map_canvas",
        stop: function(event, ui) {
            resizeIframe()     
        }
    });*/

    
    //FORM
    //~ setFormBehaviour();
    
    //~ 
    instanceMap();
    
    
    var time=[];
    for(hours=0; hours<24; hours++){
        for(minutes=0; minutes<60; minutes=minutes+30)
            time.push(FormatNumberLength(hours,2)+":"+FormatNumberLength(minutes,2))
    }
    
    $( "#start-hour" ).autocomplete({
        minLength:0,
        source: function(req, add){ req.term = ''; add(time); }
    });
    $( "#end-hour" ).autocomplete({
        minLength:0,
        source: function(req, add){

			var idx = time.indexOf($("#start-hour").val());

			add(time.slice(idx+1));
			}
    });
    
    $( "#start-hour,#end-hour" ).focus(function(){ $(this).autocomplete("search"); });
    $( "#start-hour,#end-hour" ).click(function(){ $(this).autocomplete("search"); });

});

function instanceMap(){
    //Esta funciÃ³n crea un mapa nuevo
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
            alert("Geocoder failed due to: " + status);
        }
    });
    
    //AcciÃ³n al cambiar el nombre de la ciudad
    $('#google-city').change(function(){
        
        //Sobreescribimos la variable global location para que para las
        //nuevas bÃºsquedas use ese valor
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
                                $('#answerMessage').text(gettext("Ha habido un error al aÃ±adir la sugerencia, estamos trabajando para solucionarlo.")).fadeIn('slow').delay(2000).fadeOut('slow');
                            }else{
                                $('#answerMessage').removeClass('error');
                                $('#answerMessage').addClass('success');
                                $('#answerMessage').text(gettext("La sugerencia ha sido aÃ±adida con Ã©xito")).fadeIn('slow').delay(2000).fadeOut('slow');
                                
                                //Sobreescribimos los valores anteriores para que cuando volvamos
                                //a desplegar la configuraciÃ³n salga bien
                                searchconfig_google['location']=latlong
                                searchconfig_google['type']=$('input[name="place-type"]:checked').val();
                                searchconfig_google['radius']=$('#radius').val();
                                
                                //Minimizamos el menu de configuraciÃ³n
                                showSettings()
                                
                            }
                            $('#savingSettings').text("Guardar")
                        }
                    });//End AJAX
                } else {
                    alert("Geocode was not successful for the following reason: " + status);
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
        //Se ha entrado desde aÃ±adir una sugerencia a un sitio (vista sitio)
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
	//autocompleteAddress();
}



function autocompleteAddress()
{

    $("#place")
        .autocomplete({
         //This bit uses the geocoder to fetch address values
          autoFocus: true,
          source: function(request, response) {

			var data = {};
			var service = new google.maps.places.PlacesService(map);

			data['location'] = new google.maps.LatLng(map.getCenter().lat(),map.getCenter().lng());
			data['radius'] = searchconfig_google['radius'];
			//data['sensor'] = "false";
			data['key'] = "AIzaSyBWrR-O_l5STwv1EO7U_Y3JNOnVjexf710";
			data['name'] = request.term;
			//data['types'] = 'all';

			service.search(data, function(results,status) { 
				response($.map(results, function(item) {
					return {
					  label:  item.name,
					  value: item.name
					  //latitude: item.geometry.location.lat(),
					  //longitude: item.geometry.location.lng()
					}
				  }));

				 });

			/*
			$.ajax({
				type:"get",
				url: "https://maps.googleapis.com/maps/api/place/search/json",
				data: data,
				dataType: "json",
				success: function(data) { console.debug(data); },
				error: function(data) { console.debug(data); },
				
				});
			  
            geocoder.geocode( {'address': request.term }, function(results, status) {
            
                if (status != google.maps.GeocoderStatus.OK)
                    return;
            
              response($.map(results, function(item) {
                return {
                  label:  item.formatted_address,
                  value: item.formatted_address,
                  latitude: item.geometry.location.lat(),
                  longitude: item.geometry.location.lng()
                }
              }));
            })*/
          },
          //This bit is executed upon selection of an address
          select: function(event, ui) {

                var location = new google.maps.LatLng(ui.item.latitude, ui.item.longitude);
                    
                map.setCenter(location);
          }
        });
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
    $(mirilla).attr('title','My location');
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
            //~ //Sino tan solo actualizamos la posiciÃ³n
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
    //Le aÃ±adimos los botones
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
            showMessage('Por favor introduce primero la sugerencia',"error");
            $('#suggestion-item textarea').focus()
            return false;
        }
        
        if(placeReference==null){
            showMessage('Por favor indique el campo "Â¿Donde?" para continuar',"error");
            $('#place').focus()
            return false;
        }
        
        if($('#date [type="checkbox"]').is(':checked')==false){
            if($('#start-date').val()!="mm/dd/aa" && $('#end-date').val()!="mm/dd/aa"){
                //Hacemos las comparaciones cuando estÃ¡n la fecha de inicio y la de fin
                var startDate = new Date($('#start-date').val());
                var endDate = new Date($('#end-date').val());
                
                if (startDate > endDate){
                    //Comprobamos que inicio < fin
                    showMessage('Por favor revise que la fecha de inicio sea anterior a la de fin',"error");
                    return false;
                }else if(startDate == endDate && $('#start-hour').val() !="hh:mm" && $('#end-hour').val() !="hh:mm"){
                    //Comprobamos que si inicio < fin -> hora inicio < hora fin
                    var startHour=$('#start-hour').val().split(":");
                    var endHour=$('#end-hour').val().split(":");
                    if(startHour[0]>endHour[0]){
                        showMessage('Por favor revise que la hora de inicio sea anterior a la de fin',"error");
                        return false;
                    }else if(startHour[0]==endHour[0]){
                        if(startHour[1]>endHour[1]){
                            showMessage('Por favor revise que la hora de inicio sea anterior a la de fin',"error");
                            return false;
                        }
                    }
                }
            }
        }
        
        
        $('#submit-button').text("Enviando...")
        $('#submit-button').addClass("waiting")
        GRM.wait();
        
        var params = { 
            name: $('#id_name').val(), 
            place_reference: placeReference,

			// esto envia el campo vacÃ­o si tiene el mismo valor que el placeholder
            description: ($('#id_description').val() == $('#id_description').attr('placeholder'))?'':$('#id_description').val(),

            visibility: $('#id_visibility').val(),
            tags: $('#id_tags').val()
        };
        if($('#date [type="checkbox"]').is(':checked')==false){
            //~ console.log("Entro por el checkbox no marcado");
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
        
        //Si estamos editando una sugerencia aÃ±adimos el ID.
        if(typeof eventID != 'undefined')
            params['eventid']=eventID;
        
        $.ajax({
            type: "POST",
            url: "/ajax/add/suggestion/",
            data: jQuery.param(params),
            complete: function(msg){
                GRM.nowait();
                if (msg.status !=200){
                    showMessage("Error "+msg.status,"error")
                }else{
                    showMessage("La sugerencia ha sido aÃ±adida con Ã©xito","success")

                    
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
                $('#submit-button').text("Enviar")
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
    
    //Cargamos nuestras opciones de bÃºsqueda
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
    //AÃ±adimos un listener al campo
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
                //~ if(results[i].reference==poi_reference)
                    //~ console.log(results[i])
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


/*
 * jQuery Autocomplete plugin 1.1
 *
 * Copyright (c) 2009 JÃ¶rn Zaefferer
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 * Revision: $Id: jquery.autocomplete.js 15 2009-08-22 10:30:27Z joern.zaefferer $
 */

;(function($) {

$.fn.extend({
	geoautocomplete: function(urlOrData, options) {
		var isUrl = typeof urlOrData == "string";
		options = $.extend({}, $.GeoAutocompleter.defaults, {
			url: isUrl ? urlOrData : null,
			data: isUrl ? null : urlOrData,
			delay: isUrl ? $.GeoAutocompleter.defaults.delay : 10,
			max: options && !options.scroll ? 10 : 150
		}, options);

		// if highlight is set to false, replace it with a do-nothing function
		options.highlight = options.highlight || function(value) { return value; };

		// if the formatMatch option is not specified, then use formatItem for backwards compatibility
		options.formatMatch = options.formatMatch || options.formatItem;

		return this.each(function() {
			new $.GeoAutocompleter(this, options);
		});
	},
	result: function(handler) {
		return this.bind("result", handler);
	},
	search: function(handler) {
		return this.trigger("search", [handler]);
	},
	flushCache: function() {
		return this.trigger("flushCache");
	},
	setOptions: function(options){
		return this.trigger("setOptions", [options]);
	},
	unautocomplete: function() {
		return this.trigger("unautocomplete");
	}
});

$.GeoAutocompleter = function(input, options) {

	var KEY = {
		UP: 38,
		DOWN: 40,
		DEL: 46,
		TAB: 9,
		RETURN: 13,
		ESC: 27,
		COMMA: 188,
		PAGEUP: 33,
		PAGEDOWN: 34,
		BACKSPACE: 8
	};

	// Create $ object for input element
	var $input = $(input).attr("autocomplete", "off").addClass(options.inputClass);

	var timeout;
	var previousValue = "";
	var cache = $.GeoAutocompleter.Cache(options);
	var hasFocus = 0;
	var lastKeyPressCode;
	var config = {
		mouseDownOnSelect: false
	};
	var select = $.GeoAutocompleter.Select(options, input, selectCurrent, config);

	var blockSubmit;

	// prevent form submit in opera when selecting with return key
	$.browser.opera && $(input.form).bind("submit.autocomplete", function() {
		if (blockSubmit) {
			blockSubmit = false;
			return false;
		}
	});

	// only opera doesn't trigger keydown multiple times while pressed, others don't work with keypress at all
	$input.bind(($.browser.opera ? "keypress" : "keydown") + ".autocomplete", function(event) {
		// a keypress means the input has focus
		// avoids issue where input had focus before the autocomplete was applied
		hasFocus = 1;
		// track last key pressed
		lastKeyPressCode = event.keyCode;
		switch(event.keyCode) {

			case KEY.UP:
				event.preventDefault();
				if ( select.visible() ) {
					select.prev();
				} else {
					onChange(0, true);
				}
				break;

			case KEY.DOWN:
				event.preventDefault();
				if ( select.visible() ) {
					select.next();
				} else {
					onChange(0, true);
				}
				break;

			case KEY.PAGEUP:
				event.preventDefault();
				if ( select.visible() ) {
					select.pageUp();
				} else {
					onChange(0, true);
				}
				break;

			case KEY.PAGEDOWN:
				event.preventDefault();
				if ( select.visible() ) {
					select.pageDown();
				} else {
					onChange(0, true);
				}
				break;

			// matches also semicolon
			case options.multiple && $.trim(options.multipleSeparator) == "," && KEY.COMMA:
			case KEY.TAB:
			case KEY.RETURN:
				if( selectCurrent() ) {
					// stop default to prevent a form submit, Opera needs special handling
					event.preventDefault();
					blockSubmit = true;
					return false;
				}
				break;

			case KEY.ESC:
				select.hide();
				break;

			default:
				clearTimeout(timeout);
				timeout = setTimeout(onChange, options.delay);
				break;
		}
	}).focus(function(){
		// track whether the field has focus, we shouldn't process any
		// results if the field no longer has focus
		hasFocus++;
	}).blur(function() {
		hasFocus = 0;
		if (!config.mouseDownOnSelect) {
			hideResults();
		}
	}).click(function() {
		// show select when clicking in a focused field
		if ( hasFocus++ > 1 && !select.visible() ) {
			onChange(0, true);
		}
	}).bind("search", function() {
		// TODO why not just specifying both arguments?
		var fn = (arguments.length > 1) ? arguments[1] : null;
		function findValueCallback(q, data) {
			var result;
			if( data && data.length ) {
				for (var i=0; i < data.length; i++) {
					if( data[i].result.toLowerCase() == q.toLowerCase() ) {
						result = data[i];
						break;
					}
				}
			}
			if( typeof fn == "function" ) fn(result);
			else $input.trigger("result", result && [result.data, result.value]);
		}
		$.each(trimWords($input.val()), function(i, value) {
			request(value, findValueCallback, findValueCallback);
		});
	}).bind("flushCache", function() {
		cache.flush();
	}).bind("setOptions", function() {
		$.extend(options, arguments[1]);
		// if we've updated the data, repopulate
		if ( "data" in arguments[1] )
			cache.populate();
	}).bind("unautocomplete", function() {
		select.unbind();
		$input.unbind();
		$(input.form).unbind(".autocomplete");
	});


	function selectCurrent() {
		var selected = select.selected();
		if( !selected )
			return false;

		var v = selected.result;
		previousValue = v;

		if ( options.multiple ) {
			var words = trimWords($input.val());
			if ( words.length > 1 ) {
				var seperator = options.multipleSeparator.length;
				var cursorAt = $(input).selection().start;
				var wordAt, progress = 0;
				$.each(words, function(i, word) {
					progress += word.length;
					if (cursorAt <= progress) {
						wordAt = i;
						return false;
					}
					progress += seperator;
				});
				words[wordAt] = v;
				// TODO this should set the cursor to the right position, but it gets overriden somewhere
				//$.Autocompleter.Selection(input, progress + seperator, progress + seperator);
				v = words.join( options.multipleSeparator );
			}
			v += options.multipleSeparator;
		}

		$input.val(v);
		hideResultsNow();
		$input.trigger("result", [selected.data, selected.value]);
		return true;
	}

	function onChange(crap, skipPrevCheck) {
		if( lastKeyPressCode == KEY.DEL ) {
			select.hide();
			return;
		}

		var currentValue = $input.val();

		if ( !skipPrevCheck && currentValue == previousValue )
			return;

		previousValue = currentValue;

		currentValue = lastWord(currentValue);
		if ( currentValue.length >= options.minChars) {
			$input.addClass(options.loadingClass);
			if (!options.matchCase)
				currentValue = currentValue.toLowerCase();
			request(currentValue, receiveData, hideResultsNow);
		} else {
			stopLoading();
			select.hide();
		}
	};

	function trimWords(value) {
		if (!value)
			return [""];
		if (!options.multiple)
			return [$.trim(value)];
		return $.map(value.split(options.multipleSeparator), function(word) {
			return $.trim(value).length ? $.trim(word) : null;
		});
	}

	function lastWord(value) {
		if ( !options.multiple )
			return value;
		var words = trimWords(value);
		if (words.length == 1) 
			return words[0];
		var cursorAt = $(input).selection().start;
		if (cursorAt == value.length) {
			words = trimWords(value)
		} else {
			words = trimWords(value.replace(value.substring(cursorAt), ""));
		}
		return words[words.length - 1];
	}

	// fills in the input box w/the first match (assumed to be the best match)
	// q: the term entered
	// sValue: the first matching result
	function autoFill(q, sValue){
		// autofill in the complete box w/the first match as long as the user hasn't entered in more data
		// if the last user key pressed was backspace, don't autofill
		if( options.autoFill && (lastWord($input.val()).toLowerCase() == q.toLowerCase()) && lastKeyPressCode != KEY.BACKSPACE ) {
			// fill in the value (keep the case the user has typed)
			$input.val($input.val() + sValue.substring(lastWord(previousValue).length));
			// select the portion of the value not typed by the user (so the next character will erase)
			$(input).selection(previousValue.length, previousValue.length + sValue.length);
		}
	};

	function hideResults() {
		clearTimeout(timeout);
		timeout = setTimeout(hideResultsNow, 200);
	};

	function hideResultsNow() {
		var wasVisible = select.visible();
		select.hide();
		clearTimeout(timeout);
		stopLoading();
		if (options.mustMatch) {
			// call search and run callback
			$input.search(
				function (result){
					// if no value found, clear the input box
					if( !result ) {
						if (options.multiple) {
							var words = trimWords($input.val()).slice(0, -1);
							$input.val( words.join(options.multipleSeparator) + (words.length ? options.multipleSeparator : "") );
						}
						else {
							$input.val( "" );
							$input.trigger("result", null);
						}
					}
				}
			);
		}
	};

	function receiveData(q, data) {
		if ( data && data.length && hasFocus ) {
			stopLoading();
			select.display(data, q);
			autoFill(q, data[0].value);
			select.show();
		} else {
			hideResultsNow();
		}
	};

	function request(term, success, failure) {
		if (!options.matchCase)
			term = term.toLowerCase();
		var data = cache.load(term);
		// recieve the cached data
		if (data && data.length) {
			success(term, data);

		// start geo_Autocomplete mod
		// request handler for google geocoder
		} else if (options.geocoder) {
			var _query = lastWord(term);
			options.geocoder.geocode({'address': _query}, function(_results, _status) {
				var parsed = options.parse(_results, _status, _query);
				cache.add(term, parsed);
				success(term, parsed);
			});
		// end geo_Autocomplete mod

		// if an AJAX url has been supplied, try loading the data now
		} else if( (typeof options.url == "string") && (options.url.length > 0) ){

			var extraParams = {
				timestamp: +new Date()
			};
			$.each(options.extraParams, function(key, param) {
				extraParams[key] = typeof param == "function" ? param() : param;
			});

			$.ajax({
				// try to leverage ajaxQueue plugin to abort previous requests
				mode: "abort",
				// limit abortion to this input
				port: "autocomplete" + input.name,
				dataType: options.dataType,
				url: options.url,
				data: $.extend({
					q: lastWord(term),
					limit: options.max
				}, extraParams),
				success: function(data) {
					var parsed = options.parse && options.parse(data) || parse(data);
					cache.add(term, parsed);
					success(term, parsed);
				}
			});

		} else {
			// if we have a failure, we need to empty the list -- this prevents the the [TAB] key from selecting the last successful match
			select.emptyList();
			failure(term);
		}
	};

	function parse(data) {
		var parsed = [];
		var rows = data.split("\n");
		for (var i=0; i < rows.length; i++) {
			var row = $.trim(rows[i]);
			if (row) {
				row = row.split("|");
				parsed[parsed.length] = {
					data: row,
					value: row[0],
					result: options.formatResult && options.formatResult(row, row[0]) || row[0]
				};
			}
		}
		return parsed;
	};

	function stopLoading() {
		$input.removeClass(options.loadingClass);
	};

};

$.GeoAutocompleter.defaults = {
	inputClass: "ac_input",
	resultsClass: "ac_results",
	loadingClass: "ac_loading",
	minChars: 1,
	delay: 400,
	matchCase: false,
	matchSubset: true,
	matchContains: false,
	cacheLength: 10,
	max: 100,
	mustMatch: false,
	extraParams: {},
	selectFirst: true,
	formatItem: function(row) { return row[0]; },
	formatMatch: null,
	autoFill: false,
	width: 0,
	multiple: false,
	multipleSeparator: ", ",
	highlight: function(value, term) {
		return value.replace(new RegExp("(?![^&;]+;)(?!<[^<>]*)(" + term.replace(/([\^\$\(\)\[\]\{\}\*\.\+\?\|\\])/gi, "\\$1") + ")(?![^<>]*>)(?![^&;]+;)", "gi"), "<strong>$1</strong>");
	},
    scroll: true,
    scrollHeight: 180
};

$.GeoAutocompleter.Cache = function(options) {

	var data = {};
	var length = 0;

	function matchSubset(s, sub) {
		if (!options.matchCase) 
			s = s.toLowerCase();
		var i = s.indexOf(sub);
		if (options.matchContains == "word"){
			i = s.toLowerCase().search("\\b" + sub.toLowerCase());
		}
		if (i == -1) return false;
		return i == 0 || options.matchContains;
	};

	function add(q, value) {
		if (length > options.cacheLength){
			flush();
		}
		if (!data[q]){ 
			length++;
		}
		data[q] = value;
	}

	function populate(){
		if( !options.data ) return false;
		// track the matches
		var stMatchSets = {},
			nullData = 0;

		// no url was specified, we need to adjust the cache length to make sure it fits the local data store
		if( !options.url ) options.cacheLength = 1;

		// track all options for minChars = 0
		stMatchSets[""] = [];

		// loop through the array and create a lookup structure
		for ( var i = 0, ol = options.data.length; i < ol; i++ ) {
			var rawValue = options.data[i];
			// if rawValue is a string, make an array otherwise just reference the array
			rawValue = (typeof rawValue == "string") ? [rawValue] : rawValue;

			var value = options.formatMatch(rawValue, i+1, options.data.length);
			if ( value === false )
				continue;

			var firstChar = value.charAt(0).toLowerCase();
			// if no lookup array for this character exists, look it up now
			if( !stMatchSets[firstChar] ) 
				stMatchSets[firstChar] = [];

			// if the match is a string
			var row = {
				value: value,
				data: rawValue,
				result: options.formatResult && options.formatResult(rawValue) || value
			};

			// push the current match into the set list
			stMatchSets[firstChar].push(row);

			// keep track of minChars zero items
			if ( nullData++ < options.max ) {
				stMatchSets[""].push(row);
			}
		};

		// add the data items to the cache
		$.each(stMatchSets, function(i, value) {
			// increase the cache size
			options.cacheLength++;
			// add to the cache
			add(i, value);
		});
	}

	// populate any existing data
	setTimeout(populate, 25);

	function flush(){
		data = {};
		length = 0;
	}

	return {
		flush: flush,
		add: add,
		populate: populate,
		load: function(q) {
			if (!options.cacheLength || !length)
				return null;
			/* 
			 * if dealing w/local data and matchContains than we must make sure
			 * to loop through all the data collections looking for matches
			 */
			if( !options.url && options.matchContains ){
				// track all matches
				var csub = [];
				// loop through all the data grids for matches
				for( var k in data ){
					// don't search through the stMatchSets[""] (minChars: 0) cache
					// this prevents duplicates
					if( k.length > 0 ){
						var c = data[k];
						$.each(c, function(i, x) {
							// if we've got a match, add it to the array
							if (matchSubset(x.value, q)) {
								csub.push(x);
							}
						});
					}
				}				
				return csub;
			} else 
			// if the exact item exists, use it
			if (data[q]){
				return data[q];
			} else
			if (options.matchSubset) {
				for (var i = q.length - 1; i >= options.minChars; i--) {
					var c = data[q.substr(0, i)];
					if (c) {
						var csub = [];
						$.each(c, function(i, x) {
							if (matchSubset(x.value, q)) {
								csub[csub.length] = x;
							}
						});
						return csub;
					}
				}
			}
			return null;
		}
	};
};

$.GeoAutocompleter.Select = function (options, input, select, config) {
	var CLASSES = {
		ACTIVE: "ac_over"
	};

	var listItems,
		active = -1,
		data,
		term = "",
		needsInit = true,
		element,
		list;

	// Create results
	function init() {
		if (!needsInit)
			return;
		element = $("<div/>")
		.hide()
		.addClass(options.resultsClass)
		.css("position", "absolute")
		.appendTo(document.body);

		list = $("<ul/>").appendTo(element).mouseover( function(event) {
			if(target(event).nodeName && target(event).nodeName.toUpperCase() == 'LI') {
	            active = $("li", list).removeClass(CLASSES.ACTIVE).index(target(event));
			    $(target(event)).addClass(CLASSES.ACTIVE);            
	        }
		}).click(function(event) {
			$(target(event)).addClass(CLASSES.ACTIVE);
			select();
			// TODO provide option to avoid setting focus again after selection? useful for cleanup-on-focus
			input.focus();
			return false;
		}).mousedown(function() {
			config.mouseDownOnSelect = true;
		}).mouseup(function() {
			config.mouseDownOnSelect = false;
		});

		if( options.width > 0 )
			element.css("width", options.width);

		needsInit = false;
	} 

	function target(event) {
		var element = event.target;
		while(element && element.tagName != "LI")
			element = element.parentNode;
		// more fun with IE, sometimes event.target is empty, just ignore it then
		if(!element)
			return [];
		return element;
	}

	function moveSelect(step) {
		listItems.slice(active, active + 1).removeClass(CLASSES.ACTIVE);
		movePosition(step);
        var activeItem = listItems.slice(active, active + 1).addClass(CLASSES.ACTIVE);
        if(options.scroll) {
            var offset = 0;
            listItems.slice(0, active).each(function() {
				offset += this.offsetHeight;
			});
            if((offset + activeItem[0].offsetHeight - list.scrollTop()) > list[0].clientHeight) {
                list.scrollTop(offset + activeItem[0].offsetHeight - list.innerHeight());
            } else if(offset < list.scrollTop()) {
                list.scrollTop(offset);
            }
        }
	};

	function movePosition(step) {
		active += step;
		if (active < 0) {
			active = listItems.size() - 1;
		} else if (active >= listItems.size()) {
			active = 0;
		}
	}

	function limitNumberOfItems(available) {
		return options.max && options.max < available
			? options.max
			: available;
	}

	function fillList() {
		list.empty();
		var max = limitNumberOfItems(data.length);
		for (var i=0; i < max; i++) {
			if (!data[i])
				continue;
			var formatted = options.formatItem(data[i].data, i+1, max, data[i].value, term);
			if ( formatted === false )
				continue;
			var li = $("<li/>").html( options.highlight(formatted, term) ).addClass(i%2 == 0 ? "ac_even" : "ac_odd").appendTo(list)[0];
			$.data(li, "ac_data", data[i]);
		}
		listItems = list.find("li");
		if ( options.selectFirst ) {
			listItems.slice(0, 1).addClass(CLASSES.ACTIVE);
			active = 0;
		}
		// apply bgiframe if available
		if ( $.fn.bgiframe )
			list.bgiframe();
	}

	return {
		display: function(d, q) {
			init();
			data = d;
			term = q;
			fillList();
		},
		next: function() {
			moveSelect(1);
		},
		prev: function() {
			moveSelect(-1);
		},
		pageUp: function() {
			if (active != 0 && active - 8 < 0) {
				moveSelect( -active );
			} else {
				moveSelect(-8);
			}
		},
		pageDown: function() {
			if (active != listItems.size() - 1 && active + 8 > listItems.size()) {
				moveSelect( listItems.size() - 1 - active );
			} else {
				moveSelect(8);
			}
		},
		hide: function() {
			element && element.hide();
			listItems && listItems.removeClass(CLASSES.ACTIVE);
			active = -1;
		},
		visible : function() {
			return element && element.is(":visible");
		},
		current: function() {
			return this.visible() && (listItems.filter("." + CLASSES.ACTIVE)[0] || options.selectFirst && listItems[0]);
		},
		show: function() {
			var offset = $(input).offset();
			element.css({
				width: typeof options.width == "string" || options.width > 0 ? options.width : $(input).width(),
				top: offset.top + input.offsetHeight,
				left: offset.left
			}).show();
            if(options.scroll) {
                list.scrollTop(0);
                list.css({
					maxHeight: options.scrollHeight,
					overflow: 'auto'
				});

                if($.browser.msie && typeof document.body.style.maxHeight === "undefined") {
					var listHeight = 0;
					listItems.each(function() {
						listHeight += this.offsetHeight;
					});
					var scrollbarsVisible = listHeight > options.scrollHeight;
                    list.css('height', scrollbarsVisible ? options.scrollHeight : listHeight );
					if (!scrollbarsVisible) {
						// IE doesn't recalculate width when scrollbar disappears
						listItems.width( list.width() - parseInt(listItems.css("padding-left")) - parseInt(listItems.css("padding-right")) );
					}
                }
                
            }
		},
		selected: function() {
			var selected = listItems && listItems.filter("." + CLASSES.ACTIVE).removeClass(CLASSES.ACTIVE);
			return selected && selected.length && $.data(selected[0], "ac_data");
		},
		emptyList: function (){
			list && list.empty();
		},
		unbind: function() {
			element && element.remove();
		}
	};
};

$.fn.selection = function(start, end) {
	if (start !== undefined) {
		return this.each(function() {
			if( this.createTextRange ){
				var selRange = this.createTextRange();
				if (end === undefined || start == end) {
					selRange.move("character", start);
					selRange.select();
				} else {
					selRange.collapse(true);
					selRange.moveStart("character", start);
					selRange.moveEnd("character", end);
					selRange.select();
				}
			} else if( this.setSelectionRange ){
				this.setSelectionRange(start, end);
			} else if( this.selectionStart ){
				this.selectionStart = start;
				this.selectionEnd = end;
			}
		});
	}
	var field = this[0];
	if ( field.createTextRange ) {
		var range = document.selection.createRange(),
			orig = field.value,
			teststring = "<->",
			textLength = range.text.length;
		range.text = teststring;
		var caretAt = field.value.indexOf(teststring);
		field.value = orig;
		this.selection(caretAt, caretAt + textLength);
		return {
			start: caretAt,
			end: caretAt + textLength
		}
	} else if( field.selectionStart !== undefined ){
		return {
			start: field.selectionStart,
			end: field.selectionEnd
		}
	}
};

})(jQuery);

/*
 * jQuery geo_autocomplete plugin 1.0
 *
 * Copyright (c) 2009 Bob Hitching
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 *
 * Requires jQuery Autocomplete plugin by Jörn Zaefferer - see http://bassistance.de/jquery-plugins/jquery-plugin-autocomplete/
 * jquery.autocomplete.js requires a minor modification for geo_autocomplete to work, as shown in /lib/jquery.autocomplete_geomod.js
 * 
 */
;(function($) {

$.fn.extend({
	geo_autocomplete: function(_geocoder, _options) {
		options = $.extend({}, $.GeoAutocompleter.defaults, {
			geocoder: _geocoder,
			mapwidth: 100,
			mapheight: 100,
			maptype: 'terrain',
			mapkey: 'ABQIAAAAbnvDoAoYOSW2iqoXiGTpYBT2yXp_ZAY8_ufC3CFXhHIE1NvwkxQNumU68AwGqjbSNF9YO8NokKst8w', // localhost
			mapsensor: false,
			parse: function(_results, _status, _query) {
				var _parsed = [];
				if (_results && _status && _status == 'OK') {
					$.each(_results, function(_key, _result) {
						if (_result.geometry && _result.geometry.viewport) {
							// place is first matching segment, or first segment
							var _place_parts = _result.formatted_address.split(',');
							var _place = _place_parts[0];
							$.each(_place_parts, function(_key, _part) {
								if (_part.toLowerCase().indexOf(_query.toLowerCase()) != -1) {
									_place = $.trim(_part);
									return false; // break
								}
							});
							_parsed.push({
								data: _result,
								value: _place,
								result: _place
							});
						}
					});
				}
				return _parsed;
			},
			formatItem: function(_data, _i, _n, _value) {
				var _src = 'http://maps.google.com/maps/api/staticmap?visible=' + _data.geometry.viewport.getSouthWest().toUrlValue() + '|' + _data.geometry.viewport.getNorthEast().toUrlValue() + '&size=' + options.mapwidth + 'x' + options.mapheight + '&maptype=' + options.maptype + '&key=' + options.mapkey + '&sensor=' + (options.mapsensor ? 'true' : 'false');
				var _place = _data.formatted_address.replace(/,/gi, ',<br/>');
				return '<img src="' + _src + '" width="' + options.mapwidth + '" height="' + options.mapheight + '" /> ' + _place + '<br clear="both"/>';
			}
		}, _options);

		// if highlight is set to false, replace it with a do-nothing function
		options.highlight = options.highlight || function(value) { return value; };

		// if the formatMatch option is not specified, then use formatItem for backwards compatibility
		options.formatMatch = options.formatMatch || options.formatItem;

		return this.each(function() {
			new $.GeoAutocompleter(this, options);
		});
	}
});

})(jQuery);
