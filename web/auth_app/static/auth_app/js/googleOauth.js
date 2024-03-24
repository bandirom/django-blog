$(function () {
  googleCallbackHandler();
  $('#loginGoogle').click(googleLoginInit);
});


function googleLoginInit(e) {
  $.ajax({
    url: '/api/v1/auth/oauth2/redirect-url/?provider=google',
    method: 'get',
    success: function (redirect_url) {
      window.location.href = redirect_url;
    }
  })
}


function googleCallbackHandler() {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code')
  const scope = urlParams.get('scope')
  const state = urlParams.get('state')
  if (state && scope && state) {
    const data = {
      code: code,
      scope: scope,
      state: state,
    }
    $.ajax({
      url: '/api/v1/auth/google/sign-in/',
      data: data,
      method: 'post',
      success: successGoogleCallback,
      error: errorGoogleCallback,
    })
  }
}

function successGoogleCallback(data) {
  console.log('successGoogleCallback', data)
  window.location.href = '/profile/'
}

function errorGoogleCallback(data) {
  console.log('errorGoogleCallback', data)
}
