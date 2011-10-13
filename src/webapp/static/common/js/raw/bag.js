// SACO ESTO A UNA FUNCIÓN APARTE PARA REUTILIZARLO
// AL CREAR UNA NUEVA LISTA
function show_and_hide_stats_callback(){
        var textElement=$(this).parent().find('.show-more-text');
        if($(textElement).css('display')!="none")
            $(this).html(gettext("Mostrar estadísticas"))
        else
            $(this).html(gettext("Ocultar estadísticas"))
        
        $(textElement).toggle('slow')
    }
    
// SACO ESTO A UNA FUNCIÓN APARTE PARA REUTILIZARLO
// AL CREAR UNA NUEVA LISTA
function create_share_links(){
    // ------------------------------------
    // CREANDO LOS BOTONES DE COMPARTIR 
    // CON LAS REDES SOCIALES
    // ------------------------------------
    $('.share a').click(function(e){e.preventDefault();});
    $('.share').click(function(){
        var template;
        
        if($(this).attr("type")=="link"){
            template="#shareLink";
            settings={ 
                buttons: [],
                dialogClass: 'link-dialog',
                title: "Compartir enlace",
                buttons: [{
                    text: "Cerrar",
                    click: function() { 
                        $(this).dialog("close"); 
                    }}] 
            }
        }else if($(this).attr("type")=="twitter"){
            //DIALOGO DE TWITTER
            template="#shareTwitter";
            settings={ 
                title: gettext("Compartir en Twitter"),
                dialogClass: 'twitter-dialog',
                buttons: [{
                    text: gettext("Enviar"),
                    click: function() { 
                        
                        var linkEl = $(this).find('.twitter-share-button');
                        if($(linkEl).length!=0){
                            //Este comportamiento es para los usuarios
                            //que no tienen cuenta de twitter asociada
                            var field = $(this).find('textarea');
                            linkEl.attr("href","http://twitter.com/share?text="+$(field).val()+"&url=")
                            if(linkEl.attr('onclick') === undefined || linkEl.attr('onclick')==null){
                                window.open(linkEl.attr('href'));
                            } else {
                                linkEl.click ();
                            }
                            $(this).dialog("close"); 
                        }else{
                            var element=$(this).find('textarea');
                        
                            var params;
                            if($(element).attr("event-type")=="event")
                                params={
                                    "event_id"  : $(element).attr("data-id"),
                                    "msg"       : $(element).val()
                                }
                            else
                                params={
                                    "list_id"  : $(element).attr("data-id"),
                                    "msg"       : $(element).val()
                                }
                                
                            $.ajax({
                                type: "POST",
                                url: "/ajax/share/twitter/",
                                data: params,
                                context: $(this),
                                success: function(data){
                                    $(this).dialog("close"); 
                                }
                            });
                        }
                    }
                },{
                    text: gettext("Cancelar"),
                    click: function() { 
                        $(this).dialog("close"); 
                    }}] 
            }
        }else if($(this).attr("type")=="wall"){
            //DIALOGO DE FACEBOOK
            template="#shareFacebook";
            settings={ 
                title: gettext("Compartir en Facebook"),
                dialogClass: 'facebook-dialog',
                buttons: [{
                    text: gettext("Publicar"),
                    click: function() { 
                        
                        var element=$(this).find('textarea');
                        
                        var params;
                        if($(element).attr("event-type")=="event")
                            params={
                                "event_id"  : $(element).attr("data-id"),
                                "msg"       : $(element).val()
                            }
                        else
                            params={
                                "list_id"  : $(element).attr("data-id"),
                                "msg"       : $(element).val()
                            }
                            
                        $.ajax({
                            type: "POST",
                            url: "/ajax/share/facebook/",
                            data: params,
                            context: $(this),
                            success: function(data){
                                $(this).dialog("close"); 
                            }
                        });
                    }
                },{
                    text: gettext("Cancelar"),
                    click: function() { 
                        $(this).dialog("close"); 
                    }
                }] 
            }
        }
        
        var obj=$(template).tmpl({
            "type"        :$(this).attr("data-type"),
            "elem_id"     :$(this).attr("value"),
            "link"        :$(this).attr("data-href")
        });
        
        $('#share-text').html(obj);
        setRemainingCharCounter('#twitter_msg','#twitter-counter');
        $('#id_name').keyup();
        $('#share-text').dialog(settings);
        $('#share-text').dialog("open");
    })
    /* FIN CREANDO LOS BOTONES DE COMPARTIR */
}



