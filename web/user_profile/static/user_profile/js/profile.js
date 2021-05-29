$(function () {
  $("#fileUpload").on('change', uploadPhoto);
  $('#changePasswordForm').submit(changePassword);
});

const error_class_name = "has-error"

function uploadPhoto(e) {
  e.preventDefault()
  let data = new FormData();
  let files = $(this)[0].files;
  data.append('avatar', files[0]);

  $.ajax({
    type: 'POST',
    url: $(this).data('href'),
    data: data,
    contentType: false,
    processData: false,
    success: function (data) {
      $("#avatar").attr("src", data.avatar);
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function changePassword(e) {
  e.preventDefault()
  console.log('click')
  let form = $(this)

  $.ajax({
    type: form.attr("method"),
    url: form.attr("action"),
    data: form.serialize(),
    success: function (data) {
      console.log('success', data)
    },
    error: function (data) {
      $(".help-block").remove()
      let groups = ['#oldPasswordForm', '#newPassword1Form', '#newPassword2Form']
      for (let group of groups) {
        $(group).removeClass(error_class_name);
      }
      if (data.responseJSON.old_password) {
        help_block("#oldPasswordForm", data.responseJSON.old_password)
      }
      if (data.responseJSON.new_password1) {
        help_block("#newPassword1Form", data.responseJSON.new_password1)
      }
      if (data.responseJSON.new_password2) {
        help_block("#newPassword2Form", data.responseJSON.new_password2)
      }
    }
  })

}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
