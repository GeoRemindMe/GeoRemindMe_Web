/*
 * Jeditable - jQuery in place edit plugin
 *
 * Copyright (c) 2006-2009 Mika Tuupola, Dylan Verheul
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *   http://www.appelsiini.net/projects/jeditable
 *
 * Based on editable by Dylan Verheul <dylan_at_dyve.net>:
 *    http://www.dyve.net/jquery/?editable
 *
 */

/**
  * Version 1.7.1
  *
  * ** means there is basic unit tests for this parameter. 
  *
  * @name  Jeditable
  * @type  jQuery
  * @param String  target             (POST) URL or function to send edited content to **
  * @param Hash    options            additional options 
  * @param String  options[method]    method to use to send edited content (POST or PUT) **
  * @param Function options[callback] Function to run after submitting edited content **
  * @param String  options[name]      POST parameter name of edited content
  * @param String  options[id]        POST parameter name of edited div id
  * @param Hash    options[submitdata] Extra parameters to send when submitting edited content.
  * @param String  options[type]      text, textarea or select (or any 3rd party input type) **
  * @param Integer options[rows]      number of rows if using textarea ** 
  * @param Integer options[cols]      number of columns if using textarea **
  * @param Mixed   options[height]    'auto', 'none' or height in pixels **
  * @param Mixed   options[width]     'auto', 'none' or width in pixels **
  * @param String  options[loadurl]   URL to fetch input content before editing **
  * @param String  options[loadtype]  Request type for load url. Should be GET or POST.
  * @param String  options[loadtext]  Text to display while loading external content.
  * @param Mixed   options[loaddata]  Extra parameters to pass when fetching content before editing.
  * @param Mixed   options[data]      Or content given as paramameter. String or function.**
  * @param String  options[indicator] indicator html to show when saving
  * @param String  options[tooltip]   optional tooltip text via title attribute **
  * @param String  options[event]     jQuery event such as 'click' of 'dblclick' **
  * @param String  options[submit]    submit button value, empty means no button **
  * @param String  options[cancel]    cancel button value, empty means no button **
  * @param String  options[cssclass]  CSS class to apply to input form. 'inherit' to copy from parent. **
  * @param String  options[style]     Style to apply to input form 'inherit' to copy from parent. **
  * @param String  options[select]    true or false, when true text is highlighted ??
  * @param String  options[placeholder] Placeholder text or html to insert when element is empty. **
  * @param String  options[onblur]    'cancel', 'submit', 'ignore' or function ??
  *             
  * @param Function options[onsubmit] function(settings, original) { ... } called before submit
  * @param Function options[onreset]  function(settings, original) { ... } called before reset
  * @param Function options[onerror]  function(settings, original, xhr) { ... } called on error
  *             
  * @param Hash    options[ajaxoptions]  jQuery Ajax options. See docs.jquery.com.
  *             
  */

