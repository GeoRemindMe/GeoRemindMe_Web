Config = null;

function facebookInit(config) {
  Config = config;

  FB.init({
    appId: Config.appId,
    xfbml: true,
    cookie : true, // enable cookies to allow the server to access the session
  });
  FB.Event.subscribe('auth.sessionChange', handleSessionChange);

  FB.Canvas.setAutoResize();

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
