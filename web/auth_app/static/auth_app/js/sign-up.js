console.log('sign-up')
$(function () {
  $('#signUpForm').submit(signUp);
});

function signUp(e) {
  let form = $(this);
  e.preventDefault();
  console.log('here')
}
