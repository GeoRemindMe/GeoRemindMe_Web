
newTasks=0;

$(document).ready(function(){

    // default locations
    defaultX = 0;
    defaultY = 0;
    
    loadGMaps();
    
    $('#add-task').click(addTask);
    

    // help behaviour
    $('#help').toggle(function(){
            $("#help-toolbar" ).animate( { top: "0px" }, { queue: false, duration: "fast" })
        },function(){
              $("#help-toolbar" ).animate( { top: "-150px" }, { queue: false, duration: "fast" })
        });
        
    // footer behaviour
    $('#split').toggle(function(){
            $("#footer" ).animate( { bottom: "45px" }, { queue: false, duration: "fast" });
            $("#icon_split").css('background-position','0 -13px');
            $("#footer-text").html("Hide");
        },function(){
            $("#footer" ).animate( { bottom: "10px" }, { queue: false, duration: "fast" });
            $("#icon_split").css('background-position','0 2px');
            $("#footer-text").html("Show");
        });
    
    $('#add-task').disableSelection();

   //Map_container dinamic position
   $(window).resize(function() {
      setMapContainerPosition();
   });
   //$("#task-list").keyup(cursorMove);
   setMapContainerPosition();

    AJAX_URL = "/ajax/"
    
    tasks = [];
    notsaved = [];
    
    loadTasks();
    
    if (navigator.geolocation)
    {
        $("#pointer").show();
    }
    
    window.onbeforeunload = function(e) {
        saveNotSaved();
        if (notsaved.length>0)
        {
            return gettext("There are elements that could not be saved. If you leave the page you will lose it.")
        }
    };
});

//That function animates the map_container and fits it the middle of the window
function setMapContainerPosition()
{
   var $top=($(window).height()-$('#map_container').height())/2;
   if($top<50)
      $top=50;
   $('#map_container').animate( { top: $top }, "fast");
}

// Do the AJAX request and render the template
function loadTasks()
{
    // here do the ajax and get the tasks

    $.ajax({
        url: AJAX_URL+"get/reminder/",
        type:"post",
        async: true,
        dataType: "json",
        //error: function(data){console.debug(data)},
        success: function(data){ 

                var undone = [];
                var done = [];
                data = data["result"]
                for (var i in data)
                {
                    if (typeof(data[i].done)!="undefined")
                    {
                        data[i]['task'] = data[i]['id'];
                        
                        if (data[i].done)
                            done.push(data[i]);
                        else
                            undone.push(data[i]);
                    }
                }

                $( "#taskTemplate" ).tmpl( undone ).appendTo( "#task-list" );
                $( "#doneTemplate" ).tmpl( done ).appendTo( "#done-list" );
                
                $("#task-list").ready(function(){
                    $('.task').disableSelection();
                    $('.location').geoaddress();                    
                });
           
                
                // parse to get a dict
                tasks = prepareAlerts(data);
                
                highlightFirstTask();
             }
        });
}

function highlightFirstTask()
{
    if ($("#task-list > div").size()==0)
        return;

    var id = $("#task-list > div:first").attr('id').substring(10);
    highlightTask(id);
    scrollTask(id);
    
    /*for (var i in tasks)
    {
        if (typeof(tasks[i].done)!="undefined" && !tasks[i].done)
        {
            highlightTask(i);
            scrollTask(i);
            break;
        }
    }*/
}

function autocompleteAddress()
{

    $(this)
        .autocomplete({
         //This bit uses the geocoder to fetch address values
          autoFocus: true,
          source: function(request, response) {
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
            })
          },
          //This bit is executed upon selection of an address
          select: function(event, ui) {
              
            if (typeof(EDITING)!="undefined" && EDITING)
            {
                $('#edit-'+EDITING+' .location').val(ui.item.formatted_address);

                var location = new google.maps.LatLng(ui.item.latitude, ui.item.longitude);
                
                if (typeof(tasks[EDITING].marker) == "undefined")
                {
                    tasks[EDITING]['marker'] = createMarker(EDITING,location.lat(),location.lng());
                    tasks[EDITING].marker.setAnimation(google.maps.Animation.DROP);
                    tasks[EDITING].marker.setIcon(new google.maps.MarkerImage("/static/webapp/img/marcador03.png"));
                    tasks[EDITING].marker.setVisible(true);
                    tasks[EDITING].marker.setDraggable(true);
                }
                else
                    tasks[EDITING].marker.setPosition(location);
                    
                map.setCenter(location);
            }
          }
        });
}

