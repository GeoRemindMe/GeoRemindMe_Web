GRM = { common : {}, autocomplete : {} };

GRM.common.token = "*****GRMtoken****";

GRM.common.extend = function(m, e){
    var e = e || this;
    for (var x in m) e[x] = m[x];
    return e;
};

GRM.common.get = function(s){
    if (typeof(s) == "string")
        return $(s);
    
    return s;
};

/*
    <span class="like-dislike" value="{{obj.instance.id}}" {% if obj.has_voted %}like="true"{%endif%} type="suggestion">
        <span class="dislike">
            <span class="hoverlink">Ya no me gusta</span> 
            <span class="text like-text increase">{{obj.vote_counter}}</span> personas
        </span>

        <span class="like">
            Me gusta
        </span>
    </span>
    
    $('.like-dislike').remember({like_class: "xxx", dislike_class: "xxx", progress_class: "xxx"});
*/
GRM.like = function(settings) {
    
    settings = jQuery.extend({
        like_class: null,
        dislike_class: null,
        progress_class: null        
    }, settings);
       
    return this.each(function(){

        // get init state
        var state = (typeof $(this).attr('like') != "undefined" );

        // auto-init classes
        if (state && settings.dislike_class)
            $(this).addClass(settings.dislike_class);
        if (!state && settings.like_class)
            $(this).addClass(settings.like_class);

        // auto-init show/hide
        if (state)
            $(this).find('.like').hide();
        else
            $(this).find('.dislike').hide();


        // counter incremental
        /*var inc = $(this).find('.increase');
        $.each(inc, function(index,item){
            $(item).text(parseInt($(item).text())+1);
        });*/
        
        $(this).click(function() {
            
            GRM.wait();
            
            var type = $(this).attr('type'), id = $(this).attr('value'), vote = (typeof $(this).attr('like') != "undefined" )?-1:1;
            
            if (settings.progress_class)
                $(this).addClass(settings.progress_class);
            
            $.ajax({
                    type: "POST",
                    url: "/ajax/vote/"+type+"/",
                    data: {
                        instance_id:id,
                        puntuation: vote
                    },
                    context: $(this),
                    success: function(data){
                        
                        // disliking
                        if (typeof $(this).attr('like') != "undefined" ) {
                            // send vote -1
                            $(this).find('.dislike').hide();
                            $(this).find('.like').show();
                            $(this).removeAttr("like");
                            
                            if (settings.dislike_class)
                                $(this).removeClass(settings.dislike_class);
                            
                            if (settings.like_class)
                                $(this).addClass(settings.like_class);
                                
                        }
                        
                        // liking
                        else {
                            // send vote +1
                            $(this).find('.like').hide();
                            $(this).find('.dislike').show();
                            $(this).attr("like","true");
                            
                            if (settings.like_class)
                                $(this).removeClass(settings.like_class);
                            
                            if (settings.dislike_class)
                                $(this).addClass(settings.dislike_class);
                            }
                            
                            $(this).find('.increase').text(data.votes);
                        
                    },
                    complete: function()
                    {
                        if (settings.progress_class)
                            $(this).removeClass(settings.progress_class);
                        
                        GRM.nowait();
                    }
                });
        });
    });
};

/*
    <span title="Guardar en favoritos"  class="remember-forget" value="{{obj.instance.id}}" {%if obj.user_follower%}remember="true"{%endif%}>
        <span class="remember">Guardar</span>
        <span class="forget">Guardado</span>
    </span>
    
    $('.remember-forget').remember({remember_class: "xxx", forget_class: "xxx", progress_class: "xxx"});
*/
GRM.remember = function(settings) {
    
    settings = jQuery.extend({
        remember_class: null,
        forget_class: null,
        progress_class: null        
    }, settings);
       
    return this.each(function(){

        // get init state
        var state = (typeof $(this).attr('remember') != "undefined" );

        // auto-init classes
        if (state && settings.forget_class)
            $(this).addClass(settings.forget_class);
        if (!state && settings.remember_class)
            $(this).addClass(settings.remember_class);

        // auto-init show/hide
        if (state)
            $(this).find('.remember').hide();
        else
            $(this).find('.forget').hide();

        $(this).click(function() {
            
            GRM.wait();
            
            //Primero comprobamos el tipo de mensaje
            var elemType;
            if ($(this).attr('type')=="list")
                elemType="list";
            else
                elemType="suggestion";
            var id = $(this).attr('value'), url = (typeof $(this).attr('remember') != "undefined" )?"/ajax/delete/"+elemType+"/follower/":"/ajax/add/"+elemType+"/follower/";
            
            
            
            if (settings.progress_class)
                $(this).addClass(settings.progress_class);
            
            $.ajax({
                    type: "POST",
                    url: url,
                    data: {
                        eventid:id,
                        list_id:id
                    },
                    context: $(this),
                    success: function(){
                        
                        // disliking
                        if (typeof $(this).attr('remember') != "undefined" ) {
                            // send vote -1
                            $(this).find('.forget').hide();
                            $(this).find('.remember').show();
                            $(this).removeAttr("remember");
                            
                            if (settings.forget_class)
                                $(this).removeClass(settings.forget_class);
                            
                            if (settings.remember_class)
                                $(this).addClass(settings.remember_class);
                                
                        }
                        
                        // liking
                        else {
                            // send vote +1
                            $(this).find('.remember').hide();
                            $(this).find('.forget').show();
                            $(this).attr("remember","true");
                            
                            if (settings.remember_class)
                                $(this).removeClass(settings.remember_class);
                            
                            if (settings.forget_class)
                                $(this).addClass(settings.forget_class);
                            }
                        
                    },
                    complete: function()
                    {
                        if (settings.progress_class)
                            $(this).removeClass(settings.progress_class);
                        
                        GRM.nowait();
                    }
                });
        });
    });
};

