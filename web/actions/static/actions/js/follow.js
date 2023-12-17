$(function () {
  $(".followMe").click(followMe);
});

function followMe() {
  let button = $(this)
  let data = {
    'user_id': button.data('id')
  }
  $.ajax({
    url: '/api/v1/actions/follow',
    type: 'post',
    data: data,
    success: function (data) {
      console.log(data, "success")
      button.text(getButtonText(data.status))
    }
  })
}

function getButtonText(followStatus) {
  return followStatus === true ? 'Unfollow' : 'Follow'
}