$(document).ready(function(){    
    //Asignamos comportamiento ONCLICK a cada fila --> Desplegar detalles
    setExpandible('.suggestion');
    
    //Searchable input fields
    $('#filter-suggestions').search('#suggestion-list > div',['.suggestionName_editable']);
    $('#filter-lists').search('#suggestion-list-lists > div',['.suggestionName_editable']);
    
    //Select all checkbox
    $('#checkBox_all,#checkBoxList_all').click(function(){
        var elemID=$(this).attr('id');
        //Le quitamos el "_all"
        elemID=elemID.substring(0,elemID.length-4)
//				console.log(':regex(id,^('+elemID+'_))')
        if($('#'+elemID+'_all').is(':checked'))
            $(':regex(id,^('+elemID+'_))').attr('checked',true);
        else
            $(':regex(id,^('+elemID+'_))').attr('checked',false);
    });
    
    //Editable fields
    set_editable_fields();
    
    //Show empty msg if there are no elements
    $('.empty-msg').parent().find('ul').each(function(i,elem){
        if($(elem).children().length==0){
            $(elem).hide();
            $(elem).parent().find('.empty-msg').show();
        }else{
            $(elem).parent().find('.empty-msg').hide();
        }
    })

    //Adding behaviour to tab content
    $('#tabMenu li').click(function(){
        tab_id=$('#tabMenu li.active').attr('id')
        $('#'+tab_id+'_content').addClass('hidden');
        $('#tabMenu li.active').removeClass('active');
        
        tab_id=$(this).attr('id')
        $('#'+tab_id+'_content').removeClass('hidden');
        $(this).addClass('active');
    })
    
    $('span.btn.dropDownBtn').menuList();
    
   
    
    //On expanded view of a suggestion--> Remove suggestion from a list
    $('.removable-sugestion-list li').click(function(){
        var unparsedString=$(this).attr('class').split(" ")[0];
        var listID = unparsedString.substring(5,unparsedString.length)
        removeFromList(this,listID);
    });
    
    //Añade el comportamiento a las sugerencias que se pueden 
    //eliminar de una lista y a las listas a las que pertenece
    //una sugerencia.
    $('#suggestion-list-lists .suggestions li.removable').click(function(){
        var unparsedString=$(this).attr('class').split(" ")[0];
        var listID = unparsedString.substring(5,unparsedString.length)
        removeFromList(this,listID);
    });
    

    
                
    //On LISTS tab, add new list
    $('.addNewList').click(function(){
       //console.log("Añadimos nueva lista") 
    });
    
    //Selecciona la sugerencia actual, desmarca las demas y despliega
    //la lista
    $('.add-on-list').click(function(){
        $(':regex(id,^(checkBox_))').attr('checked',false);
        $("#checkBox_"+$(this).attr('value')).attr('checked',true);
        $(".dropDownBtn").click()
    });
    
    // Comportamiento del botón mostrar y ocultar estadísticas
    $('.show-more').click(show_and_hide_stats_callback);
    
    
    //Placeholders
    $("[placeholder]").placeholder();
    $(".new-list input").css("color","black")
    $(".new-list input").css("font-style","normal")
    
    //------------------------------------
    //Boton de filtrar mis sugerencias
    //------------------------------------
    $('#filterMySuggestions').toggle(function(){
        $(this).addClass('pressed');
        var tmp=$('#suggestion-list .not-mine')
        tmp.fadeOut('slow');
        var counter=parseInt($('#suggestions-tab-counter').html());
        $('#suggestions-tab-counter').html(counter-tmp.length);
        
    },function(){
        $(this).removeClass('pressed');
        var tmp=$('#suggestion-list .not-mine');
        tmp.fadeIn('slow');
        var counter=parseInt($('#suggestions-tab-counter').html());
        $('#suggestions-tab-counter').html(counter+tmp.length);
        
    });
    
    //------------------------------------
    //Boton de filtrar mis listas
    //------------------------------------
    $('#filterMyLists').toggle(function(){
        $(this).addClass('pressed');
        $('#suggestion-list .not-mine').fadeOut('slow');
    },function(){
        $(this).removeClass('pressed');
        $('#suggestion-list-lists .not-mine').fadeIn('slow');
    });

    create_share_links();
    
    /*Set date picket behaviour*/
    $( ".date-type" ).datepicker();
    $('.datepicker .date-type,.datepicker .hour-type').change(function(){
        if($(this).val()=="mm/dd/aa" || $(this).val()=="hh:mm" || $(this).val()==""){
            //console.log("No desmarcamos porque val="+$(this).val());
        }else{
            $(this).parent().find('.anytime [type="checkbox"]').attr('checked',false);
            //~ console.log("Desmarcamos porque val="+$(this).val());
        }
        tmp=$(this)
    })
    $('.anytime [type="checkbox"]').click(function(){
        $(this).parent().parent().find(".start-date,.end-date").val("mm/dd/aa");
        $(this).parent().parent().find(".start-hour,.end-our").val("").blur();
    })
    
    $('.datepicker').find('span').click(function(){$(this).parent().find('[type="checkbox"]').click()})
    /*End set date picket behaviour*/
    
    
});//END $(document).ready

