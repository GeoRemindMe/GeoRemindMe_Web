$(document).ready(function(){
    //if(typeof(resizeIframe)!="undefined")
        //if (typeof resizeIframe != "undefined") resizeIframe();
    setTimelineBehaviour();
            
        GRM.updateTabCounters();
        
        if($("#activity").length!=0){
            $('.load-more').attr("type","activity");
        }else if($("#public-profile").length!=0){
            $('.load-more').attr("type","timeline");
        }else if($("#notifications").length!=0){
            $('.load-more').attr("type","notifications");
        }
    

        
        //Adding behaviour to tab content
        $('#tabMenu li').not('.clear-box').click(function(){
            tab_id=$('#tabMenu li.active').attr('id')
            $('#'+tab_id+'_content').addClass('hidden');
            $('#tabMenu li.active').removeClass('active');
            
            tab_id=$(this).attr('id')
            $('#'+tab_id+'_content').removeClass('hidden');
            $(this).addClass('active');
        })
        
        $('#filter-suggestions').click(function(){
            $(':regex(class,(msg-300|msg-303))').show();
            //Oculto todos aquellos que no son sugerencias
            $('#chronology li').not('.msg-300').not('.msg-303').not('.suggestion-comment').hide();
        });
        
        $('#filter-lists').click(function(){
            $(':regex(class,(msg-350|msg-353))').show();
            //Oculto todos aquellos que no son sugerencias
            $('#chronology li').not('.msg-350').not('.msg-353').not('.suggestion-comment').hide();
        });
        
        $('#filter-likes').click(function(){
            $(':regex(class,(msg-125|msg-305|msg-355))').show();
            //Ocultamos aquellos que no son 125 ni 355
            $('#chronology li').not('.msg-125').not('.msg-305').not('.msg-355').hide()  
        });
            
        $('#filter-comments').click(function(){
            $(':regex(class,(msg-120|msg-121))').show();
            //Oculto todos aquellos que no son sugerencias
            $('#chronology li').not('.msg-120').not('.msg-121').hide();
        });
        
        $('#no-filter').click(function(){
            //Muestro todos
            $('#chronology li:not(.suggestion-comment)').show();
        });
        
        //$('.user-picture').each(function(i,elem){
            
        //    (new Image()).src = $(elem).attr('src')
        //})
        
        //Cargar más elementos del Timeline
        $(".load-more").loadTimeline({
                //'query_id':$(this).attr('value'),
                container:'#chronology'
            });
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
            //if(typeof(resizeIframe)!="undefined")
                //if (typeof resizeIframe != "undefined") resizeIframe();
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
            var width=$(this).parent().parent().width()-45;
            $(this).css('width',width+'px');
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
    var width=$(obj).parent().parent().width()-10;
    $(obj).css('width',width+'px');
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
    GRM.wait();
    $.ajax({
        type: "POST",
        url: "/ajax/add/comment/"+elemType+"/",
        dataType:'json',
        data: {
            instance_id:element_id,
            msg:msg
        },
        complete: function() { GRM.nowait();},
        success: function(response){

            //console.log(response)
            textarea.parent()
            c=$('#commentTemplate').tmpl(response).appendTo('#commentList-'+element_id);
            c.find(".like-dislike").like();
            c.find(".removable").removable();
            //resetInput(textarea);
            //if(typeof(resizeIframe)!="undefined")
                //if (typeof resizeIframe != "undefined") resizeIframe();
        },
        error:{
        }
    });
}

function suggestionProposal(elem,action,timeline_id){
    
    //si se envia timeline_id por POST, se modificara ese timeline (se aceptara o rechazara la sugerencia)
    //status puede ser 0: nada 1: aceptada, 2: rechazada
    var data={};
    if(action=="accept")
        data['status']=1;
    else
        data['status']=2;
    data['timeline_id']=timeline_id;
    asd=elem;
    data["csrfmiddlewaretoken"]=$(elem).parent().find('input').val();
    
    GRM.wait();
    $.ajax({
        type: "POST",
        url: url["suggest_suggestion"],
        dataType:'json',
        data:data,
        context:$(this),
        complete: function() { GRM.nowait();},
        success: function(data){
            if(data==true){
                if(action=="accept")
                    $(elem).parent().empty().html(gettext("La propuesta ha sido aceptada"));
                else
                    $(elem).parent().empty().html(gettext("La propuesta ha sido rechazada"));
            }
            //~ $(elem).parent()
            //~ console.log(data);
        }
    })
}
