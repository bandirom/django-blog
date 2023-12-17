$(function () {
  userList()
});


function userList() {
  $.ajax({
    type: 'GET',
    url: '/api/v1/user/',
    success: userListHandler,
  })
}

function userListTemplate(user) {
  const followButtonText = getButtonText(user.follow)
  return `
    <li class="span5 clearfix">
      <div class="thumbnail clearfix">
        <img src="${user.avatar}" alt="Avatar" class="pull-left span2 clearfix avatar img-circle img-thumbnail" width="120px"
             style='margin-right:10px'>
        <div class="caption" class="pull-left">
          <a href="#" data-id="${user.id}"
             class="btn btn-primary icon  pull-right followMe">${followButtonText}</a>
          <h4>
            <a href="/user/${user.id}">${ user.full_name}</a>
          </h4>
           <small><b>RG: </b>99384877</small>
        </div>
      </div>
    </li>
  `
}

function userListHandler(data) {
  const userList = $('#userList');
  const result = data.results.map((user) => userListTemplate(user)).join('');
  userList.empty();
  userList.append(result);
  $(".followMe").click(followMe);
}
