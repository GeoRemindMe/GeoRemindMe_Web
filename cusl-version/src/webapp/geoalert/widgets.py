from django import forms


DEFAULT_WIDTH = 500
DEFAULT_HEIGHT = 300

class LocationWidget(forms.widgets.Widget):
    def __init__(self, *args, **kw):
        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)
        
        super(self.__class__, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value
        lat, lng = float(a), float(b)
        
        js = '''
<script type="text/javascript">
//<![CDATA[

    var alerts_%(name)s = %(alerts)s;
    var map_%(name)s;
    var geo = new GClientGeocoder();
    var status = {};
    status[G_GEO_SUCCESS] = 200;
    status[G_GEO_BAD_REQUEST] = "ERROR";
    status[G_GEO_SERVER_ERROR] = "SERVER ERROR";
    status[G_GEO_MISSING_QUERY] = "ERROR";
    status[G_GEO_MISSING_ADDRESS] = "ERROR";
    status[G_GEO_UNKNOWN_ADDRESS] = "UNKNOW ADDRESS";
    status[G_GEO_UNAVAILABLE_ADDRESS] = "UNAVAILABLE ADDRESS";
    status[G_GEO_UNKNOWN_DIRECTIONS] = "NO DIRECTIONS AVAILABLE";
    status[G_GEO_BAD_KEY] = "INVALID API KEY";
    status[G_GEO_TOO_MANY_QUERIES] = "TOO MANY QUERIES, TRY AGAIN";
    
    function savePosition_%(name)s(point)
    {
	    var latitude = document.getElementById("id_%(name)s");
	    latitude.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }

    function load_%(name)s() {
        if (GBrowserIsCompatible()) {
            map_%(name)s = new GMap2(document.getElementById("map_%(name)s"));
            map_%(name)s.addControl(new GSmallMapControl());
            map_%(name)s.addControl(new GMapTypeControl());
            
            var point = new GLatLng(%(lat)f, %(lng)f);
            map_%(name)s.setCenter(point, 15);//I USE 15 AS THE DEFAULT RESOLUTION
            var m = new GMarker(point, {draggable: true});
            moveTo(point)
            
            /* save coordinates on dragend */
            GEvent.addListener(m, "dragend", function() {
                point = m.getPoint();
                moveTo(point)
            });
            /* save coordinates on clicks */
            GEvent.addListener(map_%(name)s, "click", function (overlay, point) {
                m = new GMarker(point, {draggable: true});
                moveTo(point)
                GEvent.addListener(m, "dragend", function() {
                    point = m.getPoint();
                    moveTo(point)
                });
            });
        }
    }
    function drawMarkers()
    {
            var ico = new GIcon(G_DEFAULT_ICON);
            ico.image = '/static/images/marker1.png';
            ico.iconSize = new GSize(40,35);
       
            for (var i=0;i<alerts_%(name)s.length;i++)
            {
                var point = new GLatLng(alerts_%(name)s[i].x,alerts_%(name)s[i].y);
                var ma = new GMarker(point,{
                    icon: ico, 
                    draggable: false,
                });
                
                ma.georemindinfo = {
                    key: alerts_%(name)s[i].key,
                    name: alerts_%(name)s[i].name,
                    desc: alerts_%(name)s[i].description,
                    addr: alerts_%(name)s[i].addr,
                    starts: alerts_%(name)s[i].starts,
                    ends: alerts_%(name)s[i].ends
                    };
                
                /*
                geo.getLocations(point, function(response) {
                    if (response.Status.code==200){
                        addr =response.Placemark[0].address;
                    }
                });
                */
                
                GEvent.addListener(ma, "click", function(){
                    this.openInfoWindowHtml("<a href='/user/view/"+this.georemindinfo['key']+"'>"+this.georemindinfo['name']+"</a>"+
                                "<br><b>Address: </b>"+this.georemindinfo['addr']+
                                "<br><b>Starts:</b> "+this.georemindinfo['starts']+" <b>Ends: </b> "+this.georemindinfo['ends']+
                                "<br><b>Description: </b>"+this.georemindinfo['desc']);
                });
                map_%(name)s.addOverlay(ma);                
            }
    }
    
    function setCurrentPosition()
    {
        if (navigator.geolocation) 
        {
            navigator.geolocation.getCurrentPosition( 
                function (position) { 
                    var pos = new GLatLng(position.coords.latitude,position.coords.longitude);
                    moveTo(pos);
                }, 
                function (error) { });
        }
    }
    
    function moveTo(point)
    {
        savePosition_%(name)s(point);
        setCurrentAddress(point);
        map_%(name)s.clearOverlays();
        // paint the near alerts
        var m = new GMarker(point, {draggable: true});
        GEvent.addListener(m, "dragend", function() {
            map_%(name)s.clearOverlays();
            point = m.getPoint();
            map_%(name)s.addOverlay(m);
            setCurrentAddress(point);
            savePosition_%(name)s(point);
            drawMarkers();
        });
        map_%(name)s.addOverlay(m);
        // paint the near alerts
        drawMarkers();
    }
    
    function setCurrentAddress(point)
    {
        document.getElementById("list_%(name)s").innerHTML = "";
        geo.getLocations(point, function(response) {
            if (response.Status.code==200)
            {
                document.getElementById("list_%(name)s").innerHTML = '';
                document.getElementById("address_%(name)s").value=response.Placemark[0].address;
            }
        });
    }
    
    function getAddress() {//query google for all address similar to user input in address_location
        var addr = document.getElementById("address_%(name)s").value;
        if (addr != ""){
            geo.getLocations(addr, function(result) {
                document.getElementById("list_%(name)s").innerHTML = "";
                if (result.Status.code == G_GEO_SUCCESS) {//we got some address from google
                    var points = [];
                    var address = [];
                    for( var i = 0; i < result.Placemark.length; i++){//show all the results
                        points[i] = result.Placemark[i].Point;
                        address[i] = result.Placemark[i].address;
                        document.getElementById("list_%(name)s").innerHTML += "<a onClick='moveTo(new GLatLng("+points[i].coordinates[1]+", "+ points[i].coordinates[0]+"));return false;' href='#'>" + address[i] + "</a><br>";
                    } 
                }
            });
        }
    }
//]]>
</script>
        ''' % dict(name=name, lat=lat, lng=lng, alerts=kwargs.get('alerts','[]') )
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat,lng), dict(id='id_%s' % name))
        html += "<input id=\"address_%s\" class=\"gmap\" type=\"text\" name=\"address\" size=\"35\" onkeyup=\"getAddress()\" /> <br><small>Search: address, city, country</small>" % name
        html += "<p id=\"list_%s\" class=\"gmap\"></p>" % name
        html += "<a href='#' onclick='setCurrentPosition();return false;'>Ir a donde estoy</a>";
        html += "<div id=\"map_%s\" class=\"gmap\" style=\"width: %dpx; height: %dpx\"></div>" % (name, self.map_width, self.map_height)
        
        return (js+html)

