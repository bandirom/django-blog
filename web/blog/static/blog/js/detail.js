$(function () {
  $('#formReview').submit(leftComment);
});

function addParentToComment(commentAuthor, parent_id) {
  document.getElementById("commentParent").value = parent_id;
  document.getElementById("textComment").innerText = commentAuthor + ', ';
}

const error_class_name = "has-error"

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
      $(".help-block").remove()
      let groups = ['#emailGroup', '#textAreaGroup']
      for (let group of groups) {
        $(group).removeClass(error_class_name);
      }
      if (data.responseJSON.email) {
        help_block("#emailGroup", data.responseJSON.email)
      }
      if (data.responseJSON.content) {
        help_block("#textAreaGroup", data.responseJSON.content)
      }
    }
  })
}


function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
