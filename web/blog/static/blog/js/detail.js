$(function () {
  $('#formReview').submit(leftComment);
});

function addParentToComment(commentAuthor, parent_id) {
  document.getElementById("commentParent").value = parent_id;
  document.getElementById("textComment").innerText = commentAuthor + ', ';
}

function leftComment(e) {
  e.preventDefault()
  let form = $(this);
  $.ajax({
    url: form.attr("action"),
    type: form.attr("method"),
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      console.log(data, 'error')
      if (data.responseJSON.email) {
        help_block("#emailGroup", data.responseJSON.email)
      }
      if (data.responseJSON.content) {
        help_block("#emailGroup", data.responseJSON.content)
      }
    }
  })
}

const error_class_name = "has-error"
function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
