$(function () {
  // $(document).on("click", "a.login", login);
  $('#loginForm').submit(login);
  $('#forgotPasswordForm').submit(passwordReset);
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

function passwordReset(e) {
  e.preventDefault();
  let form = $(this);
  $.ajax({
    url: form.attr("action"),
    type: form.attr('method'),
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      url = $('#successPassReset').data('href')
      window.location.href = url;
    },
    error: function (data) {
      $("#emailForgotGroup").addClass("has-error");
      $(".help-block").remove()
      $("#emailForgotGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );
    }
  })
}
