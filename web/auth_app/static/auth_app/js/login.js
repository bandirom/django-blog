$(function() {
    $(document).on("click", "a.login" , login);
    $('#loginForm').submit(login);
});
console.log('login')

function login(e) {
  console.log('login form')
  e.preventDefault();
}
