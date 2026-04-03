$(function() {
    console.log('Password reset form initialized');
    
    $('#resetPasswordForm').on('submit', function(e) {
        e.preventDefault();
        console.log('Form submitted');
        
        var $form = $(this);
        var password1 = $('#password_1').val();
        var password2 = $('#password_2').val();
        var token = $('input[name="token"]').val();
        var uid = $('input[name="uid"]').val();
        
        console.log('Form data:', {
            token: token,
            uid: uid,
            password1: password1,
            password2: password2
        });
        
        // Validate passwords match
        if (password1 !== password2) {
            showMessage('Passwords do not match!', 'danger');
            console.log('Password mismatch');
            return;
        }
        
        // Validate password length
        if (password1.length < 8) {
            showMessage('Password must be at least 8 characters long!', 'danger');
            console.log('Password too short');
            return;
        }
        
        // Show loading state
        var submitBtn = $(this).find('input[type="submit"]');
        var originalText = submitBtn.val();
        submitBtn.val('Resetting...').prop('disabled', true);
        
        // Get login URL
        var loginUrl = $form.data('login-url') || window.loginUrl;
        console.log('Login URL:', loginUrl);
        
        // Get CSRF token
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        console.log('CSRF token exists:', !!csrftoken);
        
        // Send JSON request
        $.ajax({
            url: $form.attr('action'),
            method: 'POST',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: JSON.stringify({
                token: token,
                uid: uid,
                password_1: password1,
                password_2: password2
            }),
            success: function(response, status, xhr) {
                console.log('Success response:', response);
                console.log('Response status:', status);
                console.log('HTTP status:', xhr.status);
                
                showMessage('Password reset successful! Redirecting to login...', 'success');

                var redirectUrl = response.redirect_url || '/login/';
                console.log('Redirecting to:', redirectUrl);
                
                setTimeout(function() {
                    console.log('Redirecting to:', loginUrl);
                    window.location.href = loginUrl;
                }, 2000);
            },
            error: function(xhr, status, error) {
                console.error('Error details:', {
                    status: xhr.status,
                    statusText: xhr.statusText,
                    response: xhr.responseJSON,
                    error: error
                });
                
                var errorMsg = 'An error occurred. Please try again.';
                if (xhr.responseJSON) {
                    if (xhr.responseJSON.password_1) {
                        errorMsg = 'Password: ' + xhr.responseJSON.password_1[0];
                    } else if (xhr.responseJSON.password_2) {
                        errorMsg = 'Confirm password: ' + xhr.responseJSON.password_2[0];
                    } else if (xhr.responseJSON.detail) {
                        errorMsg = xhr.responseJSON.detail;
                    } else if (xhr.responseJSON.non_field_errors) {
                        errorMsg = xhr.responseJSON.non_field_errors[0];
                    }
                }
                
                showMessage(errorMsg, 'danger');
                submitBtn.val(originalText).prop('disabled', false);
            }
        });
    });
    
    function showMessage(message, type) {
        console.log('Showing message:', message, type);
        
        var alertClass = type === 'danger' ? 'alert-danger' : 'alert-success';
        var messageHtml = '<div class="alert ' + alertClass + ' alert-dismissible fade in">' +
                          '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                          '<span aria-hidden="true">&times;</span></button>' +
                          '<i class="glyphicon glyphicon-' + (type === 'danger' ? 'exclamation-sign' : 'ok-sign') + '"></i> ' +
                          message + '</div>';
        
        $('#messageContainer').html(messageHtml);
        
        // Auto-hide after 5 seconds for success messages
        if (type === 'success') {
            setTimeout(function() {
                $('#messageContainer .alert').fadeOut();
            }, 5000);
        }
    }
});