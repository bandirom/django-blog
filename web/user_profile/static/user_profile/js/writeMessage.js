$(function () {
  $('#writeMessage').click(writeMessage);

});

function writeMessage() {
  let button = $(this)
  let chatProxy = button.data('chat')
  let userId = button.data('user_id')
  const url = `${chatProxy}?user_id=${userId}`
  window.open(url, '_blank').focus();
}