(function( $ ){

    $.fn.editable = function(target, options) {
            
        if ('disable' == target) {
            $(this).data('disabled.editable', true);
            return;
        }
        if ('enable' == target) {
            $(this).data('disabled.editable', false);
            return;
        }
        if ('destroy' == target) {
            $(this)
                .unbind($(this).data('event.editable'))
                .removeData('disabled.editable')
                .removeData('event.editable');
            return;
        }
        
        var settings = $.extend({}, $.fn.editable.defaults, {target:target}, options);
        
        /* setup some functions */
        var plugin   = $.editable.types[settings.type].plugin || function() { };
        var submit   = $.editable.types[settings.type].submit || function() { };
        var buttons  = $.editable.types[settings.type].buttons 
                    || $.editable.types['defaults'].buttons;
        var content  = $.editable.types[settings.type].content 
                    || $.editable.types['defaults'].content;
        var element  = $.editable.types[settings.type].element 
                    || $.editable.types['defaults'].element;
        var reset    = $.editable.types[settings.type].reset 
                    || $.editable.types['defaults'].reset;
        var callback = settings.callback || function() { };
        var onedit   = settings.onedit   || function() { }; 
        var onsubmit = settings.onsubmit || function() { };
        var onreset  = settings.onreset  || function() { };
        var onerror  = settings.onerror  || reset;
          
        /* show tooltip */
        if (settings.tooltip) {
            $(this).attr('title', settings.tooltip);
        }
        
        settings.autowidth  = 'auto' == settings.width;
        settings.autoheight = 'auto' == settings.height;
        
        return this.each(function() {
            //~ console.debug(this)

            /* save this to self because this changes when scope changes */
            var self = this;  
                   
            /* inlined block elements lose their width and height after first edit */
            /* save them for later use as workaround */
            var savedwidth  = $(self).width();
            var savedheight = $(self).height();
            
            /* save so it can be later used by $.editable('destroy') */
            $(this).data('event.editable', settings.event);
            
            /* if element is empty add something clickable (if requested) */
            if (!$.trim($(this).html())) {
                $(this).html(settings.placeholder);
            }
            
            $(this).bind(settings.event, function(e) {
                
                /* abort if disabled for this element */
                if (true === $(this).data('disabled.editable')) {
                    return;
                }
                
                /* prevent throwing an exeption if edit field is clicked again */
                if (self.editing) {
                    return;
                }
                
                /* abort if onedit hook returns false */
                if (false === onedit.apply(this, [settings, self])) {
                   return;
                }
                
                /* prevent default action and bubbling */
                e.preventDefault();
                e.stopPropagation();
                
                /* remove tooltip */
                if (settings.tooltip) {
                    $(self).removeAttr('title');
                }
                
                /* figure out how wide and tall we are, saved width and height */
                /* are workaround for http://dev.jquery.com/ticket/2190 */
                if (0 == $(self).width()) {
                    //$(self).css('visibility', 'hidden');
                    settings.width  = savedwidth;
                    settings.height = savedheight;
                } else {
                    if (settings.width != 'none') {
                        settings.width = 
                            settings.autowidth ? $(self).width()  : settings.width;
                    }
                    if (settings.height != 'none') {
                        settings.height = 
                            settings.autoheight ? $(self).height() : settings.height;
                    }
                }
                //$(this).css('visibility', '');
                
                /* remove placeholder text, replace is here because of IE */
                if ($(this).html().toLowerCase().replace(/(;|")/g, '') == 
                    settings.placeholder.toLowerCase().replace(/(;|")/g, '')) {
                        $(this).html('');
                }
                                
                self.editing    = true;
                self.revert     = $(self).html();
                $(self).html('');

                /* create the form object */
                var form = $('<form />');
                
                /* apply css or style or both */
                if (settings.cssclass) {
                    if ('inherit' == settings.cssclass) {
                        form.attr('class', $(self).attr('class'));
                    } else {
                        form.attr('class', settings.cssclass);
                    }
                }

                if (settings.style) {
                    if ('inherit' == settings.style) {
                        form.attr('style', $(self).attr('style'));
                        /* IE needs the second line or display wont be inherited */
                        form.css('display', $(self).css('display'));                
                    } else {
                        form.attr('style', settings.style);
                    }
                }

                /* add main input element to form and store it in input */
                var input = element.apply(form, [settings, self]);

                /* set input content via POST, GET, given data or existing value */
                var input_content;
                
                if (settings.loadurl) {
                    var t = setTimeout(function() {
                        input.disabled = true;
                        content.apply(form, [settings.loadtext, settings, self]);
                    }, 100);

                    var loaddata = {};
                    loaddata[settings.id] = self.id;
                    if ($.isFunction(settings.loaddata)) {
                        $.extend(loaddata, settings.loaddata.apply(self, [self.revert, settings]));
                    } else {
                        $.extend(loaddata, settings.loaddata);
                    }
                    $.ajax({
                       type : settings.loadtype,
                       url  : settings.loadurl,
                       data : loaddata,
                       async : false,
                       success: function(result) {
                          window.clearTimeout(t);
                          input_content = result;
                          input.disabled = false;
                       }
                    });
                } else if (settings.data) {
                    input_content = settings.data;
                    if ($.isFunction(settings.data)) {
                        input_content = settings.data.apply(self, [self.revert, settings]);
                    }
                } else {
                    input_content = self.revert; 
                }
                content.apply(form, [input_content, settings, self]);

                input.attr('name', settings.name);
        
                /* add buttons to the form */
                buttons.apply(form, [settings, self]);
         
                /* add created form to self */
                $(self).append(form);
         
                /* attach 3rd party plugin if requested */
                plugin.apply(form, [settings, self]);

                /* focus to first visible form element */
                $(':input:visible:enabled:first', form).focus();

                /* highlight input contents when requested */
                if (settings.select) {
                    input.select();
                }
        
                /* discard changes if pressing esc */
                input.keydown(function(e) {
                    if (e.keyCode == 27) {
                        e.preventDefault();
                        //self.reset();
                        reset.apply(form, [settings, self]);
                    }
                });

                /* discard, submit or nothing with changes when clicking outside */
                /* do nothing is usable when navigating with tab */
                var t;
                if ('cancel' == settings.onblur) {
                    input.blur(function(e) {
                        /* prevent canceling if submit was clicked */
                        t = setTimeout(function() {
                            reset.apply(form, [settings, self]);
                        }, 500);
                    });
                } else if ('submit' == settings.onblur) {
                    input.blur(function(e) {
                        /* prevent double submit if submit was clicked */
                        t = setTimeout(function() {
                            form.submit();
                        }, 200);
                    });
                } else if ($.isFunction(settings.onblur)) {
                    input.blur(function(e) {
                        settings.onblur.apply(self, [input.val(), settings]);
                    });
                } else {
                    input.blur(function(e) {
                      /* TODO: maybe something here */
                    });
                }

                form.submit(function(e) {

                    if (t) { 
                        clearTimeout(t);
                    }

                    /* do no submit */
                    e.preventDefault(); 
            
                    /* call before submit hook. */
                    /* if it returns false abort submitting */                    
                    if (false !== onsubmit.apply(form, [settings, self])) { 
                        /* custom inputs call before submit hook. */
                        /* if it returns false abort submitting */
                        if (false !== submit.apply(form, [settings, self])) { 

                          /* check if given target is function */
                          if ($.isFunction(settings.target)) {
                              var str = settings.target.apply(self, [input.val(), settings]);
                              $(self).html(str);
                              self.editing = false;
                              callback.apply(self, [self.innerHTML, settings]);
                              /* TODO: this is not dry */                              
                              if (!$.trim($(self).html())) {
                                  $(self).html(settings.placeholder);
                              }
                          } else {
                              /* add edited content and id of edited element to POST */
                              var submitdata = {};
                              submitdata[settings.name] = input.val();
                              submitdata[settings.id] = self.id;
                              /* add extra data to be POST:ed */
                              if ($.isFunction(settings.submitdata)) {
                                  $.extend(submitdata, settings.submitdata.apply(self, [self.revert, settings]));
                              } else {
                                  $.extend(submitdata, settings.submitdata);
                              }

                              /* quick and dirty PUT support */
                              if ('PUT' == settings.method) {
                                  submitdata['_method'] = 'put';
                              }

                              /* show the saving indicator */
                              $(self).html(settings.indicator);
                              
                              /* defaults for ajaxoptions */
                              var ajaxoptions = {
                                  type    : 'POST',
                                  data    : submitdata,
                                  dataType: 'html',
                                  url     : settings.target,
                                  success : function(result, status) {
                                      if (ajaxoptions.dataType == 'html') {
                                        $(self).html(result);
                                      }
                                      self.editing = false;
                                      callback.apply(self, [result, settings]);
                                      if (!$.trim($(self).html())) {
                                          $(self).html(settings.placeholder);
                                      }
                                  },
                                  error   : function(xhr, status, error) {
                                      onerror.apply(form, [settings, self, xhr]);
                                  }
                              };
                              
                              /* override with what is given in settings.ajaxoptions */
                              $.extend(ajaxoptions, settings.ajaxoptions);   
                              $.ajax(ajaxoptions);          
                              
                            }
                        }
                    }
                    
                    /* show tooltip again */
                    $(self).attr('title', settings.tooltip);
                    
                    return false;
                });
            });
            
            /* privileged methods */
            this.reset = function(form) {
                /* prevent calling reset twice when blurring */
                if (this.editing) {
                    /* before reset hook, if it returns false abort reseting */
                    if (false !== onreset.apply(form, [settings, self])) { 
                        $(self).html(self.revert);
                        self.editing   = false;
                        if (!$.trim($(self).html())) {
                            $(self).html(settings.placeholder);
                        }
                        /* show tooltip again */
                        if (settings.tooltip) {
                            $(self).attr('title', settings.tooltip);                
                        }
                    }                    
                }
            };            
        });

    };


    $.editable = {
        types: {
            defaults: {
                element : function(settings, original) {
                    var input = $('<input type="hidden"></input>');                
                    $(this).append(input);
                    return(input);
                },
                content : function(string, settings, original) {
                    $(':input:first', this).val(string);
                },
                reset : function(settings, original) {
                  original.reset(this);
                },
                buttons : function(settings, original) {
                    var form = this;
                    if (settings.submit) {
                        /* if given html string use that */
                        if (settings.submit.match(/>$/)) {
                            var submit = $(settings.submit).click(function() {
                                if (submit.attr("type") != "submit") {
                                    form.submit();
                                }
                            });
                        /* otherwise use button with given string as text */
                        } else {
                            var submit = $('<button type="submit" />');
                            submit.html(settings.submit);                            
                        }
                        $(this).append(submit);
                    }
                    if (settings.cancel) {
                        /* if given html string use that */
                        if (settings.cancel.match(/>$/)) {
                            var cancel = $(settings.cancel);
                        /* otherwise use button with given string as text */
                        } else {
                            var cancel = $('<button type="cancel" />');
                            cancel.html(settings.cancel);
                        }
                        $(this).append(cancel);

                        $(cancel).click(function(event) {
                            //original.reset();
                            if ($.isFunction($.editable.types[settings.type].reset)) {
                                var reset = $.editable.types[settings.type].reset;                                                                
                            } else {
                                var reset = $.editable.types['defaults'].reset;                                
                            }
                            reset.apply(form, [settings, original]);
                            return false;
                        });
                    }
                }
            },
            text: {
                element : function(settings, original) {
                    var input = $('<input />');
                    if (settings.width  != 'none') { input.width(settings.width);  }
                    if (settings.height != 'none') { input.height(settings.height); }
                    /* https://bugzilla.mozilla.org/show_bug.cgi?id=236791 */
                    //input[0].setAttribute('autocomplete','off');
                    input.attr('autocomplete','off');
                    $(this).append(input);
                    return(input);
                }
            },
            textarea: {
                element : function(settings, original) {
                    var textarea = $('<textarea />');
                    if (settings.rows) {
                        textarea.attr('rows', settings.rows);
                    } else if (settings.height != "none") {
                        textarea.height(settings.height);
                    }
                    if (settings.cols) {
                        textarea.attr('cols', settings.cols);
                    } else if (settings.width != "none") {
                        textarea.width(settings.width);
                    }
                    $(this).append(textarea);
                    return(textarea);
                }
            },
            select: {
               element : function(settings, original) {
                    var select = $('<select />');
                    $(this).append(select);
                    return(select);
                },
                content : function(data, settings, original) {
                    /* If it is string assume it is json. */
                    if (String == data.constructor) {      
                        eval ('var json = ' + data);
                    } else {
                    /* Otherwise assume it is a hash already. */
                        var json = data;
                    }
                    for (var key in json) {
                        if (!json.hasOwnProperty(key)) {
                            continue;
                        }
                        if ('selected' == key) {
                            continue;
                        } 
                        var option = $('<option />').val(key).append(json[key]);
                        $('select', this).append(option);    
                    }                    
                    /* Loop option again to set selected. IE needed this... */ 
                    $('select', this).children().each(function() {
                        if ($(this).val() == json['selected'] || 
                            $(this).text() == $.trim(original.revert)) {
                                $(this).attr('selected', 'selected');
                        }
                    });
                }
            }
        },

        /* Add new input type */
        addInputType: function(name, input) {
            $.editable.types[name] = input;
        }
    };

    // publicly accessible defaults
    $.fn.editable.defaults = {
        name       : 'value',
        id         : 'id',
        type       : 'text',
        width      : 'auto',
        height     : 'auto',
        event      : 'click.editable',
        onblur     : 'cancel',
        loadtype   : 'GET',
        loadtext   : 'Loading...',
        placeholder: 'Click to edit',
        loaddata   : {},
        submitdata : {},
        ajaxoptions: {}
    };

})( jQuery );

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

