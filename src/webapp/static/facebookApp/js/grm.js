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
        var inc = $(this).find('.increase');
        $.each(inc, function(index,item){
            $(item).text(parseInt($(item).text())+1);
        });
        
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
                    success: function(){
                        
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

jQuery.fn.like = GRM.like;

function loadPage(dict){
            var page=dict['page'];
            var container=dict['container']
            var url=dict['url']
            var template=dict['template']
            var data=dict["data"]
            
            if ( typeof loadPage.currentPage == 'undefined' ) {
            // It has not... perform the initilization
                loadPage.currentPage=1
            }
            if (page=='next')
                loadPage.currentPage++;
            else if(page=='prev' && loadPage.currentPage>1)
                loadPage.currentPage--;
            else
                loadPage.currentPage=page;
            
            page=loadPage.currentPage;
            data['page']=page;
            
            $.ajax({
                type: 'POST',
                url: url,
                data:data,
                success: function(data){
                    
                    $(container).empty()
                    $.each(data[1], function(index,suggestion){
                        $(template).tmpl( {element:suggestion} ).appendTo(container);
                    });
                    
                    //Ocultamos los botones de siguiente y anterior si es necesario
                    if(page>1)
                        $('#prev-page').removeClass('hidden')
                    else
                        $('#prev-page').addClass('hidden')
                    
                    return page;
                }
            });
        }

//Creamos nuestro propio namespace       
//~ if (typeof GRM == "undefined" || !GRM ) {
    //~ window.GRM = {};
//~ };

/*
 *  Esta función hace una petición AJAX y carga una plantilla con los
 *  datos recibidos.
 * 
 *  Ejemplo de llamada:
 *  GRM.loadPage({
 *               page:page,
 *               container:'#suggestion-list',
 *               url:'/ajax/get/suggestion/',
 *               template: "#suggestionTemplate",
 *               data:{
 *                       'query_id':{{suggestions.0}},
 *                   }                
 *           });
 */
 //~ jQuery.extend({
     //~ loadPage : function(dict){
        //~ var page=dict['page'];
        //~ var container=dict['container']
        //~ var url=dict['url']
        //~ var template=dict['template']
        //~ var data=dict["data"]
        //~ console.log(dict)
        //~ 
        //~ if ( typeof GRM.loadPage.currentPage == 'undefined' ) {
            //~ // Creamos una variable estática
            //~ GRM.loadPage.currentPage=1
        //~ }
        //~ if (page=='next')
            //~ GRM.loadPage.currentPage++;
        //~ else if(page=='prev' && loadPage.currentPage>1)
            //~ GRM.loadPage.currentPage--;
        //~ else
            //~ GRM.loadPage.currentPage=page;
        //~ 
        //~ page=GRM.loadPage.currentPage;
        //~ data['page']=page;
        //~ 
        //~ $.ajax({
            //~ type: 'POST',
            //~ url: url,
            //~ data:data,
            //~ success: function(data){
                //~ 
                //~ $(container).empty()
                //~ $.each(data[1], function(index,suggestion){
                    //~ $(template).tmpl( {suggestion} ).appendTo(container);
                //~ });
                //~ 
                //~ //Ocultamos los botones de siguiente y anterior si es necesario
                //~ if(page>1)
                    //~ $('#prev-page').removeClass('hidden')
                //~ else
                    //~ $('#prev-page').addClass('hidden')
                //~ 
                //~ return page;
            //~ }
        //~ });
    //~ }
//~ });
