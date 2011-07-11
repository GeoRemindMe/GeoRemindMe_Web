$(document).ready(function() {
    $("form").submit(function() {
        $('#submit-button').val("Enviado...")
        $('#submit-button').addClass("waiting")
        
        var params = { 
            name: $('#id_name').val(), 
            place_id: $('#id_place_id').val(), 
            description: $('#id_description').val(),
            starts_month: $('#id_starts_month').val(),
            starts_day: $('#id_starts_day').val(),
            starts_year: $('#id_starts_year').val(),
            ends_month: $('#id_ends_month').val(),
            ends_day: $('#id_ends_day').val(),
            ends_year: $('#id_ends_year').val(),
            visibility: $('#id_visibility').val()
        };
        
        $.ajax({
            type: "POST",
            url: "/ajax/add/suggestion/",
            data: jQuery.param(params),
            complete: function(msg){
                if (msg.status !=200){
                    $('#error-msg').text("Error "+msg.status)
                    $('#error-msg').fadeIn('slow').delay(2000).fadeOut('slow')
                }
                $('#submit-button').val("Enviar")
                $('#submit-button').removeClass("waiting")
            }
        });
         
        return false;
    });
});
