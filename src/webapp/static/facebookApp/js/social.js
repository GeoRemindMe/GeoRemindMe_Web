var lastUID=null;
function follow(action,userid,username) {
    
    //~ alert($('#followTemplate').length)
    //TEMPLATES
    if($('#followTemplate').length==0){
        var temp =  '<script id="followTemplate" type="text/x-jquery-tmpl">\
                        <span  onclick="javascript:follow(\'follow\',${id})"><a href="#">Seguir</a></span>\
                    </script>\
                    <script id="unfollowTemplate" type="text/x-jquery-tmpl">\
                        <span  onclick="javascript:follow(\'unfollow\',${id})"><a href="#">Dejar de seguir</a></span>\
                    </script>'
        $('#templates').append(temp).ready()
    }
    
    
    var data = { "userid" : userid};
    lastUID=userid;
    if(username!=null)
        data["username"]=username;
    if(action=='follow')
        var url = 'http://localhost:8080/ajax/add/following/'
    else
        var url = 'http://localhost:8080/ajax/delete/following/'
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(data,userid){
            //console.log(data)
            $("#following_state_"+lastUID).children().remove()
            if(action=='follow' && data)
                $("#unfollowTemplate").tmpl( {id:lastUID} ).appendTo( "#following_state_"+lastUID );
            else if (action=='unfollow' && data)
                $("#followTemplate").tmpl( {id:lastUID} ).appendTo( "#following_state_"+lastUID );
            }
    });
}
