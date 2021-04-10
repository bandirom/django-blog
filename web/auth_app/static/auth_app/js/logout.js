$(function () {
  $('#logoutSubmit').click(logout);
});


function logout(e) {
  e.preventDefault();
  $.ajax({
    url: $('#logoutForm').attr("action"),
    type: "POST",
    dataType: 'json',
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}