function prepareAlerts(arr)
{
    ret = {};
    for (var i in arr)
    {
        var id = arr[i].id+''; // convert in str
        ret[id] = {};
        for (var v in arr[i])
        {
            ret[id][v] = arr[i][v];
        }

        // create a marker for each task
        if (!ret[id].done)
            ret[id]['marker'] = createMarker(id,ret[id].x,ret[id].y);
    }
    
    return ret;
}

function createMarker(task,x,y)
{
    var icon = new google.maps.MarkerImage("/static/webapp/img/marcador02.png");
    var myLatlng = new google.maps.LatLng(x,y);
    
    var marker = new google.maps.Marker({
        map: map,
        draggable: false,
        position: myLatlng,
        icon: icon
    });

    marker.task = task;

    // set marker events
    google.maps.event.addListener(marker, 'click', function(){highlightTask(this.task,false);});
    google.maps.event.addListener(marker, 'dblclick', function(){editTask(this.task);});
    google.maps.event.addListener(marker, 'dragend', function(){updateAddressByMarker(this);});
    
    return marker;
}

function addTask()
{
    var newid = "new"+newTasks;
    
    
    var x,y;
    var p = map.getCenter();
    x = p.lat();
    y = p.lng();
    
    // default task info
    tasks[newid] = {task:newid,description:"",name:gettext("New task"),distance:"0",x:x,y:y,address:""};

    // by default a new tasks hasn't id

    $( "#taskTemplate" ).tmpl( tasks[newid] ).appendTo( "#task-list" );
    $("#name-"+newid).disableSelection();
    editTask(newid);
    $('#edit-'+newid+' .location').geoaddress();
    
    newTasks++;
}

function closeEdit(task)
{
    $("#name-"+task+" span").text(tasks[task].name);
    $("#name-"+task).show();
    $("#edit-"+task).css("display","none");
    
    if (EDITING==task)
    {
        EDITING = null;
    }
    
    if (typeof(tasks[task].marker)!="undefined")
    {
        tasks[task].marker.setDraggable(false);
    }
}

function cancelEdit(task)
{
    // was new?
    if (typeof(tasks[task].id) == "undefined")
    {
        removeTask(task);
        EDITING = null;
    }
    else
    {
        // get the old data
        $('#edit-'+task+' .task-name').val(tasks[task].name);
        $('#edit-'+task+' textarea').val(tasks[task].description);
        //$('#edit-'+task+' .location').val(tasks[task].location);
        $('#edit-'+task+' .radius').val(tasks[task].location);
        
        if (typeof(tasks[task].marker) != "undefined" && typeof(tasks[task].x) != "undefined" && (tasks[task].x!=0 || tasks[task].y!=0) )
        {
            var location = new google.maps.LatLng(tasks[task].x, tasks[task].y);
            tasks[task].marker.setPosition(location);
        }

        closeEdit(task);
    }
}

