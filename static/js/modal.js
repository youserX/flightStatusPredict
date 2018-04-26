$(function() {
    $('#dtp_input').click(function() {

        alert("here")

        $.ajax({
            url: '/result',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                alert("here2")
                console.log(response);

            },
            error: function(error) {
                alert("here3")
                console.log(error);
                 alert("here3")
            }
        });
    });
});