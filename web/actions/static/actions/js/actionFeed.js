$(function () {
  feedList();
});

function feedList() {
  $.ajax({
   url: '/api/v1/actions/feed',
   type: 'get',
   success: feedListHandler,
   error: function (data) {
     console.log('error', data)
   }
  })
}


function feedListHandler(data) {
  const feedList = $('#feedList')
  const template = data.results.map((feed) => feedTemplate(feed)).join('<hr>');
  feedList.append(template);
}

function feedTemplate(feed) {
  switch (feed.action) {
    case 'update_avatar':
      return updateAvatarTemplate(feed);
    case 'create_article':
      return updateAvatarTemplate(feed);
  }
}

function updateAvatarTemplate(feed) {
  return `
    <div class="panel panel-default">
    <div class="panel-heading">
      User <a href="/user/${feed.user.id}/">${feed.user.full_name}</a> changed avatar
    </div>
    <div class="panel-image">
      <img
        src="${feed.user.avatar}"
        class="img-circle img-responsive center-image"
      />
    </div>
    ${feedPanel()}
  </div>
  `
}


function feedPanel() {
  return `
    <div class="panel-footer clearfix">
      <a href="#download" class="btn btn-primary btn-sm btn-hover pull-left">Save <span class="fa fa-bookmark"></span></a>
      <a href="#facebook" class="btn btn-success btn-sm btn-hover pull-left" style="margin-left: 5px;">Share <span
        class="glyphicon glyphicon-send"></span></a>
      <a class="btn comsys btn-danger btn-sm btn-hover pull-left" style="margin-left: 5px;">Cmt <span
        class="fa fa-comment"></span></a>
      <a href="#like" class="btn btn-warning btn-sm btn-hover pull-left" style="margin-left: 5px;">Like <span
        class="fa fa-thumbs-up"></span></a>
    </div>
  `
}

$('.toggler').click(function() {
    var tog = $(this);
    var secondDiv = tog.parent().prev();
    var firstDiv = secondDiv.prev();
    firstDiv.children('p').toggleClass('hide');
    secondDiv.toggleClass('hide');
    //tog.parent().find('.first > p').toggleClass('hide');
    //tog.parent().find('.second').toggleClass('hide');
    //$('.first > .main').toggleClass('hide');
    tog.toggleClass('fa fa-chevron-up fa fa-chevron-down');
    return false;
});

$('.comsys').click(function() {
    var togCmt = $(this);
    togCmt.toggleClass('active');
    var panelFooterDiv = togCmt.parent();
    var panelDefaultDiv = panelFooterDiv.parent();
    var panelCmtsDiv = panelDefaultDiv.next();
    panelCmtsDiv.slideToggle('hide');
    return false;
});