function saveTask(task)
{
    if (typeof(tasks[task]) == "undefined")
        tasks[task] = {};
    
    if ($('#edit-'+task).is(":visible"))
    {
        // get the data from the form
        tasks[task].name = $('#edit-'+task+' .task-name').val();
        tasks[task].description = $('#edit-'+task+' textarea').val();
        tasks[task].address = $('#edit-'+task+' .location').val();
        tasks[task].distance = $('#edit-'+task+' .radius').val();
        closeEdit(task);
    }
    
    if (typeof(tasks[task].marker)!="undefined")
    {
        tasks[task].x = tasks[task].marker.getPosition().lat();
        tasks[task].y = tasks[task].marker.getPosition().lng();
    }
    
    var data = {
            name: tasks[task].name,
            description: tasks[task].description,
            address: tasks[task].address,
            location: tasks[task].x+','+tasks[task].y,
            distance: tasks[task].distance
        }
    
    
    if (tasks[task].done)
        data['done'] = true;
    
    if (typeof(tasks[task].id) != "undefined")
        data['id'] = tasks[task].id;
    
    // ajax
    $.ajax({
    url: AJAX_URL+"add/reminder/",
    type:"post",
    async: true,
    dataType: "json",
    data: data,
    success: function(data){ 
        
            // save the id, new or not
            tasks[task]['id'] = data.id;
            
            var idx = notsaved.indexOf(task);
            if (idx>=0)
                notsaved.splice(idx,1);
         },
    error: function() { 
        
        // save in not saved vector
        if (notsaved.indexOf(task)<0)
            notsaved.push(task);
        
        }
    });
    
}

function saveNotSaved()
{
    
    if (notsaved.length==0)
        return;
    

    //tosend = [];
    //todel = []
    var saved = [];
    for (var i in notsaved)
    {
        var task = notsaved[i];
        
        if (typeof(tasks[task])!="undefined")
        {
            var data = {
                    name: tasks[task].name,
                    description: tasks[task].description,
                    address: tasks[task].address,
                    location: tasks[task].x+','+tasks[task].y,
                    distance: tasks[task].distance
                };
            
            if (typeof(tasks[task].id) != "undefined")
                data['id'] = tasks[task].id;
            
            // ajax
            $.ajax({
                url: AJAX_URL+"add/reminder/",
                type:"post",
                async: false,
                dataType: "json",
                data: data,
                success: function(data){ 
        
                    // save the id, new or not
                    tasks[task]['id'] = data.id;
                    
                    saved.push(task);
                    
                 }
            });
            
            //tosend.push( data );
        }
        else
            $.ajax({
                url: AJAX_URL+"delete/reminder/",
                type:"post",
                async: false,
                dataType: "json",
                data: {id:task},
                success: function(data){ 
        
                    // save the id, new or not
                    //tasks[task]['id'] = data.id;
                    
                    saved.push(task);
                 }
            });
    }
    

    // remove the saved tasks
    for (var i in saved)
    {
        delete notsaved[saved[i]];
    }
    
}

function removeTask(task)
{
    if (typeof(tasks[task].id)!="undefined")    
        if (!confirm(gettext("Sure you want to delete the task")+" '"+tasks[task].name+"'?"))
            return;
    
    $('#full-task-'+task).remove();
    
    
    if (typeof(tasks[task].id)!="undefined")
        // remove of server
        $.ajax({
            url: AJAX_URL+"delete/reminder/",
            type:"post",
            async: true,
            dataType: "json",
            data: {id:tasks[task].id},
            error: function() { 
                
                // save in not saved vector
                if (notsaved.indexOf(tasks[task].id)<0)
                    notsaved.push(tasks[task].id);
                
                }
        });
    
    // remove from memory or cache
    tasks[task].marker.setMap(null);
    delete tasks.task;

    if (!getHighlightTask());
        highlightFirstTask();
}