/*
 * 
 * 
 * 
 */





// Actualizamos la información de en que listas se encuentra
// cada una de la sugerencias del grid
function updateSuggestions(data){
    asd=data;
    var suggestions = data.keys;
    var listID = data.id;
    var listName = data.name;
    
    $(suggestions).each(function(i,suggestionID){
        /** SUGGESTIONS TAB **/
        //Comprobamos si ya aparece en el DOM de la sugerencia, la lista de sugerencias
        if($('#suggestion_'+suggestionID+' .removable-sugestion-list .list_'+listID).length==0){
            //Si no existe creamos el elemento y le damos el comportamiento de edición/borrado
            var tmp='<li class="list_'+listID+' removable" value="'+suggestionID+'">'+listName+'</li>';
            $('#suggestion_'+suggestionID+' .removable-sugestion-list ').append(tmp);
            var element=$('#suggestion_'+suggestionID+' .removable-sugestion-list .list_'+listID);
            element.click(function(){
                var unparsedString=$(this).attr('class').split(" ")[0];
                var listID = unparsedString.substring(5,unparsedString.length)
                removeFromList(this,listID);
            });
            
            //Si se mostraba en el mensaje de vacío lo borramos
            if(element.parent().css('display')=="none"){
                element.parent().show();
                element.parent().parent().find('.empty-msg').hide();
            }
        }
        
        /** LISTS TAB **/
        //Comprobamos si en la lista ya existe la sugerencia
        if ($('#list_'+listID+' .suggestions li[value="'+suggestionID+'"]').length==0){
            //Si no está la sugerencia en la lista la añadimos
            $('#list_'+listID+' .suggestions ul').append('<li value="'+suggestionID+'" class="list_'+listID+' removable">'+$('#suggestion_'+suggestionID+' .suggestionName_editable').text()+'</li>');
            
            $('#list_'+listID+' .suggestions ul li[value="'+suggestionID+'"]').click(function(){
                var unparsedString=$(this).attr('class').split(" ")[0];
                var listID = unparsedString.substring(5,unparsedString.length)
                removeFromList(this,listID);
            });
            
            if($('#list_'+listID+' .suggestions ul li').length==1){
                $('#list_'+listID+' .suggestions ul').show();
                $('#list_'+listID+' .suggestions .empty-msg').hide();
                
            }
        }
    })
    
    
}

