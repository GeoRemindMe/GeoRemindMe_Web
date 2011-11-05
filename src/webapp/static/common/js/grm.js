// Defino que submenus deben estar visibles cuando se pasa el mouse por encima            
hiConfig = {
    sensitivity: 2, // number = sensitivity threshold (must be 1 or higher)
    interval: 0, // number = milliseconds for onMouseOver polling interval
    timeout: 500, // number = milliseconds delay before onMouseOut
    over: function() {
        $(this).find('ul:first:hidden').css({visibility: "visible",display: "none"}).slideDown(400);
    },
    out: function() {
        
        var inputVisibility=$('#dropdown-list .new-list').css('display');
        if($("#dropdown-list").hasClass('visible-display')==false && inputVisibility!="inline-block"){
            $(this).find('ul:first').slideUp(400);
            $("#dropdown-list").removeClass('visible-display');
            
        }
        
    }
}

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
    
    $('.like-dislike').like({like_class: "xxx", dislike_class: "xxx", progress_class: "xxx"});
*/
GRM.like = function(settings) {
    
    settings = jQuery.extend({
        like_class: null,
        dislike_class: null,
        progress_class: null,
        callback: null           
    }, settings);
    
    var token = "grm-like";
    
    return this.each(function(){
        
        if ($(this).attr(token))
            return;
        $(this).attr(token,true);

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
            
            /*GRM.wait();
            if (settings.progress_class)
                $(this).addClass(settings.progress_class);*/
            
            function toggleme(me) {
                // disliking
                if (typeof me.attr('like') != "undefined") {
                    // send vote -1
                    me.find('.dislike').hide();
                    me.find('.like').show();
                    me.removeAttr("like");
                    
                    if (settings.dislike_class)
                        me.removeClass(settings.dislike_class);
                    
                    if (settings.like_class)
                        me.addClass(settings.like_class);
                        
                }
                
                // liking
                else {
                    // send vote +1
                    me.find('.like').hide();
                    me.find('.dislike').show();
                    me.attr("like","true");
                    
                    if (settings.like_class)
                        me.removeClass(settings.like_class);
                    
                    if (settings.dislike_class)
                        me.addClass(settings.dislike_class);
                }
                
            }
            
            toggleme($(this));
            
            $.ajax({
                    type: "POST",
                    url: "/ajax/vote/"+type+"/",
                    data: {
                        instance_id:id,
                        puntuation: vote
                    },
                    context: $(this),
                    error: function() { toggleme($(this)); },
                    success: function(data){
                        
                        if(data!=null)
                            $(this).find('.increase').text(data.votes);
                        else {
                            showMessage("Pio! Perdona se ha producido un error<br>Estamos trabajando en solucionarlo","error");
                            toggleme($(this));
                        }
                        
                        if (settings.callback)
                            settings.callback();
                        
                    },
                    complete: function()
                    {
                        /*
                        if (settings.progress_class)
                            $(this).removeClass(settings.progress_class);
                        GRM.nowait();*/
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
        progress_class: null,
        callback: null    
    }, settings);
    
    var token = "grm-remember";
    
    return this.each(function(){
        
        if ($(this).attr(token))
            return;
        $(this).attr(token,true);
        
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
            
            
            //Primero comprobamos el tipo de mensaje
            var elemType;
            if ($(this).attr('type')=="list")
                elemType="list";
            else
                elemType="suggestion";
            var id = $(this).attr('value'), url = (typeof $(this).attr('remember') != "undefined" )?"/ajax/delete/"+elemType+"/follower/":"/ajax/add/"+elemType+"/follower/";
            
            
            /*
            GRM.wait();
            if (settings.progress_class)
                $(this).addClass(settings.progress_class);*/


            function toggleme(me) {
                // disliking
                if (typeof me.attr('remember') != "undefined" ) {
                    // send vote -1
                    me.find('.forget').hide();
                    me.find('.remember').show();
                    me.removeAttr("remember");
                    
                    if (settings.forget_class)
                        me.removeClass(settings.forget_class);
                    
                    if (settings.remember_class)
                        me.addClass(settings.remember_class);
                        
                }
                
                // liking
                else {
                    // send vote +1
                    me.find('.remember').hide();
                    me.find('.forget').show();
                    me.attr("remember","true");
                    
                    if (settings.remember_class)
                        me.removeClass(settings.remember_class);
                    
                    if (settings.forget_class)
                        me.addClass(settings.forget_class);
                    }
                
                }
            
            toggleme($(this));
            
            $.ajax({
                    type: "POST",
                    url: url,
                    data: {
                        eventid:id,
                        list_id:id
                    },
                    context: $(this),
                    error: function() {
                        toggleme($(this));
                    },
                    success: function(){
                        
                        if (settings.callback)
                            settings.callback();
                    },
                    complete: function()
                    {
                        /*if (settings.progress_class)
                            $(this).removeClass(settings.progress_class);
                        GRM.nowait();*/
                    }
                });
        });
    });
};

/*
    HOW TO USE
    --------------------------------
    HTML Template needed:
    
    <span class="btn dropDownBtn">
        Guardar en
        <ul class="submenu" style="display:none" id="dropdown-list">
            {% if lists %}
                {% for obj in lists %}
                    {% if obj.user.username = request.user.username %}
                        <!-- Solo se muestran mis listas -->
                        <li id="listid-{{obj.id}}">{{obj.name}} (<span class="list-{{obj.id}}-counter">{{obj.keys|length}}</span> sugerencias)</li>
                    {% endif %}
                {% endfor %}
            {% endif %}
            <li class="new-list-btn">
                <span id="text">Nueva lista...</span>
                <span class="new-list" style="display:none"><input type="text" /></span><div id="cancel-link" onclick="closeDropdown()" style="display:none">Cancel</div>
            </li>
        </ul>
    </span>
    
    Javascript call at onready
    $('.dropDownBtn').menuList({onNewList: function(){}});
*/
GRM.menuList = function(settings) {
    
    settings = jQuery.extend({
        onNewList: null,
        onLiClick: null
        
    }, settings);
       
    return this.each(function(){
        
        // Menu desplegable "Listas"
            
            
            $(this).hoverIntent(hiConfig);
            $(this).find('.submenu').hoverIntent(hiConfig);
            $(this).click(function(){
                $(this).find('ul:first:hidden').css({visibility: "visible",display: "none"}).slideDown(400);
            })
            
            //console.log("settings.onLiClick="+settings.onLiClick)
            if(settings.onLiClick!=null)
                $(this).find('.submenu li:not(.dropDownBtn-btn,.new-list-btn)').click(settings.onLiClick);
            else
                $(this).find('.submenu li:not(.dropDownBtn-btn,.new-list-btn)').click(function(){submenuLiBehave(this)})
            
            //Enter behave when adding new list on Suggestions Tab
            $(this).find(".new-list-btn span.new-list").keyup(function(e) {
                var suggestionList=[];
                e.preventDefault();
                if (e.which == 27){
                    //On press escape
                    closeDropdown();
                }else if(e.keyCode == 13) {
                    if(settings.onNewList!=null){
                        settings.onNewList($(this).find('input').val());
                    }else{
                        //On press enter
                        //Comprobamos si hay sugerencias seleccionadas para añadirlas
                        var checkedSuggestions=$('.suggestion input[name=suggestions]').filter(':checked');
                        if( checkedSuggestions.length>0){
                            checkedSuggestions.each(function(){
                                suggestionList.push($(this).attr('id').substring(9,$(this).attr('id').length))
                            })
                        }
                        
                        $.ajax({
                            type: "POST",
                            url: url["modify_suggestion_list"],
                            data: {
                                name: $(this).find('input').val(),
                                suggestions: suggestionList
                            },
                            dataType:'json',
                            success: function(data){
                                //Añadimos la lista al desplegable
                                $("<li id=\"listid-"+data.id+"\">"+data.name+" (<span class=\"list-"+data.id+"-counter\">"+data.keys.length+"</span> sugerencias)</li>").insertBefore('.new-list-btn');
                                $('#listid-'+data.id).click(function(){submenuLiBehave(this)});
                                
                                //Añadimos la lista en la pestaña listas
                                
                                //Reordenamos alfabéticamente la lista desplegable
                                $('.submenu li').not('li.new-list-btn').sortElements(function(a, b){
                                    return $(a).text().toLowerCase() > $(b).text().toLowerCase() ? 1 : -1;
                                });
                                
                                $("#dropdown-list").removeClass('visible-display');
                                
                                //Añadimos a la sugerencia dentro de la lista de sugerencias 
                                //las nuevas listas en las que se encuentra
                                updateSuggestions(data);
                                
                                //Actualizamos el contador de la lista con el número de sugerencias
                                updateCounter(data.id,data.keys.length);
                                
                                //Añadimos la lista a la pestaña listas
                                var suggestions=[];
                                $(data.keys).each(function(){
                                    suggestions.push({
                                            id:this,
                                            name:$('#suggestion_'+this+' .suggestionName_editable').text()
                                        })
                                })
                                var obj=$("#listTemplate").tmpl({obj:data, keys:suggestions}).appendTo("#suggestion-list-lists");
                                if(obj.find('.suggestions ul li').length > 0){
                                    tmp=obj;
                                    obj.find('.suggestions ul').show();
                                    obj.find('.suggestions .empty-msg').hide();
                                    obj.find('.suggestions li.removable').click(function(){
                                        var unparsedString=$(this).attr('class').split(" ")[0];
                                        var listID = unparsedString.substring(5,unparsedString.length)
                                        removeFromList(this,listID);
                                    });
                                }
                                
                                
                                setExpandible('#list_'+data.id);
                                
                                
                                // Activamos el mismo comportamiento que tienen el resto de listas:
                                // que se puedan editar los campos, que se activen los diálogos para compartir
                                // y que se puedan mostrar y ocultar las estadísticas
                                set_editable_fields();
                                
                                create_share_links();
                                
                                obj.find('.show-more').click(show_and_hide_stats_callback);
                                
                                //Aumentamos el contador de las listas
                                $('#lists-tab-counter').text(parseInt($('#lists-tab-counter').text())+1);
                                
                                //Mostrar mensaje de éxito
                                showMessage("La lista ha sido añadida con éxito","success")
                                
                                
                            }
                        });
                    }
                    
                        
                    
                    $(".new-list-btn span#text").css('display','inline-block')
                    $(".new-list-btn span.new-list").css('display','none')
                    $(".new-list-btn div#cancel-link").css('display','none')
                    $(".new-list-btn span.new-list").find('input').val("");
                }                
            });
            
            //Reordenamos alfabéticamente la lista desplegable
            $('.submenu li').not('li.new-list-btn').sortElements(function(a, b){
                return $(a).text().toLowerCase() > $(b).text().toLowerCase() ? 1 : -1;
            });
            
            //Convierte el texto de nueva lista en un input field
            $(this).find('.new-list-btn span#text').click(function(){                
                $(this).css('display','none')
                $(this).parent().find("span.new-list").css('display','inline-block')
                $(this).parent().find("span.new-list").find('input').focus()
                $(this).parent().find("div#cancel-link").css('display','block')
                var tmp=$('#text').parentsUntil('.dropDownBtn');
                var dropdown=tmp[tmp.length-1]
                $(dropdown).addClass('visible-display');
            })
        
    });
}

GRM.removable = function() {

    var token = "grm-removable";

    return this.each(function(){

        if ($(this).attr(token))
            return;
        $(this).attr(token,true);

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

GRM.loadTimeline = function(settings){

        var token = "grm-loadtimeline";

        settings = jQuery.extend({
            container: null
            
        }, settings);
           
        return this.each(function(){
            
                    if ($(this).attr(token))
                        return;
                        
                    $(this).attr(token,true);
                    
                    $(this).click(function(){
                        
                    var loadmore = $(this);
                    
                    var data = {};
                    data['query_id'] = $(settings.container).attr("value");
                    
                    if ($(settings.container).attr("username"))
                        data['username'] = $(settings.container).attr("username");
                    
                    loadmore.addClass("waiting");

                    var url = '/ajax/get/'+$(this).attr('type')+'/';
                    
                    $.ajax({
                        type: 'POST',
                        url: url,
                        data: data,
                        complete: function() { loadmore.removeClass("waiting"); },
                        success: function(data){
                            if(data[1].length>0){
                                if(data[0].length==2)
                                    $(settings.container).attr("value",'["'+data[0][0]+'","'+data[0][1]+'"]');
                                else
                                    $(settings.container).attr("value",data[0]);
                                var nextPage=parseInt($(settings.container).attr("page"))+1;
                                $(settings.container).attr("page",nextPage);
                                
                                $.each(data[1], function(index,suggestion){
                                    var temp=$(suggestion).appendTo(settings.container);
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
                                loadmore.hide();
                            }
                        }
                    });
                });
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
            //if (typeof resizeIframe != "undefined") resizeIframe();
            
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
jQuery.fn.loadTimeline = GRM.loadTimeline;
jQuery.fn.remember = GRM.remember;
jQuery.fn.removable = GRM.removable;
jQuery.fn.menuList = GRM.menuList;

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
        $('#notification-msg').attr('class',"")
        $('#notification-msg').html(txt)
        $('#notification-msg').addClass(msgClass)
        var posTop=$(window).scrollTop();
        if(posTop<60)posTop=60;
        $('#notification-msg').css('top',posTop+'px');
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

//Cierra el menu desplegable
function closeDropdown(){
    $("#dropdown-list").removeClass('visible-display');
    $(".new-list-btn span#text").css('display','inline-block');
    $(".new-list-btn span.new-list").css('display','none');
    $(".new-list-btn div#cancel-link").css('display','none');
    $(".new-list-btn span.new-list").find('input').val("");
}

function FormatNumberLength(num, length) {
    var r = "" + num;
    while (r.length < length) {
        r = "0" + r;
    }
    return r;
}

function validateDates(start,end){
    //Date format mm/dd/aaaa
    var start = start.split("/");
    var end = end.split("/");
    
    start = new Date(start[0], start[1] -1, start[2]);
    end = new Date(end[0], end[1] -1, end[2]);

    if (start > end) 
        return false;
    else
        return true;
}
function validateTimes(start,end){
    //Time format hh:mm
    var start = start.split(":");
    var end = end.split(":");
    
    if(start[0]>end[0])
        return false;
    else if(start[0]==end[0] && start[1]>end[1])
        return false;
    return true;
}

function checkEmail() {
    var email = $('#registerEmail').val();
    var item = $('#registerEmail').next('div');
    var st = $('#emailStatus');
    item.text('');
    st.hide();

    if (email=='Email') {
        item.text('Necesitamos que rellenes el email');
        //$(email).addClass('error');
        item.show();
        st.removeClass("ok").addClass("no-ok");
        st.show();
        return false;
    }
    
    if (!GRM.common.checkemail(email)) {
        item.text('E-mail inválido');
        item.show();
        st.removeClass("ok").addClass("no-ok");
        st.show();
        return false;
    }
    else {
        $.ajax({
            url:"/ajax/exists/",
            type:'post',
            dataType:'json',
            data: {
                email: email,
                "csrfmiddlewaretoken": $('#registerFormForm input[type="hidden"]').val() 
            },
            async:true,
            success: function(data){ 
        
                if(data.result){
                    item.text("Esta cuenta ya está siendo usada");
                    item.show();
                    st.removeClass("ok").addClass("no-ok");
                    st.show();
                }
                else
                {
                    //item.text("Esta cuenta ya está siendo usada");
                    st.removeClass("no-ok").addClass("ok");
                    st.show();
                    item.hide();
                }
            }
        });
    }
    
    return true;
}

function checkTerms() {
    if (!$('#termsCheckbox').is(":checked")) {
       showMessage("Para poder crear una cuenta primero necesitas leer y aceptar las condiciones de uso.","error");
       return false;
    }
    return true;
}

function checkPasswords(emptymessage) {
    
    var pwd1 = $('#userRegisterPass1').val(), pwd2 = $('#userRegisterPass2').val();
    var item = $('#passwordStatus');
    
    if (pwd1.length==0 || pwd2.length==0) {

        if (emptymessage) {
            item.text("Debes rellenar los dos campos de las contraseñas");
            item.show();
        }

        return false;
        }
    
    if (pwd1!=pwd2){

        item.text("Las contraseñas no coinciden, por favor vuelva a introducirlas");
        item.show();

        return false;
        }
    
    if (pwd1.length<6){
        item.text("La contraseña tiene que tener al menos 6 caracteres");
        item.show();
        return false;
        }
    
    return true;
}

function showMenu(){
    $('#login-bar p').show();
    $('#login-bar ul').show();
    $('#georemindme-form').hide();
}

function checkUncheck(obj){
    var checkbox=$(obj).find('input');
    if($(checkbox).attr('checked')==true)
        $(checkbox).attr('checked',false);
    else
        $(checkbox).attr('checked',true)
}

/**
 * jQuery.fn.sortElements
 * --------------
 * @param Function comparator:
 *   Exactly the same behaviour as [1,2,3].sort(comparator)
 *   
 * @param Function getSortable
 *   A function that should return the element that is
 *   to be sorted. The comparator will run on the
 *   current collection, but you may want the actual
 *   resulting sort to occur on a parent or another
 *   associated element.
 *   
 *   E.g. $('td').sortElements(comparator, function(){
 *      return this.parentNode; 
 *   })
 *   
 *   The <td>'s parent (<tr>) will be sorted instead
 *   of the <td> itself.
 */
jQuery.fn.sortElements = (function(){
 
    var sort = [].sort;
 
    return function(comparator, getSortable) {
 
        getSortable = getSortable || function(){return this;};
 
        var placements = this.map(function(){
 
            var sortElement = getSortable.call(this),
                parentNode = sortElement.parentNode,
 
                // Since the element itself will change position, we have
                // to have some way of storing its original position in
                // the DOM. The easiest way is to have a 'flag' node:
                nextSibling = parentNode.insertBefore(
                    document.createTextNode(''),
                    sortElement.nextSibling
                );
 
            return function() {
 
                if (parentNode === this) {
                    throw new Error(
                        "You can't sort elements if any one is a descendant of another."
                    );
                }
 
                // Insert before flag:
                parentNode.insertBefore(this, nextSibling);
                // Remove flag:
                parentNode.removeChild(nextSibling);
 
            };
 
        });
 
        return sort.call(this, comparator).each(function(i){
            placements[i].call(getSortable.call(this));
        });
 
    };
 
})();  


(function($){  
$.extend(  
{  
    jsonp: {  
        script: null,  
        options: {},  
        call: function(url, options) {  
            var default_options = {  
                callback: function(){},  
                callbackParamName: "callback",  
                params: []  
            };  
            this.options = $.extend(default_options, options);  
            //Determina si se debe añadir el parámetro separado por ? o por &  
            var separator = url.indexOf("?") > -1? "&" : "?";  
            var head = $("head")[0];  
            /*Serializa el objeto en una cadena de texto con formato URL*/  
            var params = [];  
            for(var prop in this.options.params){  
                params.push(prop + "=" + encodeURIComponent(options.params[prop]));  
            }  
            var stringParams = params.join("&");  
            //Crea el script o borra el usado anteriormente  
            if(this.script){  
                head.removeChild(script);  
            }  
            script = document.createElement("script");  
            script.type = "text/javascript";  
            //Añade y carga el script, indicandole que llame al metodo process  
            script.src = url + separator + stringParams + (stringParams?"&":"") + this.options.callbackParamName +"=jQuery.jsonp.process";  
            head.appendChild(script);  
        },  
        process: function(data) { this.options.callback(data); }  
    }  
});  
})(jQuery)  

//How to use: showHelp('#mobile','#texto3','right');
function showHelp(element,text_help,position,plusLeft,plusTop){
	if(!$(text_help).hasClass('help-box'))
		$(text_help).addClass('help-box');
	
	$(text_help +' div.arrow').each(function(i,elem){
		$(elem).remove();
	});
	arrow = $('<div class="arrow arrow-'+position+'"></div>');
	$(text_help).append(arrow);
	

	var adjust_top,adjust_left,arrow_top,arrow_left;
	var box_size = [$(text_help).width(),$(text_help).height()]
	
	if(position==='right'){
		adjust_top=-15;
		adjust_left=-300;
		arrow_top=0;
		arrow_left=box_size[0]+11;//5px porque tiene 10 de ancho
	}else if(position==='left'){
		adjust_top=-15;
		adjust_left=$(element).width();
		arrow_top=0;
		arrow_left=-11;//5px porque tiene 10 de ancho
	}else if(position==='up'){
		adjust_top=$(element).height();
		adjust_left=-$(text_help).width()/2+$(element).width()/2-20;
		arrow_top=-11;
		arrow_left=box_size[0]/2-5;//5px porque tiene 10 de ancho
	}else if(position==='down'){
		adjust_top=-$(text_help).height()-40;
		adjust_left=-$(text_help).width()/2+$(element).width()/2-20;
		arrow_top=box_size[1]+8;
		arrow_left=box_size[0]/2-5;//5px porque tiene 10 de ancho
	}

	if(plusTop!=null)
		adjust_top += plusTop;
	if(plusLeft!=null)
		adjust_left += plusLeft;

	
	var pos=$(element).position()
	var top_pos=pos['top']+adjust_top;
	var left_pos=pos['left']+adjust_left;
	
	$(text_help).css('top',top_pos+'px')
	$(text_help).css('left',left_pos+'px')
	
	$(text_help).show();
	
	$(text_help +' div.arrow').css('top',arrow_top+'px')
	$(text_help +' div.arrow').css('left',arrow_left+'px')
	
	if($('#showing-help').length==0){
		invisible_layer = $('<div id="showing-help" style="width:100%;height:100%;position:absolute;z-index:99" onclick="javascript:closeHelp()"></div>');
		$('body').prepend(invisible_layer)
	}
}

function closeHelp(){
	$('.help-box').hide();
	$('#showing-help').remove();
}

// ensuring ajax https
$(document).ajaxSend(function(event, xhr, settings) {
    if ( document.location.hostname != "localhost" && document.location.hostname != "127.0.0.1" && document.location.protocol.slice(0,5) != "https" && settings.url.slice(0,6)=="/ajax/" ) {
        settings.url = "https://georemindme.appspot.com" + settings.url;
        //settings.xhrFields =  { withCredentials: true };
    }
});