function highlightTask(task,movetotask)
{
    // default move the map
    var move = movetotask;
    if (typeof(move) == "undefined")
        move = true;
    
    disableAllHightlight();

    if (typeof(tasks[task].marker)!="undefined")
    {
        tasks[task].marker.setVisible(true);
        tasks[task].marker.setIcon(new google.maps.MarkerImage("/static/webapp/img/marcador03.png"));
        
        if (move)
        {
            var pos = tasks[task].marker.getPosition();
            moveTo(pos.lat(),pos.lng());
        }
    }

    if (!movetotask) // from the marker
    {
        //highlightMultiMarker(task);
        scrollTask(task);
    }

    $("#name-"+task+" span").css('background-color','');
    $('#name-'+task+' span,#edit-'+task).addClass('task-highlight');

    if ($("#edit-"+task).is(":visible"))
    {
        scrollTask(task);
        EDITING=task;
    }


    // tooltip manager
    var multichicken = $('#show-all input[type=checkbox]').is(":checked");
    if (multichicken)
    {
        if (typeof(infowindow)!="undefined")
        {
            infowindow.setMap(null);
            delete infowindow;
        }
        
        var content = '<div id="tooltip">'+
            '<h1>'+tasks[task].name+'</h1>'+
            '<h3>'+tasks[task].address+'</h3>'+
            '<hr/><p>'+tasks[task].description+'</p>'+
            '</div>';
        
        infowindow = new google.maps.InfoWindow({
            content: content
        });
        
        infowindow.open(map,tasks[task].marker);
    }

}

function disableAllHightlight()
{
    $('.task-highlight').removeClass('task-highlight');
    for (var task in tasks)
    {
        var multichicken = $('#show-all input[type=checkbox]').is(":checked");
        if (typeof(tasks[task].marker)!="undefined")
        {
            tasks[task].marker.setIcon(new google.maps.MarkerImage("/static/webapp/img/marcador02.png"));
            
            if (!multichicken)
                tasks[task].marker.setVisible(false);
        }
    }
}
    
function editTask(task)
{
    EDITING=task;
    if (typeof(tasks[task].marker)!="undefined")
    {
        tasks[task].marker.setDraggable(true);
        tasks[task].marker.setVisible(true);
    }
    
    if (typeof(infowindow)!="undefined")
    {
        infowindow.setMap(null);
        delete infowindow;
    }
    
    toggleShowAll(false);
    highlightTask(task);
    $("#name-"+task).hide();
    $("#edit-"+task).css("display","block");
    
    scrollTask(task);
    
    hideButtons(task);
}

function scrollTask(task)
{
    var offset, toscroll;
        
    //if ($('#edit-'+task).is(":visible"))
        //toscroll = $('#edit-'+task);
    //else
    toscroll = $('#name-'+task);
        
    offset = toscroll.offset().top;
    
    $("html,body").animate( {scrollTop: offset}, "slow" );
    
    /*
    // to down
    if (offset<$('#task-list').offset().top)
    {
        $("html,body").animate( {scrollTop: offset}, "slow" );
    }
    else
    {
        // to top
        if ( offset+toscroll.height() > $('#task-list').offset().top + $(window).height() )
        {
            $("html,body").animate( {scrollTop: offset}, "slow" );
            //$("html,body").animate( {scrollTop: (offset-$('#task-list').offset().top + $(window).height()) }, "slow" );
        }
    }*/
}

function showButtons(task)
{
    if (!$("#name-"+task).is(':visible'))
        return;
    
    $("#buttons-"+task).css('visibility','visible');
    
    //if (!$("#name-"+task+" span").hasClass("task-highlight"))
        $("#name-"+task+" span").css('background-color','#EBEBEB');
}

function hideButtons(task)
{
    $("#buttons-"+task).css('visibility','hidden');
    $("#name-"+task+" span").css('background-color','');
}

function moveTo(x,y)
{
    var point = new google.maps.LatLng(x, y);
    map.panTo(point);
}

function loadGMaps() {
    var myLatlng = new google.maps.LatLng(defaultX,defaultY);
    var myOptions = {
        zoom: 17,
        //mapTypeId: 'satellite'
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.TOP_CENTER
        }
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    geocoder = new google.maps.Geocoder();
    
    
    var homeControlDiv = document.createElement('DIV');
    var homeControl = new HomeControl(homeControlDiv, map);
    
    var pointerDiv = document.createElement('DIV');
    var pointerControl = new PointerControl(pointerDiv, map);
    
        homeControlDiv.index = 2;
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(homeControlDiv);
    
    pointerDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(pointerDiv);
}

