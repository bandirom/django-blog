$(function () {
  $('#writeMessage').click(writeMessage);

});

function writeMessage() {
  jwt = localStorage.getItem('jwt')
  let button = $(this)
  let chatProxy = button.data('chat')
  let userId = button.data('user_id')
  url = chatProxy + '?auth=' + jwt + '&user_id=' + userId
  window.open(url, '_blank').focus();

}
