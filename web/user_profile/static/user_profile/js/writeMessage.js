$(function () {
  $('#writeMessage').click(writeMessage);

});

function writeMessage() {
  jwt = localStorage.getItem('jwt')
  console.log('writeMessage', jwt)


}
