var lastUID=null;

$(document).ready(function(){
    //TEMPLATES
    if($('#followTemplate').length==0){
        var temp =  '<script id="followTemplate" type="text/x-jquery-tmpl">\
                        <span  onclick="javascript:follow(\'follow\',${id})"><a href="javascript:void(0)" class="no-following">'+gettext("Seguir")+'</a></span>\
                    </script>\
                    <script id="unfollowTemplate" type="text/x-jquery-tmpl">\
                        <span  onclick="javascript:follow(\'unfollow\',${id})"><a href="javascript:void(0)" class="following">'+gettext("Siguiendo")+'</a></span>\
                    </script>'
        $('#templates').append(temp).ready()
        
    }

    /* Preload Spinning icon if it is the first time */
    var cache = [];
    var cacheImage = document.createElement('img');
    cacheImage.src ="/static/facebookApp/img/spinning-icons/wait16trans.gif";
    cache.push(cacheImage);
});

function follow(action,userid,username) {      
    var data = { "userid" : userid};
    
    if(username!=null)
        data["username"]=username;
    if(action=='follow')
        var url = '/ajax/add/following/'
    else
        var url = '/ajax/delete/following/'
    
    $("#following_state_"+userid).children().text(gettext("Enviado..."))
    $('#following_state_'+userid).removeClass('following-state');
    $("#following_state_"+userid).children().addClass("waiting")
    $.ajax({
        type: 'POST',
        url: url,
        context: data,
        data: data,
        complete: function(msg){
            //console.log(data)
            $("#following_state_"+userid).children().remove()
            $("#following_state_"+userid).children().removeClass("waiting")
            if(action=='follow' && data && msg.status==200){
                $("#unfollowTemplate").tmpl( {id:userid} ).appendTo( "#following_state_"+userid );
            
                $('#following_state_'+userid).addClass('following-state');
            }
            else{
                $("#followTemplate").tmpl( {id:userid} ).appendTo( "#following_state_"+userid );
                
                $('#following_state_'+userid).removeClass('following-state');
            }
            
        }
    });
}
