GRM = { common : {} };

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
            
            var id = $(this).attr('value'), url = (typeof $(this).attr('remember') != "undefined" )?"/ajax/delete/suggestion/follower/":"/ajax/add/suggestion/follower/";
            
            if (settings.progress_class)
                $(this).addClass(settings.progress_class);
            
            $.ajax({
                    type: "POST",
                    url: url,
                    data: {
                        eventid:id
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
            
            $.ajax({
                type: "POST",
                url: custom_url,
                data: data,
                dataType:'json',
                context:$(this),
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
                            updateTabCounters();
                    
                            
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
                    
                    $(container).empty();
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

GRM.sendComment = function(type,text,id,callback){
    
    if(text=="")
        return false;

    $.ajax({
        type: "POST",
        url: "/ajax/add/comment/"+type+"/",
        data: {
            instance_id:id,
            msg:text },
        dataType:'json',
        success: function(response){
            
            var message=$('#msg').val()
            $('#msg').val("")
            
            var c = $('#commentTemplate').tmpl(response).prependTo('#comment-list');
            
        
            c.find(".like-dislike").like();
            resizeIframe()
            
            if (typeof callback != "undefined")
                callback();
        }
    });

    return true;
}
    

jQuery.fn.like = GRM.like;
jQuery.fn.remember = GRM.remember;
jQuery.fn.removable = GRM.removable;

GRM.init = function() {
        $(".like-dislike").like();
        $(".remember-forget").remember(); //<-- Now on chronology (Debugging)
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
