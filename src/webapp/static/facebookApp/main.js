Config = null;

function facebookInit(config) {
  Config = config;

  FB.init({
    appId: Config.appId,
    xfbml: true,
    cookie : true, // enable cookies to allow the server to access the session
    //~ channelUrl:
      //~ window.location.protocol + '//' + window.location.host + '/channel.html'
  });
  FB.Event.subscribe('auth.sessionChange', handleSessionChange);
  //~ FB.Event.subscribe('auth.logout', function() {
      //~ alert("yepah2");
      //~ FB.logout(function(response) {
          //~ alert("yepah");
          //~ });
    //~ });
  FB.Canvas.setAutoResize();

  // ensure we're always running on apps.facebook.com
  // if we are opening http://localhost:8080/fb/ or
  // georemindme.appspot.com/fb we will be redirected
  if (window == top) { goHome(); }
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
  top.location = 'http://apps.facebook.com/' + Config.canvasName + '/dashboard/';
}

function publishRun(title) {
  FB.ui({
    method: 'stream.publish',
    attachment: {
      name: title,
      caption: "I'm running!",
      media: [{
        type: 'image',
        href: 'http://runwithfriends.appspot.com/',
        src: 'http://runwithfriends.appspot.com/splash.jpg'
      }]
    },
    action_links: [{
      text: 'Join the Run',
      href: 'http://runwithfriends.appspot.com/'
    }],
    user_message_prompt: 'Tell your friends about the run:'
  });
}
