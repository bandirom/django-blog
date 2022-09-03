$(function () {
  $('#loginForm').submit(login);
  $('#openForgotPasswdModal').click(openForgotPasswordModal);
});

function login(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      localStorage.setItem('jwt', data.access_token)
      location.reload();
    },
    error: function (data) {
      $("#emailGroup").addClass("has-error");
      $("#passwordGroup").addClass("has-error");
      $(".help-block").remove()
      $("#passwordGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );
    }
  })
}

function passwordReset(e) {
  e.preventDefault();
  let form = $(this);
  $.ajax({
    url: "/api/v1/auth/password/reset/",
    type: "POST",
    data: form.serialize(),
    success: function (data) {
      let container = $('#formContainer')
      container.empty()
      container.append(emailSentDiv())
    },
    error: function (data) {
      $("#emailForgotGroup").addClass("has-error");
      $(".help-block").remove()
      $("#emailForgotGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );
    }
  })
}

const emailSentDiv = () => {
  console.log('email send div')
  return `
    <div>
      Email has been sent to your email
    </div>
  `
}

const openForgotPasswordModal = () => {
  $('#forgotPasswdModal').empty()
  $('#forgotPasswdModal').append(forgotPasswordModalForm())
  $('#pwdModal').modal('show')
  $('#forgotPasswordForm').submit(passwordReset);
}

forgotPasswordModalForm = () => {
  return `
    <div id="pwdModal" class="modal fade" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
          <h1 class="text-center">Reset Password?</h1>
        </div>
        <div class="modal-body">
          <div class="col-md-12">
            <div class="panel panel-default">
              <div class="panel-body">
                <div class="text-center">
                  <div id="formContainer" class="panel-body">
                      <form id="forgotPasswordForm" method="post">
                        <div id="emailForgotGroup" class="form-group">
                          <input class="form-control input-lg" placeholder="E-mail Address" name="email" type="email" required>
                        </div>
                        <input class="btn btn-lg btn-success btn-block" value="Reset password" type="submit">
                      </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <div class="col-md-12">
            <button class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  `
}
