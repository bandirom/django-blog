$(function () {
  apiRequest()

})
let requestedNewPage = false

$(window).scroll(function () {
  const pagination = $('#pagination')
  if (pagination.height() - $(this).height() <= $(this).scrollTop() && !requestedNewPage) {
    nextUrl = pagination.attr('data-href-next')
    if (nextUrl && nextUrl != 'None'){
       requestedNewPage = true
       console.log(nextUrl)
       apiRequest()
    }
  }
});


function apiRequest() {
  let pagination = $('#pagination')
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

const tagTemplate = (tag) => {
  return `<a class="tag-list" style="padding: 3px;" data-slug="${tag.slug}"><span class="label label-info">${tag.name}</span></a> `
}

const articleTemplate = (article) => {
  let tags = article.tags.map((tag)=> tagTemplate(tag)).join('')
  return `
    <div class="row">
      <div class="col-md-12 post">
        <div class="row">
          <div class="col-md-12">
            <h4><strong><a href="${article.url}" class="post-title">${article.title}</a></strong></h4>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 post-header-line">
            <span class="glyphicon glyphicon-user"></span>by <a href="${article.author.url}">${article.author.full_name}</a> |
            <span class="glyphicon glyphicon-calendar"></span>${article.updated} |
            <span class="glyphicon glyphicon-comment"></span><a href="#"> ${article.comments_count} Comments</a> |
            <i class="icon-share"></i><a href="#">39 Shares</a> |
            <span class="glyphicon glyphicon-tags"></span> Tags: ${tags}
          </div>
        </div>
        <div class="row post-content">
          <div class="col-md-3">
            <a href="#"><img src="${article.image}" alt="" class="img-responsive" width="200" height="100"></a>
          </div>
          <div class="col-md-9">
            <p>${article.content}</p>
            <p><a class="btn btn-read-more" href="${article.url}">Read more</a></p>
          </div>
        </div>
      </div>
    </div>
  `
}


function newArticlesRender(data, pagination) {
  for (let article of data.results) {
    const template = articleTemplate(article)
    pagination.append(template);
    $('.tag-list').click(tagClickHandler)

  }
  return true;
}
