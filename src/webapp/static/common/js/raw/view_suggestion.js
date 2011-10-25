function toggle_showMore(){
    if($('#show-more-text').css('display')!="none")
        $('.show-more').html(gettext("Más información"))
    else
        $('.show-more').html(gettext("[Ocultar]"))
    
    $('#show-more-text').toggle('slow')
}
function addSuggestionToList(obj){
    GRM.wait();
    $.ajax({
        type: "POST",
        url: url["modify_suggestion_list"],
        data: {
            list_id: [$(obj).attr('value')],
            suggestions: [$('#add-to-list').attr('value')]
        },
        dataType:'json',
        complete: function(){GRM.nowait();},
        success: function(data){
            
            if($('.no-lists').is(':visible'))
                $('.no-lists').hide();
            
            $(obj).find("span.name").addClass("checked");
            
            //Actualizamos el contador de la lista
            counterClass='.list-'+data.id+'-counter';
            $(counterClass).text(data.keys.length);
            
            //Añadimos la lista a "Listas en las que aparece"
            var htmlCode='<a href="../list/'+data.id+'" value="'+data.id+'">'+data.name+'</a>';
            if($('#list-lists').children().length==0)
                htmlCode="<span>"+htmlCode+"</span>";
            else
                htmlCode="<span>, "+htmlCode+"</span>";
            $('#list-lists').append(htmlCode);
            
            //Mostrar mensaje de éxito
            showMessage(gettext("Las sugerencia han sido añadida a la lista","success"))
        }
    });    
}

function removeSuggestionToList(obj){
    GRM.wait();
    $.ajax({
        type: "POST",
        url: url["modify_suggestion_list"],
        data: {
            list_id: [$(obj).attr('value')],
            suggestions_del: [$('#add-to-list').attr('value')]
        },
        dataType:'json',
        complete: function(){GRM.nowait();},
        success: function(data){
            
            
            
            $(obj).find("span.name").removeClass("checked");
            
            //Actualizamos el contador de la lista
            counterClass='.list-'+data.id+'-counter';
            $(counterClass).text(data.keys.length);
            
            //Eliminamos la lista de "Listas en las que aparece"
            $('#in-lists a[value="'+$(obj).attr('value')+'"]').parent().remove();
            
            if($('#list-lists').children().length==0)
                $('.no-lists').show();
                
            //Mostrar mensaje de éxito
            showMessage(gettext("Las sugerencia ha sido eliminada de la lista","success"))
        }
    });    
}

//Añadimos el comportamiento	
function onLiClick(obj){
    var checkbox=$(obj).find("span.name");

    if($(checkbox).hasClass("checked"))
        removeSuggestionToList(obj)
    else
        addSuggestionToList(obj)            
}
$(document).ready(function(){
    //if (typeof resizeIframe != "undefined") resizeIframe();
    $('#comment-list li,#popular-comments li').hover(
        function(){$(this).find('.action-bar').show()},
        function(){$(this).find('.action-bar').hide()}
    );
    
    //Set like & dislike, remember and removable behaviour
    $(".like-dislike").like();
    $(".remember-forget").remember();
    $(".removable").removable();
    
    $(".like-dislike-suggestion").like({
        callback: function() {
            if($(".like-dislike-suggestion").attr('like')=="true"){
                var value = parseInt($('#vote-counter').text())+1;
                $('#vote-counter').text(value);
                
                if(value>0){
                    $('#suggestion-vote-counter .none').hide();
                    $('#suggestion-vote-counter .votes-msg').show();
                }
            }else{
                var value = parseInt($('#vote-counter').text())-1;
                $('#vote-counter').text(value);
                
                if(value==0){
                    $('#suggestion-vote-counter .none').show();
                    $('#suggestion-vote-counter .votes-msg').hide();
                }
            }
        }
    });
    
    loadPanoramioPhotos(latlngStr);

    $('span.btn.dropDownBtn').menuList({
        onLiClick: function(){
            //Buscamos el checkbox y lo marcamos/desmarcamos
            onLiClick(this);
        },
        onNewList: function(listname){
           
            $.ajax({
                type: "POST",
                url: url["modify_suggestion_list"],
                data: {
                    name: [listname]
                },
                dataType:'json',
                success: function(data){
                    //Añadimos la lista al desplegable
                    var c=$("<li value=\""+data.id+"\"><span class=\"checkbox name\">"+data.name+"</span> (<span class=\"list-"+data.id+"-counter\">"+data.keys.length+"</span> "+gettext("sugerencias")+"</li>").insertBefore('.new-list-btn');
                    c.click(function(){onLiClick(this)});
                    
                    //Forzamos el click para que se añada la sugerencia a la lista
                    c.click();
                    
                    //Reordenamos alfabéticamente la lista desplegable
                    $('.submenu li').not('li.new-list-btn').sortElements(function(a, b){
                        return $(a).text().toLowerCase() > $(b).text().toLowerCase() ? 1 : -1;
                    });
                    
                    $("#dropdown-list").removeClass('visible-display');
                }
            });
        }
    });
});

