$(document).ready(function(){
    resizeIframe();
    setTimelineBehaviour();
    
    
    
});

function setTimelineBehaviour(page){
    
    if (typeof page == "undefined" )
        page='';
    else
        page='li[value="'+page+'"] ';
    
    $(page + ".like-dislike").like();
    $(page + ".remember-forget").remember();
    $(page + ".removable").removable(); 
    showHideActionBar(page);
    setCommentsBehaviour(page);
    markUnreadItems(page);
}
function markUnreadItems(page){
    var notifications=$('#chronology').attr('notifications');
    if(notifications!='undefined'){
        var i=0;
        var msgs;
        if(page=='')
            msgs=$('#chronology > li');
        else
            msgs=$('#chronology > '+page);

        while (notifications > 0 && i < 10){
            $(msgs[i]).addClass("unread-item")
            notifications--;
            i++;
        }
        $('#chronology').attr('notifications',notifications)
    }
}

function showHideActionBar(page){
    //Show and hide action-bar
    $('#chronology '+ page +' div.timeline-msg,#chronology '+ page +' li.suggestion-comment').hover(
        function(){$(this).find('.action-bar').css('visibility','visible')},
        function(){$(this).find('.action-bar').css('visibility','hidden')}
    )
}

function setCommentsBehaviour(page){
    
    $(page+'.show-all-comments').click(function(){
        //Después de mostrar los comentarios ocultamos el botón
        $(this).parent().find('.long-list').slideDown('fast', function(){
            resizeIframe();
            $(this).parentsUntil('.suggestion-element').parent().find('.show-all-comments').remove();
            
        });
    });
    
    //Al pulsar en comentar ponemos el foco en el input
    $(page+'.focusInput').click(function(){
        var commentBox=$(this).parentsUntil('li').parent().find('.input-box')
        
        if(commentBox.hasClass('hidden'))
            commentBox.removeClass('hidden');
        
        commentBox.find('textarea').focus()
    });
    
    setCommentFormsBehaviour(page);
}

function setCommentFormsBehaviour(page){
    
    $(page+'.commentForm').find("textarea").focus(function(){
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
    
    $(page+'.commentForm').find("textarea").blur(function(){
        if($(this).val()=="")
            $(this).attr('empty',"true");
        
        if($(this).attr('empty')=="true")
            resetInput(this)
        
    })
    
    $(page+'.commentForm').find("textarea").keyup(function(e) {
        e.preventDefault();
        if(e.keyCode == 13) {
            //If keypress==enter -> submit
            element_id=$(this).parent().parent().parent().attr('value')
            parents=$(this).parentsUntil("#chronology")
            liElement=parents[parents.length-1]
            
            if($(liElement).hasClass('msg-350'))
                sendComment2($(this),element_id,"list");
            else
                sendComment2($(this),element_id,"event");
            
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

function sendComment2(textarea,element_id,elemType){
    if(textarea.val()=="")
        return false;
    else{
        msg=textarea.val();
        msg=msg.substring(0,msg.length-1);
    }

    $.ajax({
        type: "POST",
        url: "/ajax/add/comment/"+elemType+"/",
        dataType:'json',
        data: {
            instance_id:element_id,
            msg:msg
        },
        success: function(response){

            //console.log(response)
            textarea.parent()
            c=$('#commentTemplate').tmpl(response).appendTo('#commentList-'+element_id);
            c.find(".like-dislike").like();
            c.find(".removable").removable();
            //resetInput(textarea);
            resizeIframe();
        },
        error:{
        }
    });
}