class AJAXWidget(forms.widgets.Widget):
    def __init__(self, *args, **kw):
        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)
        
        super(self.__class__, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value
        lat, lng = float(a), float(b)
        
        js = '''
<script type="text/javascript">
//<![CDATA[
    /*
        AJAX
    */
    var url_request = '/user/list/near/';
    function getXMLHttp(){
        if(window.XMLHttpRequest) {
            return new XMLHttpRequest();
        }
        else if(window.ActiveXObject) {
            return new ActiveXObject("Microsoft.XMLHTTP");
        }
    }
    function MakeRequest(point){
        url = url_request + point.lat() +'/'+point.lng() +'/'
        xmlHttp = getXMLHttp();
        
        xmlHttp.onreadystatechange = function(){
            if(xmlHttp.readyState == 4){//State 4 -> all data is loaded
                HandleResponse(xmlHttp.responseText);
            }
        }
        xmlHttp.open("GET", url, true);
        //with this header we can use request.is_ajax() in django
        xmlHttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xmlHttp.send(null);
    }
    function HandleResponse(response){
        var alerts = JSON.parse(response);
        var ico = new GIcon(G_DEFAULT_ICON);
        ico.image = '/static/images/marker1.png';
        ico.iconSize = new GSize(40,35);
        for (var i=0;i<alerts.length;i++){
            var point = new GLatLng(alerts[i].x,alerts[i].y);
                var ma = new GMarker(point,{
                    icon: ico, 
                    draggable: false,
                });
                
                ma.georemindinfo = {
                    id: alerts[i].id,
                    name: alerts[i].name,
                    desc: alerts[i].description,
                    addr: alerts[i].addr,
                    starts: alerts[i].starts,
                    ends: alerts[i].ends,
                    distance: alerts[i].distance
                    };
                
                GEvent.addListener(ma, "click", function(){
                    this.openInfoWindowHtml("<a href='/user/view/"+this.georemindinfo['id']+"'>"+this.georemindinfo['name']+"</a>"+
                                "<br><b>Address: </b>"+this.georemindinfo['addr']+
                                "<br><b>Starts:</b> "+this.georemindinfo['starts']+" <b>Ends: </b> "+this.georemindinfo['ends']+
                                "<br><b>Description: </b>"+this.georemindinfo['distance']);
                });
                map_%(name)s.addOverlay(ma);           
        }
    }
 
    
    var map_%(name)s;
    var geo = new GClientGeocoder();
    var status = {};
    
    
    status[G_GEO_SUCCESS] = 200;
    status[G_GEO_BAD_REQUEST] = "ERROR";
    status[G_GEO_SERVER_ERROR] = "SERVER ERROR";
    status[G_GEO_MISSING_QUERY] = "ERROR";
    status[G_GEO_MISSING_ADDRESS] = "ERROR";
    status[G_GEO_UNKNOWN_ADDRESS] = "UNKNOW ADDRESS";
    status[G_GEO_UNAVAILABLE_ADDRESS] = "UNAVAILABLE ADDRESS";
    status[G_GEO_UNKNOWN_DIRECTIONS] = "NO DIRECTIONS AVAILABLE";
    status[G_GEO_BAD_KEY] = "INVALID API KEY";
    status[G_GEO_TOO_MANY_QUERIES] = "TOO MANY QUERIES, TRY AGAIN";
    
    function savePosition_%(name)s(point)
    {
        var latitude = document.getElementById("id_%(name)s");
        latitude.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }

    function load_%(name)s() {
        if (GBrowserIsCompatible()) {
            map_%(name)s = new GMap2(document.getElementById("map_%(name)s"));
            map_%(name)s.addControl(new GSmallMapControl());
            map_%(name)s.addControl(new GMapTypeControl());
            
            var point = new GLatLng(%(lat)f, %(lng)f);
            map_%(name)s.setCenter(point, 15);//I USE 15 AS THE DEFAULT RESOLUTION
            var m = new GMarker(point, {draggable: true});
            moveTo(point)
            
            /* save coordinates on dragend */
            GEvent.addListener(m, "dragend", function() {
                point = m.getPoint();
                moveTo(point)
            });
            /* save coordinates on clicks */
            GEvent.addListener(map_%(name)s, "click", function (overlay, point) {
                m = new GMarker(point, {draggable: true});
                moveTo(point)
                GEvent.addListener(m, "dragend", function() {
                    point = m.getPoint();
                    moveTo(point)
                });
            });
        }
    }
   
    function setCurrentPosition()
    {
        if (navigator.geolocation) 
        {
            navigator.geolocation.getCurrentPosition( 
                function (position) { 
                    var pos = new GLatLng(position.coords.latitude,position.coords.longitude);
                    moveTo(pos);
                }, 
                function (error) { });
        }
    }
    
    function moveTo(point)
    {
        savePosition_%(name)s(point);
        setCurrentAddress(point);
        map_%(name)s.clearOverlays();
        var m = new GMarker(point, {draggable: true});
        GEvent.addListener(m, "dragend", function() {
            map_%(name)s.clearOverlays();
            point = m.getPoint();
            map_%(name)s.addOverlay(m);
            setCurrentAddress(point);
            savePosition_%(name)s(point);
            MakeRequest(point);
        });
        map_%(name)s.addOverlay(m);
        // paint the near alerts
        MakeRequest(point);
        
    }
    
    function setCurrentAddress(point)
    {
        document.getElementById("list_%(name)s").innerHTML = "";
        geo.getLocations(point, function(response) {
            if (response.Status.code==200)
            {
                document.getElementById("list_%(name)s").innerHTML = '';
                document.getElementById("address_%(name)s").value=response.Placemark[0].address;
            }
        });
    }
    
    function getAddress() {//query google for all address similar to user input in address_location
        var addr = document.getElementById("address_%(name)s").value;
        if (addr != ""){
            geo.getLocations(addr, function(result) {
                document.getElementById("list_%(name)s").innerHTML = "";
                if (result.Status.code == G_GEO_SUCCESS) {//we got some address from google
                    var points = [];
                    var address = [];
                    for( var i = 0; i < result.Placemark.length; i++){//show all the results
                        points[i] = result.Placemark[i].Point;
                        address[i] = result.Placemark[i].address;
                        document.getElementById("list_%(name)s").innerHTML += "<a onClick='moveTo(new GLatLng("+points[i].coordinates[1]+", "+ points[i].coordinates[0]+"));return false;' href='#'>" + address[i] + "</a><br>";
                    } 
                }
            });
        }
    }
    
//]]>
</script>
        ''' % dict(name=name, lat=lat, lng=lng)
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat,lng), dict(id='id_%s' % name))
        html += "<input id=\"address_%s\" class=\"gmap\" type=\"text\" name=\"address\" size=\"35\" onkeyup=\"getAddress()\" /> <br><small>Search: address, city, country</small>" % name
        html += "<p id=\"list_%s\" class=\"gmap\"></p>" % name
        html += "<a href='#' onclick='setCurrentPosition();return false;'>Ir a donde estoy</a>";
        html += "<div id=\"map_%s\" class=\"gmap\" style=\"width: %dpx; height: %dpx\"></div>" % (name, self.map_width, self.map_height)
        
        return (js+html)


