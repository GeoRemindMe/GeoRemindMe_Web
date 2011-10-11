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
    
       
    //$('.help-icon img').click(function(){
    //    $('#'+$(this).attr('id')+'-text').dialog("open");
    //})
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
    if (window == top && DEBUG_mode==false) { 
        alert(gettext("No puedes entrar a esta URL sin estar en Facebook, procedemos a redireccionarte"));
        goHome(); 
    }
}

function handleSessionChange(response) {
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

function grmLogged(){
    if($.cookies.get('georemindme_session_cookie')!="undefined")
        return true;
    else
        return false;
}


function check_ext_perm(session,callback) {
    
    var permArray=permissions.split(",");
    var query = FB.Data.query('select '+permissions+' from permissions where uid='+ session.userID);
    query.wait(function(rows) {
        var has_all_perms=true;
        permArray=permissions.split(",");
        for(perm in permArray){
            if(rows[0][permArray[perm]]!=1){
                has_all_perms=false
                break;
            }
        }
        if(has_all_perms) {
            callback(true);
        } else {
            callback(false);
        }
    });
};

function hasPerms(response){
    check_ext_perm(response.authResponse, function(isworking) {
        //Comprobamos si tenemos permisos para la app de FB
       if(isworking) {
          //window.location="/fb/dashboard/"
          return true
       } else {
          return false;
       }
    });
}
function haveLinkedAccount(uid){
    if(uid==null)
        return false;
    else
        return true;
}
function areCookiesCoherent(grm_cookie,fb_cookie){
    $.cookies.get('georemindme_session_cookie');
}

function loginApp(){
    FB.login(function(response) {
        tmp=response
        if (response.authResponse) {
            FB.api('/me', function(response) {
                //Redireccionamos
            });
        } else {
            //~ console.log('User cancelled login or did not fully authorize.');
        }
    }, {scope: permissions});
}
