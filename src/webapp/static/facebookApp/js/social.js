var lastUID=null;

$(document).ready(function(){
        //TEMPLATES
    if($('#followTemplate').length==0){
        var temp =  '<script id="followTemplate" type="text/x-jquery-tmpl">\
                        <span  onclick="javascript:follow(\'follow\',${id})"><a href="#" class="no-following">Seguir</a></span>\
                    </script>\
                    <script id="unfollowTemplate" type="text/x-jquery-tmpl">\
                        <span  onclick="javascript:follow(\'unfollow\',${id})"><a href="#" class="following">Seguiendo</a></span>\
                    </script>'
        $('#templates').append(temp).ready()
        
    }

    /* Preload Spinning icon if it is the first time */
    var cacheImage = document.createElement('img');
    cacheImage.src ="/static/facebookApp/img/spinning-icons/wait16trans.gif";
    cache.push(cacheImage);
});

function follow(action,userid,username) {      
    var data = { "userid" : userid};
    
    if(username!=null)
        data["username"]=username;
    if(action=='follow')
        var url = 'http://localhost:8080/ajax/add/following/'
    else
        var url = 'http://localhost:8080/ajax/delete/following/'
    
    $("#following_state_"+userid).children().text("Enviado...")
    $('#following_state_'+userid).removeClass('following-state');
    $("#following_state_"+userid).children().addClass("waiting")
    $.ajax({
        type: 'POST',
        url: url,
        context: data,
        data: data,
        success: function(data){
            //console.log(data)
            $("#following_state_"+userid).children().remove()
            $("#following_state_"+userid).children().removeClass("waiting")
            if(action=='follow' && data){
                $("#unfollowTemplate").tmpl( {id:userid} ).appendTo( "#following_state_"+userid );
            
                $('#following_state_'+userid).addClass('following-state');
            }
            else if (action=='unfollow' && data){
                $("#followTemplate").tmpl( {id:userid} ).appendTo( "#following_state_"+userid );
                
                $('#following_state_'+userid).removeClass('following-state');
            }
            
        }
    });
}
