$(document).ready(function() {
    $('#forgotPasswordForm').on('submit', function(e) {
        e.preventDefault();
        
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                // Redirect to success page
                var redirectUrl = $('#successPassReset').data('href');
                window.location.href = redirectUrl;
            },
            error: function(xhr) {
                $('#emailForgotGroup').addClass('has-error');
                alert('Error: ' + (xhr.responseJSON?.detail || 'Please try again'));
            }
        });
    });
});