$(function () {
  verifyEmail()
});

function verifyEmail() {
  const api_url = $('#verifyConfirm').data('href')
  const urlSearchParams = new URLSearchParams(window.location.search);
  let data = {'key': urlSearchParams.get('key')}
  $.ajax({
    url: api_url,
    type: 'post',
    dataType: 'json',
    data: data,
    success: function (data) {
      console.log(data, 'success')
      url = $('#singIn').data('href');
      window.location.href = url;
    },
    error: function (data) {
      $('#ifErrors').append('<h3>Confirmation url expired or link is not valid</h3>');
    }
  })
}