class LocationWidget2(forms.widgets.Widget):
    def __init__(self, *args, **kw):
        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)
        
        super(self.__class__, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value
        lat, lng = float(a), float(b)
        
        js = '''
<script type="text/javascript">
//<![CDATA[

    var map_%(name)s;
    
    function savePosition_%(name)s(point)
    {
        var latitude = document.getElementById("id_%(name)s");
        //var longitude = document.getElementById("id_%(name)s_longitude");
        latitude.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
        //longitude.value = point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }

    function load_%(name)s() {
        if (GBrowserIsCompatible()) {
            map_%(name)s = new GMap2(document.getElementById("map_%(name)s"));
            map_%(name)s.addControl(new GSmallMapControl());
            map_%(name)s.addControl(new GMapTypeControl());

            var point = new GLatLng(%(lat)f, %(lng)f);
            map_%(name)s.setCenter(point, 8);
            m = new GMarker(point, {draggable: true});

            GEvent.addListener(m, "dragend", function() {
                    point = m.getPoint();
                    savePosition_%(name)s(point);
            });

            map_%(name)s.addOverlay(m);

            /* save coordinates on clicks */
            GEvent.addListener(map_%(name)s, "click", function (overlay, point) {
                savePosition_%(name)s(point);
            
                map_%(name)s.clearOverlays();
                m = new GMarker(point, {draggable: true});

                GEvent.addListener(m, "dragend", function() {
                    point = m.getPoint();
                    savePosition_%(name)s(point);
                });

                map_%(name)s.addOverlay(m);
            });
        }
    }
//]]>
</script>
        ''' % dict(name=name, lat=lat, lng=lng)
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat,lng), dict(id='id_%s' % name))
        html += "<div id=\"map_%s\" class=\"gmap\" style=\"width: %dpx; height: %dpx\"></div>" % (name, self.map_width, self.map_height)
        
        return (js+html)
