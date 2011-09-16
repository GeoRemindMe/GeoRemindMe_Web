Config = null;

$(document).ready(function() {
    
    var dialogSettings={
            autoOpen:false,
			resizable: false,
            buttons: [{
                    text: "Cerrar",
                    click: function() { $(this).dialog("close"); }
                }],
            draggable: false,
			width:560,
            
    }
    if(typeof($('#webapp'))=="undefined")
        dialogSettings['position'] = ['right', 45];
    else
        dialogSettings['position'] = ['top', 65];
        
    $('.help-txt').dialog(dialogSettings);
    
       
    $('.help-icon img').click(function(){
        $('#'+$(this).attr('id')+'-text').dialog("open");
    })
});

function facebookInit(config) {
  Config = config;

  FB.init(config);
  FB.Event.subscribe('auth.sessionChange', handleSessionChange);

  //FB.Canvas.setAutoResize();
  //if (typeof resizeIframe != "undefined") resizeIframe();
  // ensure we're always running on apps.facebook.com
  // if we are opening http://localhost:8080/fb/ or
  // georemindme.appspot.com/fb we will be redirected
  if (window == top && DEBUG_mode==false) { goHome(); }
}

function handleSessionChange(response) {
    tmp=response;
    console.log(tmp)
    console.log(Config.userIdOnServer);
    console.log(tmp.session);
    console.log(tmp.session.uid);
    //This checks if the user have changed the session and if it
    //is incoherent or there ir no session we move to home
    if ((Config.userIdOnServer && !response.session) ||
        Config.userIdOnServer != response.session.uid) 
    {
        //goHome();
    }
}

function goHome() {
    top.location = 'http://apps.facebook.com/' + Config.canvasName + '/';
}

function resizeIframe() {
    var tam=$('#right-col').height(); //Get height of the iframe
    //console.log("Entro y tam="+tam);
    //~ tam=tam+250;
    //~ console.log('Resize to '+tam);
    FB.Canvas.setSize({ height: tam });
    $('#right-col').css('min-height',tam+'px');
    
}
