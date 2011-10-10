$(document).ready(function() {
    
    /*** login function ***/
    $('#loginForm').submit(function(e){
        e.preventDefault();
        GRM.wait();
        $.ajax({
            type: "POST",
            url: "/ajax/login/",
            dataType:'json',
            data: {
                "user_login-email":$(this).find('[name="email"]').val(),
                "user_login-password":$(this).find('[name="password"]').val(),
                "csrfmiddlewaretoken":$(this).find('[name="csrfmiddlewaretoken"]').val()
            },
            error: function() { GRM.nowait(); },
            success: function(msg){
                if(msg.error!="") {
                    showMessage(msg.error,"error");
                    GRM.nowait();
                }
                else {
                    window.location=msg._redirect;
                }
            }
        });
    });
    
    /*** terms check ***/
    $('#textTermsCheckbox').click(function(){
        var item = $(this).parent().find('input');
        item.attr('checked',!item.is(':checked'));
    });
    
    /*** select social ***/
    $('#register-menu li').click(function(e){
        
        var lastActive=$('#register-menu li.active');
        $(lastActive).removeClass("active");
        if($(lastActive).attr("id")!=$(this).attr("id")){
            //Si no está deseleccionado lo activamos
            $(this).addClass("active");
        }
    });
    
    
    /*** slide up/down register ***/
    $('.register-text-aux').toggle(function(){
            $('#registerForm').slideDown(400);
            $("#register-with-social").slideUp(400);
            $(this).addClass("close");
        },function(){
            $('#registerForm').slideUp(400);
            $("#register-with-social").slideDown(400);
            $(this).removeClass("close");
    })
    
    /*** social register button ***/
    $('#register-btn').click(function(e){
        e.preventDefault();
        
        var network=$('#register-menu li.active');
        if(network.length==0){
            //Mensaje
            showMessage(gettext("Primero selecciona una de la redes"),"error")
        }else{
            var register_link="/login/"+network.attr('id')+"/";
            $(this).attr('href',register_link)
            if($(this).attr('onclick') === undefined || $(this).attr('onclick')==null){
                window.location=$(this).attr('href');
            } else {
                $(this).click ();
            }
        }
        
    })

    /*** show georemindme login ***/
    $('.georemindme').click(function(){
       $('#login-bar p').hide();
       $('#login-bar ul').hide();
       $('#georemindme-form').show();
    });
    
    /*** check passwords ***/
    $('#userRegisterPass1,#userRegisterPass2').blur(function() { checkPasswords(false) });
    $('#userRegisterPass1,#userRegisterPass2').keyup(function() { $('#passwordStatus').hide() });
    /*** check email ***/
    $('#registerEmail').blur(function() { checkEmail(); });
    $('#registerEmail').keyup(function() { $('#emailStatus').hide(); $('#registerEmail').next('div').hide();$('#registerEmail').next('div').text(''); });


    /*** register form ***/
    $('#registerFormForm').submit(function (e){

       if (typeof(REQUEST) != "undefined" && REQUEST)
          REQUEST.abort();
       
       e.preventDefault();
       
       var a = checkPasswords();
       var b = checkEmail(true);
       var c = checkTerms();
       
       if (!a || !b || !c){
          return;
      }
       
       var data = {
          "user_register-email":function() { return $('#registerEmail').val() },
          "user_register-password":function() { return $('#userRegisterPass1').val() },
          "user_register-password2":function() { return $('#userRegisterPass2').val() },
          "csrfmiddlewaretoken": function() { return $('#registerFormForm input[type="hidden"]').val()}
          };
       
       GRM.wait();
       
       $('#msgRegisterEmail').hide();
       $('#msgRegisterPass').hide();
       
       REQUEST = $.ajax({
          url: "/ajax/register/",
          dataType: 'json',
          data: data,
          success: function(data){
             if (typeof(data.errors)!="undefined")
             {
                if(typeof(data.errors.email)!="undefined"){
                   $('#emailStatus').removeClass("ok").addClass("no-ok").show();
                   $('#registerEmail').next('div').text(data.errors.email).show();
                }
                if (typeof(data.errors.password)!="undefined"){
                   $('#passwordStatus').show().text(data.errors.password);
                }
                
               GRM.nowait();
             }
             else
             {
                if(typeof(data._redirect)!="undefined")
                {
                   window.location = data._redirect;
                }
             }
             
             REQUEST=null;
          },
          error: function(data){GRM.nowait();REQUEST=null;},
          type:"POST",
          async:true
        });
       
       // Si es correcto => Redirect
    });
    
});