//Extrae a una sugerencia de una lista
function removeFromList(obj,listID){
    
    suggestionID = $(obj).attr('value')
    domElement=$(obj);
    
    //console.log("Eliminamos sugerencia "+suggestionID+" de la lista " + listID)
    
    $.ajax({
        type: "POST",
        url: url["modify_suggestion_list"],
        data: {
            list_id: [listID],
            suggestions_del: [suggestionID]
        },
        dataType:'json',
        success: function(data){

            
            //Ocultamos el objeto y eliminamos
            domElement.fadeOut(function(){ 
                if($('#suggestion_'+suggestionID+' .removable-sugestion-list li').length==1){
                    //Mostramos el mensaje de que no quedan más
                    $('#suggestion_'+suggestionID+' .empty-msg').fadeIn('slow');
                }
                
                if($(obj).parent().children().length==1){
                    //console.log("Ya no quedan más hermanos");
                    $(obj).parent().parent().find('.empty-msg').show()
                }
                $(obj).remove();
                
                //Actualizamos el contador de la lista
                updateCounter(listID,data.keys.length);
            })
            
            //Buscamos en la pestaña opuesta
            if($('#suggestions_lists').hasClass('active')){
                //Borramos del detalle de sugerencia la lista
                if($('#suggestion_'+suggestionID+' ul.removable-sugestion-list li').length==1){
                    //Ya no quedan más hermanos en la pestaña detalle de sugerencia
                    $('#suggestion_'+suggestionID+' .empty-msg').show()
                }
                $('#suggestion_'+suggestionID+' .list_'+listID).remove()
            }else{
                //Borramos del detalle de lista la sugerencia
                if($('#list_'+listID+' dd.suggestions li').length==1){
                    //Ya no quedan más hermanos en la pestaña detalle de sugerencia
                    $('#list_'+listID+' dd.suggestions .empty-msg').show()
                }
                $('#list_'+listID+' li[value="'+suggestionID+'"]').remove()
                
            }
            
            showMessage(gettext("La sugerencia ha sido eliminada de la lista correctamente"),"success")

            
        }
    });
}

//Añade las sugerencias marcadas a la lista correspondiente
function submenuLiBehave(obj){
    
    
    
    if($(obj).attr('id')=="new-list-btn")
        return false;
    
    var data={};
    data['list_id']=[$(obj).attr('id').substring(7,$(obj).attr('id').length)];
    data['suggestions']=new Array();
    
    var checkedSuggestions=$('.suggestion input[name=suggestions]').filter(':checked');
    if( checkedSuggestions.length==0){
        showMessage(gettext("No hay ninguna sugerencia seleccionada"),"error")
    }else{
        checkedSuggestions.each(function(i,elem){
            //console.log("Añadimos a la lista: la sugerencia: "+$(elem).attr('id'));
            data['suggestions'][i]=$(elem).attr('id').substring(9,$(this).attr('id').length)
        });
        $.ajax({
            type: "POST",
            url: url["modify_suggestion_list"],
            data: data,
            dataType:'json',
            success: function(data){
                
                //Añadimos a la sugerencia dentro de la lista de sugerencias 
                //las nuevas listas en las que se encuentra
                updateSuggestions(data);
                
                
                //Actualizamos el contador de la lista
                updateCounter(data.id,data.keys.length);
                
                //Mostrar mensaje de éxito
                showMessage(gettext("Las sugerencias han sido añadidas a la lista"),"success")
            }
        });
    }
    
}



function toogleSuggestion(obj){
    var suggestion_id=$(obj).parent().attr('id').substr(11)
    var temp=$(obj).parent()
    
    temp.parent().find('div.expanded').toggle();
    temp.parent().find('div.collapsed').toggle();
}


//function loadSuggestionsPage(page){
//    GRM.loadPage({
//        page:page,
//        "total_pages":{{suggestions.2}},
//        container:'#suggestion-list',
//        url:'/ajax/get/suggestion/',
//        template: "#suggestionTemplate",
//        data:{
//                'query_id':"{{suggestions.0}}",
//            }                
//    });
//}

