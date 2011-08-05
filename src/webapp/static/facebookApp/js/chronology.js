$(document).ready(function(){
    resizeIframe();
    
    GRM.init();

    $('.show-all-comments').click(function(){
        //Después de mostrar los comentarios ocultamos el botón
        $(this).parent().find('.long-list').slideDown('fast', function(){
            resizeIframe();
            $(this).parentsUntil('.suggestion-element').parent().find('.show-all-comments').remove();
            
        });
        
    });

    $('#chronology li').hover(
        function(){$(this).find('.action-bar').css('visibility','visible')},
        function(){$(this).find('.action-bar').css('visibility','hidden')}
    )
    
    //Al pulsar en comentar ponemos el foco en el input
    $('.focusInput').click(function(){
        var commentBox=$(this).parentsUntil('li').parent().find('.input-box')
        
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
     console.log("elemType="+  elemType);         
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

function updateTabCounters(){
    
    $('#all-counter').text($('#chronology li').length);
    $('#suggestions-counter').text($('#chronology li.msg-300').length);
    $('#lists-counter').text($('#chronology li.msg-350').length);
    $('#likes-counter').text($(':regex(class,(msg-125|msg-305))').length);
    $('#comments-counter').text($(':regex(class,(msg-120|msg-121))').length);
}
