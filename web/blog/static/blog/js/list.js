
let requestedNewPage = false

$(window).scroll(function () {
  let pagination = $('#pagination')
  if (pagination.height() - $(this).height() <= $(this).scrollTop() && !requestedNewPage) {
    nextUrl = pagination.attr('data-href-next')
    if (nextUrl && nextUrl != 'None'){
       requestedNewPage = true
       console.log(nextUrl)
       apiRequest(pagination)
    }
  }
});


function apiRequest(pagination){
  $.ajax({
      type: "GET",
      url: pagination.attr('data-href-next'),
      success: function (data) {
        if (data.results) {
          appendUrls(pagination,data.next, data.previous)
          if (newArticlesRender(data, pagination)) {
             requestedNewPage = false;
          }
        }
      }
  })
}

function appendUrls(pagination, next, previous) {
  pagination.attr('data-href-next', next)
  pagination.attr('data-href-previous', previous)

}

function newArticlesRender(data, pagination) {
  articles = data.results
  $.each(articles, function(i){
    let tags = ''
    for (let j of articles[i].tag_list) {
      tags += `<a href="#"><span class="label label-info">${j}</span></a> `;
    }
   var templateString = `
      <div class="row">
          <div class="col-md-12 post">
            <div class="row">
              <div class="col-md-12">
                <h4>
                  <strong>
                    <a href="${articles[i].url}" class="post-title">${articles[i].title}</a>
                  </strong>
                </h4>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12 post-header-line">
                <span class="glyphicon glyphicon-user"></span>by <a href="${articles[i].author.url}">${articles[i].author.full_name}</a> |
                <span class="glyphicon glyphicon-calendar"></span>${articles[i].updated} |
                <span class="glyphicon glyphicon-comment"></span><a href="#"> ${articles[i].comments_count} Comments</a> |
                <i class="icon-share"></i><a href="#">39 Shares</a> |
                <span class="glyphicon glyphicon-tags"></span> Tags: ${tags}
              </div>
            </div>
            <div class="row post-content">
              <div class="col-md-3">
                <a href="#"><img src="${articles[i].image}" alt="" class="img-responsive" width="200" height="100"></a>
              </div>
              <div class="col-md-9">
                <p>
                  ${articles[i].content}
                </p>
                <p>
                  <a class="btn btn-read-more" href="${articles[i].url}">Read more</a>
                </p>
              </div>
            </div>
          </div>
        </div>
   `
   pagination.append(templateString);
  })
  return true;
}