//Establece el comportamiento a un objeto para poder expandirse
function setExpandible(obj){
    $(obj+' .maximize-minimize').toggle(function(){
            //Lo primero que hacemos es cerrar todas aquellas listas/sugerencias
            //que ya estén desplegadas --> Accordion
            var parents=$(this).parentsUntil(".tab-content");
            var elementsList=parents[parents.length-1];
            var elements;
            if($(elementsList).attr("id")=="suggestion-list-lists")
                elements=$(elementsList).children()
            else
                elements=$(elementsList).parent().children()
            
            $(elements).each(function(i,elem){
                if($(elem).find(".expanded").css("display")!="none"){
                    $(elem).find(".maximize-minimize").click()
                    
                }
            })
            //A continuación expandimos
            $(this).parent().find('div.expanded').slideDown('fast');
            $(this).parent().find('.suggestionName').toggle();
            $(this).parent().find('.suggestionName_editable').toggle();
            $(this).removeClass('suggestionCollapsed');
            $(this).addClass('suggestionExpanded');
        },function() {
            $(this).parent().find('div.expanded').slideUp('fast'); 
            $(this).parent().find('.suggestionName').toggle();
            $(this).parent().find('.suggestionName_editable').toggle();
            $(this).removeClass('suggestionExpanded');
            $(this).addClass('suggestionCollapsed');
    });
    
    //Copiamos el comportamiento del click sobre el botón al hacerlo
    //sobre el nombre de la sugenrecia
    $(obj+' .suggestionName').click(function(){
        var element=$(this).parentsUntil('.suggestion').parent().find('.maximize-minimize')
        //Solo simula click cuando no está expandido
        if($(element).hasClass("suggestionCollapsed"))
            $(element).click();
    })
    $(obj+' .suggestionName_editable').click(function(){
        var element=$(this).parentsUntil('.suggestion,.suggestionList').parent().find('.maximize-minimize')
        //Solo simula click cuando no está expandido
        if($(element).hasClass("suggestionCollapsed"))
            $(element).click();
    })
}

//Elimina las sugerencias marcadas
function removeSuggestions(){
    temp=$("input[name='suggestions']:checked")
    $.each(temp, function(index,value){
        $.ajax({
            type: "POST",
            url: "/ajax/delete/suggestion/",
            data: {
                eventid:value.value
            },
            complete: function(msg){
                if (msg.status !=200){
                    showMessage("Error: "+msg.status,"error")
                }else{
                    $('#suggestion_'+value.value).fadeOut('slow').remove()
                    showMessage("Las sugerencias han sido eliminadas con éxito","success")
                    //Disminuimos el contador
                    $('#suggestions-tab-counter').text(parseInt($('#suggestions-tab-counter').text())-1);
                }
                
            }
        });
    })
}

//Elimina las listas marcadas
function removeLists(){
    temp=$("input[name='lists']:checked")
    $.each(temp, function(index,value){
        $.ajax({
            type: "POST",
            url: "/ajax/delete/suggestion/list/",
            data: {
                list_id: value.value
            },
            complete: function(msg){
                if (msg.status !=200){
                    showMessage("Error: "+msg.status,"error")
                }else{
                    $('#list_'+value.value).fadeOut('slow').remove()
                    showMessage(gettext("Las listas han sido eliminadas con éxito"),"success")
                    //Disminuimos el contador
                    $('#lists-tab-counter').text(parseInt($('#lists-tab-counter').text())-1);
                    
                    //La borramos del desplegable
                    $('#dropdown-list #listid-'+value.value).remove();
                    
                    //Y del detalle de sugerencia
                    $('.list_'+value.value).remove()
                    
                }
                
            }
        });
    })
}

//Actualiza el contador de la lista: listID y le pone el valor Val
function updateCounter(listID,val){
    counterClass='.list-'+listID+'-counter';
    $(counterClass).text(val);
}

//Obtiene el id de una sugerencia
function get_suggestion_id(obj){
    var hash={};
    var parents=$(obj).parentsUntil(':regex(id,(suggestion-list|suggestion-list-lists))');
    var suggestion_element=parents[parents.length-1];
    if($(suggestion_element).hasClass("suggestionList"))
        hash['list_id']=($(suggestion_element).attr("id")).substring(5,($(suggestion_element).attr("id")).length);
    else
        hash['eventid']=($(suggestion_element).attr("id")).substring(11,($(suggestion_element).attr("id")).length);
    var if_editing_name=$('form.editable-fields input[name="name"]').val();
    if(typeof(if_editing_name)!="undefined")
        hash['name']=if_editing_name;
    else
        hash['name']=$(suggestion_element).find('.suggestionName').html();

    
    if($(suggestion_element).find('.editable_visibility select').length>0)
        hash['visibility']=$(suggestion_element).find('.editable_visibility select').val();
    else
        hash['visibility']=$(suggestion_element).find('.editable_visibility').attr("value");
                 
    return hash;
}