function disableAllEditing()
{
    for (var task in tasks)
    {
        if (typeof(tasks[task]) != "undefined")
        {
            $('#name-'+task).show();
            $('#edit-'+task).hide();
            
            if (typeof(tasks[task].marker) != "undefined")
            {
                tasks[task].marker.setDraggable(false);
            }
        }
    }
    
    EDITING = null;
}

function toggleShowAll(value)
{
    if (typeof(value)!="undefined")
        $('#show-all input[type=checkbox]').attr('checked',value);
    
    if ($('#show-all input[type=checkbox]').is(":checked"))
    {
        var high = getHighlightTask();
        
        disableAllHightlight();
        disableAllEditing();
        
        for (var task in tasks)
        {
            var icon = new google.maps.MarkerImage("/static/webapp/img/marcador02.png");
            if (typeof(tasks[task]) != "undefined" && typeof(tasks[task].marker) != "undefined")
            {
                tasks[task].marker.setVisible(true);
                tasks[task].marker.setIcon(icon);
                
            }
        }
        
        if (high)
            highlightTask(high);
    }
    else
    {
        
        for (var task in tasks)
        {
            if (typeof(tasks[task]) != "undefined" && typeof(tasks[task].marker) != "undefined")
            {

                // remove the markers
                tasks[task].marker.setVisible(false);
            }
        }
        
        // set the marker to the current position
        if (typeof(EDITING)=="undefined" || !EDITING)
        {
            var task = getHighlightTask();
            
            if (task && typeof(tasks[task]) != "undefined" && typeof(tasks[task].marker) != "undefined")
            {
                tasks[task].marker.setVisible(true);
                moveTo(tasks[task].x,tasks[task].y);
            }
        }
        
        if (typeof(infowindow)!="undefined")
        {
            infowindow.setMap(null);
            delete infowindow;
        }
    }
}

function getHighlightTask()
{
    if ($('.task-highlight').size()==0)
        return null;
    
    var id = $('.task-highlight[id^="edit"]').attr('id');
    
    return id.substr(5,id.length-5);

}

function highlightMultiMarker(task)
{
    var icon = new google.maps.MarkerImage("/static/webapp/img/marcador03.png");
    tasks[task].marker.setIcon(icon);
    tasks[task].infowindow.open(map,tasks[task].marker);
    
    icon = new google.maps.MarkerImage("/static/webapp/img/marcador02.png");
    for (var i in tasks)
    {
        if (typeof(tasks[i]) != "undefined" && i!=task && typeof(tasks[i].marker) != "undefined")
        {
            // change the icon
            tasks[i].marker.setIcon(icon);
            
            // close infowindow
            tasks[i].infowindow.close();
        }
    }
}

function updateAddressByMarker(marker)
{
    geocoder.geocode({'latLng': marker.getPosition()}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results && results[0]) {
          $('#edit-'+marker.task+' .location').val(results[0].formatted_address);
        }
      }
    });
}

// Not used
function getAddress(input,address)
{
    geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK)
        {
            /*map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
            map: map, 
            position: results[0].geometry.location
            });*/
            if (results.length>0)
            {
                var arr = [];
                for (i in results)
                {
                    arr.push(results[i].formatted_address);
                }
                
                $( input ).autocomplete({
                    source: arr
                });
            }
        }
    });
}

function doTask(task)
{
    $('#full-task-'+task).remove();
    
    var date = new Date();
    
    tasks[task]['done'] = true;
    tasks[task]['donedate'] = date.getDate()+MONTH[(date.getMonth()+1)].substring(0,3);
    
    saveTask(task);
    
    if (typeof(tasks[task].marker)!="undefined")
    {
        tasks[task].marker.setMap(null);
        delete tasks[task].marker;
    }
    
    $( "#doneTemplate" ).tmpl( tasks[task] ).prependTo( "#done-list" );
    
    $("#done-list li:first").effect("highlight", {}, 3000);
    
    if (!getHighlightTask())
        highlightFirstTask();
    
}

