$(function () {
  $(".followMe").click(followMe);
});

function followMe() {
  console.log('click')
  let button = $(this)
  let data = {
    'user_id': button.data('id')
  }

  $.ajax({
    url: button.data('href'),
    type: 'post',
    data: data,
    success: function (data) {
      console.log(data, "success")
      button.text(data.status)
    }
  })
}