function nl2br (str, is_xhtml) {   
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br />' : '<br>';    
    return (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1'+ breakTag +'$2');
}
//Establece los campos editables de las sugerencias de las que se es autor
function set_editable_fields(objID){
    var eventidValue;
    var tmp;
    
    var base_settings={ 
         cancel    : gettext('Cancelar'),
         data: function(value, settings) {
            /* Convert <br> to newline. */
            var retval = value.replace("\n", '').replace(/<br[\s\/]?>/gi, '\n');
            return retval;
        },
         submit    : gettext('Guardar'),
         indicator : gettext('Guardando...'),
         tooltip   : gettext('Haz clic para editar...'),
         cssclass  : 'editable-fields',
         onblur    : 'ignore',
         callback  : function(value, settings){
                    //Establecemos el valor guardado
                    $(this).html(nl2br(tmp))
                    if( $(this).hasClass("suggestionName_editable") ){
                        this.previousElementSibling.innerHTML = nl2br(tmp);
                    }
                    
         },
         onerror    : function(settings, original, xhr){
                        
                        //console.log(original);
                        //console.log(settings);
                        //console.log(xhr);
                        //if(xhr.status==500){
                            showMessage(gettext("Ouch! Se ha producido un error; perdón!, lo solucionaremos lo antes posible!"),"error");
                        //}
                    }
     }
    

    var description_field=tags_field=name_field=visibility_field=base_settings;
    
    name_field["name"]="name";
    name_field["type"]="text";
    name_field["width"]="490";
    name_field["onsubmit"]=function(settings, original){
         settings['submitdata']=get_suggestion_id(this);
         //Guardamos el valor modificado en una var. temporal
         tmp=$(this).find("input").val();
         //~ console.log(tmp)
         asd=this
    }
    $('.editable_list_name').editable('/ajax/suggestion/list/modify/', name_field);
    
    description_field["name"]="description";
    description_field["type"]="textarea";
    description_field["height"]="40";
    description_field["width"]="390";
    description_field["placeholder"]=gettext("Sin descripción");
    description_field["onsubmit"]=function(settings, original){
         settings['submitdata']=get_suggestion_id(this);
         //Guardamos el valor modificado en una var. temporal
         tmp=$(this).find("textarea").val();
    }
    $('.editable_description').editable('/ajax/add/suggestion/', description_field);
    
    description_field["placeholder"]=gettext("Esta lista aún no tiene descripción");
    $('.editable_list_description').editable('/ajax/suggestion/list/modify/', description_field);
    
    tags_field["name"]="tags";
    tags_field["type"]="text";
    tags_field["height"]="20";
    tags_field["width"]="none";
    tags_field["placeholder"]=gettext("Esta sugerencia no tiene tags");
    tags_field["onsubmit"]=function(settings, original){
         settings['submitdata']=get_suggestion_id(this);
         //Guardamos el valor modificado en una var. temporal
         tmp=$(this).find("input").val()
    }
    $('.editable_tags').editable('/ajax/add/suggestion/', tags_field);
    
    tags_field["placeholder"]=gettext("Esta lista de sugerencias no tiene tags");
    $('.editable_list_tags').editable('/ajax/suggestion/list/modify/', tags_field);             
    
    visibility_field["name"]="visibility";
    visibility_field["type"]="select";
    visibility_field["data"]="{'public':'"+gettext("Pública")+"','private':'"+gettext("Privada")+"'}";
    visibility_field["onsubmit"]=function(settings, original){
         settings['submitdata']=get_suggestion_id(this);
         //Guardamos el valor modificado en una var. temporal
         var privacy=$(this).find("select").val()
         if(privacy=="private")
            tmp=gettext("Privada");
         else
            tmp=gettext("Pública");
    }
    $('.editable_visibility').editable('/ajax/add/suggestion/', visibility_field);
    $('.editable_list_visibility').editable('/ajax/suggestion/list/modify/', visibility_field);             
}
