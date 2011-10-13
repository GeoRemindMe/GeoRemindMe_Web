function loadPanoramioPhotos(latlngStr){
    //Load Panoramios photos
    //------------------------------------------
    var ne={}
    var sw={}

    ne['lat']=parseFloat(latlngStr[0])+0.003004;
    ne['lng']=parseFloat(latlngStr[1])+0.002604;

    sw['lat']=parseFloat(latlngStr[0])-0.000848;
    sw['lng']=parseFloat(latlngStr[1])-0.002609;

    var myRequest = new panoramio.PhotoRequest({
      'rect': {'sw': {'lat': sw['lat'], 'lng': sw['lng']}, 'ne': {'lat': ne['lat'], 'lng': ne['lng']}}
    });

    var myOptions = {
      'width': 270,
      'height': 180,
      'columns': 1,
      'rows': 1,
      'delay':2.5,
      'croppedPhotos': false,
    };

    var wapiblock = document.getElementById('panoramio-imgs');
    widget = new panoramio.PhotoListWidget(wapiblock, myRequest, myOptions);
    widget.setPosition(0);

    $('.panoramio-wapi-loaded-img-div,.panoramio-wapi-images,').css('background-color','#f9f9f9')
    $('.panoramio-wapi-tos').remove()


    panoramio.events.listen(widget, panoramio.events.EventType.PHOTO_CHANGED, function(){
        $('.panoramio-wapi-empty-img-div').remove()
    });

    panoramio.events.listen(widget, panoramio.events.EventType.PHOTO_CLICKED, function(event){
        //console.log('Photo "' + event.getPhoto().getPhotoTitle() + '" was clicked')        
        //return false;
          
    });

    $('#panoramio-tos').append('<div class="panoramio-wapi-tos" style="color: black ! important; background-color: #f9f9f9 ! important;font-family:"lucida grande",tahoma,verdana,arial,sans-serif; font-size:10.8px;line-height:16.2px"><a target="_top" href="http://www.panoramio.com"><img src="/static/common/img/transparent.gif"></a><span>, '+gettext("los derechos de las fotos pertenecen a los autores")+'</span></div>');
    //------------------------------------------
}
