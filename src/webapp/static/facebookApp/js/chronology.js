$(document).ready(function(){
    resizeIframe();
    $(".like-dislike").like();
    
    initRemovable();

    $('.show-all-comments').click(function(){
        //Después de mostrar los comentarios ocultamos el botón
        $(this).parent().find('.long-list').slideDown('fast', function(){
            resizeIframe();
            $(this).parentsUntil('.suggestion-element').parent().find('.show-all-comments').remove();
            
        });
        
    });


    //Al pulsar en comentar ponemos el foco en el input
    $('.focusInput').click(function(){
        var commentBox=$(this).parentsUntil('.suggestion-element').parent().find('.input-box')
        
        if(commentBox.hasClass('hidden'))
            commentBox.removeClass('hidden');
        
        commentBox.find('textarea').focus()
    });
    
    setCommentFormsBehaviour()
});


function setCommentFormsBehaviour(){
    
    $('.commentForm').find("textarea").focus(function(){
        $(this).css('color','black');
        if($(this).attr('empty')=="true"){
            $(this).css('width','430px');
            $(this).css('font-style','normal');
            $(this).css('font-size','1.1em');
            $(this).parent().parent().find("img").removeClass('hidden');
            //Guardamos y machamos el mensaje
            $(this).attr('msg',$(this).text())
            $(this).text("");
        }
    })
    
    $('.commentForm').find("textarea").blur(function(){
        if($(this).val()=="")
            $(this).attr('empty',"true");
        
        if($(this).attr('empty')=="true")
            resetInput(this)
        
    })
    
    $('.commentForm').find("textarea").keyup(function(e) {
        e.preventDefault();
        if(e.keyCode == 13) {
            //If keypress==enter -> submit
            
            
            suggestion_id=$(this).parent().parent().parent().attr('value')
            sendComment2($(this),suggestion_id);
            
            $(this).val("");
            $(this).blur();
            resetInput(this)
            
            
        }else{
            var height=(parseInt($(this).val().length/55)+1)*1.2;
            if($(this).css('height')!=height)
                $(this).css('height',height+'em');
            if($(this).val().length>0)
                $(this).attr('empty',"false")
            else
                $(this).attr('empty',"true")
        }
    });
}

function resetInput(obj){
    
    $(obj).css('width','470px');
    $(obj).css('color','#999');
    $(obj).css('font-style','italic');
    $(obj).css('font-size','0.9em');
    $(obj).parent().parent().find("img").addClass('hidden');
    
    //Reestablecemos el mensaje
    $(obj).attr('empty',"true")
    $(obj).text($(obj).attr('msg'));
    
    $(obj).focusout()
}
function vote(type,obj,value){
    var element_id=obj.attr('value')
    
    $.ajax({
            type: "POST",
            url: "/ajax/vote/"+type+"/",
            data: {
                instance_id:element_id,
                puntuation: value,
            },
            dataType:'json',
            success: function(msg){
                //console.log(msg)
                //if(msg!=false){
                    action=obj.attr('class')
                    obj.addClass('hidden')
                    
                    if(action=="LikeComment")
                        obj.parent().find(".dontLikeComment").removeClass('hidden')
                    else if (action=="dontLikeComment")
                        obj.parent().find(".LikeComment").removeClass('hidden')
                        
                    if(action=="LikeSuggestion")
                        obj.parent().find(".dontLikeSuggestion").removeClass('hidden')
                    else if (action=="dontLikeSuggestion")
                        obj.parent().find(".LikeSuggestion").removeClass('hidden')
                //}
            },
            error:function(){
            }
            
        });   
}





function sendComment2(textarea,suggestion_id){
    if(textarea.val()=="")
        return false;
    else{
        msg=textarea.val();
        msg=msg.substring(0,msg.length-1);
    }
                
    $.ajax({
        type: "POST",
        url: "/ajax/add/comment/event/",
        dataType:'json',
        data: {
            instance_id:suggestion_id,
            msg:msg
        },
        success: function(response){

            //console.log(response)
            textarea.parent()
            c=$('#commentTemplate').tmpl(response).appendTo('#commentList-'+suggestion_id);
            c.find(".like-dislike").like();
            //resetInput(textarea);
            initRemovable();
            resizeIframe();
        },
        error:{
        }
    });
}