GRM.removable = function() {

    return this.each(function(){
        $(this).hide();
        
        var item = $(this);
        
        $(this).parent().hover(
            function(){item.show();},
            function(){item.hide();}
        );

        $(this).click(function(){
            var id = $(this).attr('value'), type = $(this).attr('type');
            
            var custom_url;
            if(type=="person")
                custom_url="/ajax/contacts/block/";
            else
                custom_url="/ajax/delete/"+type+"/";
            
            var data = { eventid:id,  comment_id:id, list_id:id, userid:id};
            GRM.wait();
            $.ajax({
                type: "POST",
                url: custom_url,
                data: data,
                dataType:'json',
                context:$(this),
                complete: function() { GRM.nowait();},
                success: function(msg){
                    
                    if(msg==true){

                        if (type=="comment"){
                            //Eliminamos el comentario
                            var preElem=$(this).parent().prev();
                            var posElem=$(this).parent().next();
                            //parentTree=elem.parentsUntil('.suggestion-element');
                            if(preElem.size()==0 && posElem.size()==0){
                                //Si al borrar el comentario ya no quedan más elementos
                                //Ocultamos la caja de comentarios
                                $(this).parent().parent().next().addClass('hidden');
                                
                            }
                            
                            $(this).parent().fadeOut('slow').remove();
                            
                        }else if(type=="suggestion" || type=="suggestion/list" || type=="person")
                            $(this).parent().parent().fadeOut('slow').remove()
                        
                        //Si estamos en chronology actualizamos los contadores de los tabs
                        if($('ul#chronology').length>0)
                            GRM.updateTabCounters();
                    
                            
                    }
                },
                error:function(){
                }
                
            });
        });

    });

}

GRM.loadPage = function(params){
    
            var page=params['page'];
            var container=params['container'];
            var url=params['url'];
            var template=params['template'];
            var data=params["data"];
            var total=params["total_pages"];
            var current_page = ( typeof $(container).attr('page') == 'undefined' )?1:parseInt($(container).attr('page'));
            
            if (page=='next')
                current_page++;
            else if(page=='prev' && current_page>1)
                current_page--;

            data['page'] = current_page;
            
            $.ajax({
                type: 'POST',
                url: url,
                data:data,
                success: function(data){
                    
                    $(container).attr("page",current_page);
                    
                    //$(container).empty();
                    $.each(data[1], function(index,suggestion){
                        $(template).tmpl( {element:suggestion} ).appendTo(container);
                    });

                    //Ocultamos los botones de siguiente y anterior si es necesario
                    if(current_page>1)
                        $('#prev-page').removeClass('hidden');
                    else
                        $('#prev-page').addClass('hidden');
                        
                    if(current_page<total)
                        $('#next-page').removeClass('hidden');
                    else
                        $('#next-page').addClass('hidden');
                }
            });
        }

GRM.loadTimeline = function(params){

            var container=params['container'];
            var url=params['url'];
            
            var data="query_id="+$(container).attr("value");
            $('.load-more').addClass("waiting");

            
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                success: function(data){
                    $('.load-more').removeClass("waiting");
                    if(data[1].length>0){
                        if(data[0].length==2)
                            $(container).attr("value",'["'+data[0][0]+'","'+data[0][1]+'"]');
                        else
                            $(container).attr("value",data[0]);
                        var nextPage=parseInt($(container).attr("page"))+1;
                        $(container).attr("page",nextPage);
                        
                        $.each(data[1], function(index,suggestion){
                            var temp=$(suggestion).appendTo(container);
                            //Anadimos el valor de la página para añadir comportamientos
                            $(temp).first().attr('value',nextPage);
                        });
                        
                        setTimelineBehaviour(nextPage);
                        
                        GRM.updateTabCounters();
                        
                        //Volvemos a filtrar la pestaña activa forzando evento click
                        $('#'+$('ul#tabMenu .active').attr('id')).click()
                        
                        
                    }
                    showMessage("Se han cargado "+data[1].length+" elementos nuevos","success");
                    if(data[1].length<10){
                        //Si no hay más datos ocultamos el boton de cargar más
                        $(".load-more").hide();
                    }
                }
            });
        }

