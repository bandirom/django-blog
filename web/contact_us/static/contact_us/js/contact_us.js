$(function () {
    $('#feedBackForm').submit(postContactUs);

});

const error_class_name = "has-error"

function error_process(data) {
  $(".help-block").remove()
  console.log('error_process')
  let groups = ['#nameGroup', '#mailGroup', '#contentGroup', '#fileGroup']
  for (let group of groups) {
    $(group).removeClass(error_class_name);
  }
  if (data.responseJSON.name) {
    help_block("#nameGroup", data.responseJSON.name)
  }
  if (data.responseJSON.mail) {
    help_block("#emailGroup", data.responseJSON.mail)
  }
  if (data.responseJSON.content) {
    help_block("#contentGroup", data.responseJSON.content)
  }
  if (data.responseJSON.file) {
    help_block("#fileGroup", data.responseJSON.file)
  }

}
function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}

function postContactUs(event){
    event.preventDefault()
    let form=$(this)

    let formData = new FormData(form[0])
    $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        data: formData,
        contentType: false,
        processData: false,
        success: function (data){
            console.log('success', data)
        },
        error: function (data){
            console.log('error', data)
            error_process(data);

        }
    })
}
