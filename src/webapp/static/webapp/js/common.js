function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ajaxSend(function(event, xhr, settings) {
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});



$(document).ready(function(){
    
    
            
    if($('.active-section').length!=0)
        $(".lavaLamp").lavaLamp({ fx: "backout", speed: 700 })
    $('.help-txt').dialog({
        autoOpen:false,
        resizable: false,
        buttons: [{
                text: "Cerrar",
                click: function() { $(this).dialog("close"); }
            }],
        draggable: false,
        width:560,
        position: ['center', 125]
    });



    
    $("[placeholder]").placeholder();
                
    $(".user-dropDownBtn, .user-submenu ").hoverIntent(hiConfig);
    $(".user-dropDownBtn").click(function(){
        //Alineamos el menu desplegable desde la esquina sup-izq.
        var tmp=$('#dropdown-list-user').width();
        tmp=52-tmp;
        $('#dropdown-list-user').css("margin-left",tmp+'px')
        
        $(this).find('ul:first:hidden').css({visibility: "visible",display: "none"}).slideDown(400);
    })
    
    $("#left-col").css("height",$("#right-col").height()+'px');
    $("#right-col").bind("resize",function(){
        $("#left-col").css("height",$(this).height()+'px');
    });
    
    $('#search-form').bind('submit', function(e){
        e.preventDefault;
        window.location="/search/"+$(this).find("input[type='text']").val();
        return false;
    });


    var userAgent = navigator.userAgent.toLowerCase();
    jQuery.browser = {
        version: (userAgent.match( /.+(?:rv|it|ra|ie|me)[\/: ]([\d.]+)/ ) || [])[1],
        chrome: /chrome/.test( userAgent ),
        safari: /webkit/.test( userAgent ) && !/chrome/.test( userAgent ),
        opera: /opera/.test( userAgent ),
        msie: /msie/.test( userAgent ) && !/opera/.test( userAgent ),
        mozilla: /mozilla/.test( userAgent ) && !/(compatible|webkit)/.test( userAgent )
    };

    
    if($.browser.msie && $.browser.version.split(".")[0]!=9){
        $("body").children(":not('div#browser-error-msg,script#browser-error')").remove()
        $("#browser-error").tmpl({
            version:$.browser.version,
            browser: "Internet Explorer",
            download_url: "http://windows.microsoft.com/en-US/internet-explorer/products/ie/home"
        }).appendTo("body");
    }else if($.browser.mozilla && $.browser.version.split(".")[0]<3){
        $("body").children(":not('div#browser-error-msg,script#browser-error')").remove()
        $("#browser-error").tmpl({
            version:$.browser.version,
            browser: "Mozilla",
            download_url: "http://www.mozilla.org/es-ES/firefox/"
        }).appendTo("body");
    }else if($.browser.chrome && $.browser.version.split(".")[0]<11){
        $("body").children(":not('div#browser-error-msg,script#browser-error')").remove()
        $("#browser-error").tmpl({
            version:$.browser.version,
            browser: "Google Chrome",
            download_url: "http://www.google.es/chrome"
        }).appendTo("body");
    }else if($.browser.safari){
    }else if($.browser.opera){
    }
    
});
