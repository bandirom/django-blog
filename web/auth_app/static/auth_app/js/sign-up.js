$(function () {
  $('#signUpForm').submit(singUp);
  $('.pass-icon').click(passwordVisibility);
});

const error_class_name = "has-error"

function passwordVisibility() {
  let name = $(this).attr('data-field-name')
  let input = $("[name=" + name + "]")
  if (input.attr("type") == "password"){
      input.attr("type", "text");
  }
  else {
      input.attr("type", "password");
  }
}

function singUp(e) {
  const form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: form.attr("method"),
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      window.location.href = form.data('href');
    },
    error: function (data) {
      error_process(data);
    }
  })
}

function error_process(data) {
  $(".help-block").remove()
  let groups = ['#emailGroup', '#password1Group', '#password2Group', '#firstNameGroup', '#lastNameGroup']
  for (let group of groups) {
    $(group).removeClass(error_class_name);
  }
  if (data.responseJSON.email) {
    help_block("#emailGroup", data.responseJSON.email)
  }
  if (data.responseJSON.password1) {
    help_block("#password1Group", data.responseJSON.password1)
  }
  if (data.responseJSON.password2) {
    help_block("#password2Group", data.responseJSON.password2)
  }
  if (data.responseJSON.first_name) {
    help_block("#firstNameGroup", data.responseJSON.first_name)
  }
  if (data.responseJSON.last_name) {
    help_block("#lastNameGroup", data.responseJSON.last_name)
  }
}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
