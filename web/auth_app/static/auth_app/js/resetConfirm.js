$(function () {
  $('#resetConfirmForm').submit(confirmReset);
});

function confirmReset(e) {
  let form = $(this);
  e.preventDefault();
  const urlParams = new URLSearchParams(window.location.search);
  const data = {
    uid: urlParams.get('uid'),
    token: urlParams.get('token'),
//    password_1: this.password_1.value,
    password_1: $("input[name=password_1]").val(),
    password_2: $("input[name=password_2]").val(),
  }

  $.ajax({
    url: "/api/v1/auth/password/reset/confirm/",
    type: "POST",
    data: data,
    success: successPasswordResetHandler,
    error: error_process,
  })
}

let error_class_name = "has-error"

function successPasswordResetHandler(data) {
  let msg = data.detail + '\n You will be redirect to Sign In page'
  $('#successReset').append('<div class="help-block">' + msg + "</div>");
  window.setTimeout(function () {
    location.href = '/login';
  }, 3000);
}

function error_process(data) {
  $(".help-block").remove()
  let groups = ['#password1Group', '#password2Group']
  for (let group of groups) {
    $(group).removeClass(error_class_name);
  }
  if (data.responseJSON.token || data.responseJSON.uid) {
    help_block("#tokenValidationError", 'Token expired or invalid')
  }
  if (data.responseJSON.new_password1) {
    help_block("#password1Group", data.responseJSON.new_password1)
  }
  if (data.responseJSON.new_password2) {
    help_block("#password2Group", data.responseJSON.new_password2)
  }
}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