function undoTask(task)
{
    $('#done-task-'+task).remove();
    
    tasks[task]['done'] = false;
    
    saveTask(task);

    $( "#taskTemplate" ).tmpl( tasks[task] ).prependTo( "#task-list" );

    if (tasks[task].x!=0 || tasks[task].y!=0)
        tasks[task]['marker'] = createMarker(task,tasks[task].x,tasks[task].y);

    if (getHighlightTask())
    {
        if (!$('#show-all input[type=checkbox]').attr('checked'))
            if (typeof(tasks[task].marker)!="undefined")
                tasks[task].marker.setVisible(false);
    }
    else
        highlightTask(task);

    scrollTask(task);
    
    $("#name-"+task+" span").effect("highlight", {}, 3000);
    $("#name-"+task).disableSelection();
    $('#edit-'+task+' .location').geoaddress();
    
}

function setCurrentLocation()
{
    
    if (typeof(myPos)!="undefined" && myPos)
    {
        map.setCenter(new google.maps.LatLng(myPos[0],myPos[1]));
    }
    else
    if (navigator.geolocation) 
    {
        navigator.geolocation.getCurrentPosition( 
            function (position) {
                myPos = [position.coords.latitude,position.coords.longitude]
                map.setCenter(new google.maps.LatLng(position.coords.latitude,position.coords.longitude));
            }, 
            function (error) {  });
    }

}

function search()
{
    disableAllHightlight();
    
    var words = [];
    var rawwords = $('#search input').val().split(' ');
    
    for (var i in rawwords)
    {
        if (typeof(rawwords[i])=="string" && rawwords[i] != '' && words.indexOf(rawwords[i])<0)
            words.push(rawwords[i]);
        
    }
    
    // no words entered
    if (words.length==0)
    {
        for (var task in tasks)
        {
            $('#full-task-'+task+',#name-'+task).show();
            $('#edit-'+task).css("display","none");
            
        }
    }
    else
    {        
        var regexp=new RegExp("("+words.join('|')+")","im");
        
        for (var task in tasks)
        {
            $('#full-task-'+task).hide();
            $('#edit-'+task).css("display","none");
            
        }

        for (var task in tasks)
        {   
            if (task!="undefined" && !tasks[task].done && (tasks[task].name.search(regexp)>=0 || tasks[task].description.search(regexp)>=0) )
            {
                $('#full-task-'+task+',#name-'+task).show();
                $('#edit-'+task).css("display","none");
            }
        }
    }
}

jQuery.fn.extend({
        geoaddress : function()
        {
            this.each(autocompleteAddress);
        },
        disableSelection : function() { 
                this.each(function() { 
                        this.onselectstart = function() { return false; }; 
                        this.unselectable = "on"; 
                        jQuery(this).css('-moz-user-select', 'none'); 
                }); 
        } 
});