GRM.sendComment = function(type,text,id,callback){
    
    if(text=="")
        return false;

    GRM.wait();

    $.ajax({
        type: "POST",
        url: "/ajax/add/comment/"+type+"/",
        data: {
            instance_id:id,
            msg:text },
        dataType:'json',
        complete: function() { GRM.nowait(); },
        success: function(response){
            
            var message=$('#msg').val()
            $('#msg').val("")
            
            var c = $('#commentTemplate').tmpl(response).prependTo('#comment-list');
            
        
            c.find(".like-dislike").like();
            c.find(".removable").removable();
            if (typeof resizeIframe != "undefined") resizeIframe();
            
            showMessage("El comentario ha sido añadido con éxito", "success")
            
            if (typeof callback != "undefined")
                callback();
        }
    });

    return true;
}

GRM.updateTabCounters = function(){
    //~ $('#all-counter').text('('+$('#chronology li').not('.comment-box li').length+')');
    $('#suggestions-counter').text('('+$(':regex(class,(msg-300|msg-303))').length+')');
    $('#lists-counter').text('('+$(':regex(class,(msg-350|msg-353))').length+')');
    $('#likes-counter').text('('+$(':regex(class,(msg-125|msg-305|msg-355))').length+')');
    $('#comments-counter').text('('+$(':regex(class,(msg-120|msg-121))').length+')');
}

GRM.wait = function() {
    if ($("#wait-mask").size()==0) {
        $("body").append("<div id='wait-mask' style='position:fixed;height:100%;width:100%;top:0px;left:0px;z-index:1000;cursor:wait;'></div>");
        }
    else {
        $("#wait-mask").show();
    }
}

GRM.nowait = function() {
    $("#wait-mask").hide();
}

GRM.search = function(str,containers,fields)
{    
    var words = [];
    var rawwords = str.split(' ');
    
    for (var i in rawwords)
    {
        if (typeof(rawwords[i])=="string" && rawwords[i] != '' && words.indexOf(rawwords[i])<0)
            words.push(rawwords[i]);
        
    }
    
    $(containers+" .expanded").hide();
    
    // no words entered
    if (words.length==0)
    {
        $(containers).not(".expanded").show();
    }
    else
    {        
        var regexp=new RegExp("("+words.join('|')+")","im");
        
        $.each($(containers),function(idx,item) {
            item = $(item);
            item.hide();
            for (var i=0;i<fields.length;i++) {
                    if (item.find(fields[i]).text().search(regexp)>=0) {
                            var id = "#"+item.attr('id');
                            $(id+","+id+' > *').not(".expanded").show();
                            break;
                        }
                }
            
            });
    }
}

GRM.common.checkemail = function(email) {
	var regexp  = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	
	return (regexp.test(email));				
}

GRM.autocomplete.frompoint = function() {
    
    }

GRM.autocomplete.topoint = function() {
    
    }

jQuery.fn.search = function(container,fields) {
    return this.each(function(){
        $(this).keyup(function(){GRM.search($(this).val(),  container, fields)});
    });
}

jQuery.fn.like = GRM.like;
jQuery.fn.remember = GRM.remember;
jQuery.fn.removable = GRM.removable;

GRM.init = function() {
        $(".like-dislike").like();
        $(".remember-forget").remember();
        $(".removable").removable();
    }

//$(document).ready(GRM.init);

jQuery.expr[':'].regex = function(elem, index, match) {
    var matchParams = match[3].split(','),
        validLabels = /^(data|css):/,
        attr = {
            method: matchParams[0].match(validLabels) ?
                        matchParams[0].split(':')[0] : 'attr',
            property: matchParams.shift().replace(validLabels,'')
        },
        regexFlags = 'ig',
        regex = new RegExp(matchParams.join('').replace(/^\s+|\s+$/g,''), regexFlags);
    return regex.test(jQuery(elem)[attr.method](attr.property));
}


function sendComment(btn,elemType,id) {
    if (GRM.sendComment(elemType,$('#msg').val(),id,function(){$(btn).text("Comentar");$(btn).removeClass("waiting");})){
        $(btn).text("Enviando")
        $(btn).addClass("waiting")
    }
}

function showMessage(txt,msgClass){
    if($('#notification-msg').css("display")=="none"){
        $('#notification-msg').html(txt)
        $('#notification-msg').addClass(msgClass)
        $('#notification-msg').fadeIn('slow').delay(3000).fadeOut('slow')
    }
}
'#id_name','#counter'
function setRemainingCharCounter(input,counter){
    $(input).keyup(function(){
        charLeft=140-$(input).val().length;
        $(counter).text(charLeft);
        if(charLeft<0)
            $(counter).css("color","red")
        if(charLeft>-1)
            $(counter).css("color","#777")
        
    })
    
    //$('#id_name').trigger('keyup');
}


