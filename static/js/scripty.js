
$(document).ready(function(){

    console.log("loaded");
    $.material.init();
    console.log("loaded");
    $(document).on("submit", "#register-form", function(e){
        e.preventDefault();

        var form = $("#register-form").serialize();
        $.ajax({
            url: '/postregistration',
            Type: 'POST',
            data: form,
            success: function(response){
                console.log(response);
            }
        });
    });

});