function HomeControl(controlDiv, map) {
 
  // Set CSS styles for the DIV containing the control
  // Setting padding to 5 px will offset the control
  // from the edge of the map
  controlDiv.style.padding = '5px';
 
  // Set CSS for the control border
  var controlUI = document.createElement('DIV');
  controlUI.style.backgroundColor = 'white';
  controlUI.style.borderStyle = 'solid';
  controlUI.style.borderWidth = '2px';
  controlUI.style.cursor = 'pointer';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Click to get the marker';
  controlDiv.appendChild(controlUI);
 
  // Set CSS for the control interior
  var controlText = document.createElement('DIV');
  controlText.style.fontFamily = '\'Helvetica Neue\',Arial,Helvetica,sans-serif';
  controlText.style.fontSize = '12px';
  controlText.style.paddingLeft = '4px';
  controlText.style.paddingRight = '4px';
  controlText.innerHTML = '<b>'+gettext("Get the chicken!")+'</b>';
  controlUI.appendChild(controlText);
 
  // Setup the click event listeners: simply set the map to
  google.maps.event.addDomListener(controlUI, 'click', getTheChicken);
  $(controlDiv).disableSelection();
 
}
function PointerControl(controlDiv, map) {
 
  // Set CSS styles for the DIV containing the control
  // Setting padding to 5 px will offset the control
  // from the edge of the map
  //controlDiv.style.padding = '1px';
 
  // Set CSS for the control border
  var controlUI = document.createElement('DIV');
  //controlUI.style.backgroundColor = 'white';
  //controlUI.style.borderStyle = 'solid';
  //controlUI.style.borderWidth = '2px';
  controlUI.style.cursor = 'pointer';
  controlUI.style.textAlign = 'center';
  controlUI.setAttribute('id', 'pointer');
  controlUI.title = 'Where Am I?';
  controlDiv.appendChild(controlUI);
 
  // Set CSS for the control interior
  var controlImg = document.createElement('img');
  controlImg.src="/static/webapp/img/mirilla.png";
  controlUI.appendChild(controlImg);
 
  // Setup the click event listeners: simply set the map to
  google.maps.event.addDomListener(controlUI, 'click', setCurrentLocation);
 
}

function cursorMove(e)
{
    alert(e.which);
    
    // down
    
    // up

}

function getTheChicken()
{
    if (typeof(EDITING)=="undefined" || !EDITING)
    {
        // create new task for editing
        addTask();
    }
    else
    {
        // move the current marker
        
        if (typeof(tasks[EDITING].marker)!="undefined")
        {
            tasks[EDITING].marker.setMap(null);
            delete tasks[EDITING].marker;
        }
    
    }
        
    var pos = map.getCenter();
    
    tasks[EDITING]['marker'] = createMarker(EDITING,pos.lat(),pos.lng());
    tasks[EDITING].marker.setIcon(new google.maps.MarkerImage("/static/webapp/img/marcador03.png"));
    tasks[EDITING].marker.setAnimation(google.maps.Animation.DROP);
    tasks[EDITING].marker.setDraggable(true);
    tasks[EDITING].marker.setFlat(false);
    updateAddressByMarker(tasks[EDITING].marker);
    //tasks[EDITING].marker.setShadow("/static/webapp/img/marcador02.png");
    
}

function stopPropagation(e)
{
    e= e || event;
    e.stopPropagation ? e.stopPropagation() : e.cancelBubble=true;
}

if(!Array.indexOf){
   Array.prototype.indexOf = function(obj){
      for(var i=0; i<this.length; i++){
         if(this[i]==obj){
            return i;
         }
      }
      return -1;
   }
}

// try to get the locatization and add the task there
// NOT USED
function startAddTask()
{
    if (typeof(myPos)!="undefined" && myPos)
    {
        continueAddTask(myPos[0],myPos[1]);
    }
    else
    if (navigator.geolocation) 
    {
        navigator.geolocation.getCurrentPosition( 
            function (position) {
                myPos = [position.coords.latitude,position.coords.longitude]
                continueAddTask(position.coords.latitude,position.coords.longitude);
            }, 
            function (error) { continueAddTask(defaultX,defaultY); });
    }
    else
        continueAddTask(defaultX,defaultY);
}

// callback after get the current location
// NOT USED
function continueAddTask(x,y)
{
    var newid = "new"+newTasks;
    
    // default task info
    tasks[newid] = {description:"",name:gettext("New task"),distance:"0",x:x,y:y,address:""};

    $( "#taskTemplate" ).tmpl( {id:newid,description:"",name:gettext("New task"),distance:"0",x:x,y:y,address:""} ).appendTo( "#task-list" );
    $("#name-"+newid).disableSelection();
    editTask(newid);
    $('#edit-'+newid+' .location').geoaddress();
    
    newTasks++;
}
