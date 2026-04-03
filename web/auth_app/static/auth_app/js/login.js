$(function () {
  $('#loginForm').submit(login);
});

function login(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      $("#emailGroup").addClass("has-error");
      $("#passwordGroup").addClass("has-error");
      $(".help-block").remove()
      $("#passwordGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );

    }
  })
}


$(function () {
  $('#forgotPasswordForm').submit(forgot_password);
});

function forgot_password(e) {
  let form = $(this);
  e.preventDefault();

  $('#emailForgotGroup').removeClass('has-error');

  var email = $('input[name="email"]').val();
  var submitBtn = $('#resetPasswordBtn');
  var originalBtnText = submitBtn.html();

  if (!email) {
      showError('Please enter your email address.');
      return;
  }

  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
      showError('Please enter a valid email address.');
      return;
  }

  submitBtn.html('<i class="glyphicon glyphicon-refresh glyphicon-spin"></i> Sending...');
  submitBtn.prop('disabled', true);

  $.ajax({
      url: $(this).attr('action'),
      method: 'POST',
      data: $(this).serialize(),
      headers: {
          'X-Requested-With': 'XMLHttpRequest'
      },
      success: function(response) {
          // Show success message
          $('#successMessage')
              .html('<i class="glyphicon glyphicon-envelope"></i> ' + 
                    (response.detail || 'Password reset email has been sent. Please check your inbox.'))
              .show();
          
          // Clear the form
          $('input[name="email"]').val('');
          
          // Optionally redirect after 3 seconds
          setTimeout(function() {
              $('#pwdModal').modal('hide');
              
              // Check if we have a redirect URL
              var redirectUrl = $('#successPassReset').data('href');
              if (redirectUrl) {
                  window.location.href = redirectUrl;
              }
          }, 3000);
      },
      error: function(xhr) {
          var errorMsg = 'An error occurred. Please try again.';
          
          if (xhr.responseJSON) {
              if (xhr.responseJSON.detail) {
                  errorMsg = xhr.responseJSON.detail;
              } else if (xhr.responseJSON.email) {
                  errorMsg = xhr.responseJSON.email[0];
              }
          }
          
          showError(errorMsg);
          $('#emailForgotGroup').addClass('has-error');
      },
      complete: function() {
          // Reset button state
          submitBtn.html(originalBtnText);
          submitBtn.prop('disabled', false);
      }
  });
}

$('#pwdModal').on('hidden.bs.modal', function() {
    $('#emailForgotGroup').removeClass('has-error');
    $('input[name="email"]').val('');
});