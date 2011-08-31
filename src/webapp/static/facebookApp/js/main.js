Config = null;

$(document).ready(function() {
    $('.help-txt').dialog({
            autoOpen:false,
			resizable: false,
            buttons: [{
                    text: "Cerrar",
                    click: function() { $(this).dialog("close"); }
                }],
            draggable: false,
			width:560,
            position: ['right', 45]
    });
    
       
    $('.help-icon img').click(function(){
        $('#'+$(this).attr('id')+'-text').dialog("open");
    })
});

function facebookInit(config) {
  Config = config;

  FB.init({
    appId: Config.appId,
    xfbml: true,
    cookie : true, // enable cookies to allow the server to access the session
  });
  FB.Event.subscribe('auth.sessionChange', handleSessionChange);

  //FB.Canvas.setAutoResize();
  if (typeof resizeIframe != "undefined") resizeIframe();
  // ensure we're always running on apps.facebook.com
  // if we are opening http://localhost:8080/fb/ or
  // georemindme.appspot.com/fb we will be redirected
  //~ if (window == top) { goHome(); }
}

function handleSessionChange(response) {
    //This checks if the user have changed the session and if it
    //is incoherent or there ir no session we move to home
    if ((Config.userIdOnServer && !response.session) ||
        Config.userIdOnServer != response.session.uid) 
    {
        goHome();
    }
}

function goHome() {
    top.location = 'http://apps.facebook.com/' + Config.canvasName + '/';
}

function resizeIframe() {
    var tam=$('#right-col').height(); //Get height of the iframe
    console.log("Entro y tam="+tam);
    //~ tam=tam+250;
    //~ console.log('Resize to '+tam);
    FB.Canvas.setSize({ height: tam });
    $('#right-col').css('min-height',tam+'px');
    
}


jQuery.expr[':'].regex = function(elem, index, match) {
    var matchParams = match[3].split(','),
        validLabels = /^(data|css):/,
        attr = {
            method: matchParams[0].match(validLabels) ?
                        matchParams[0].split(':')[0] : 'attr',
            property: matchParams.shift().replace(validLabels,'')
        },
        regexFlags = 'ig',
        regex = new RegExp(matchParams.join('').replace(/^\s+|\s+$/g,''), regexFlags);
    return regex.test(jQuery(elem)[attr.method](attr.property));
}
