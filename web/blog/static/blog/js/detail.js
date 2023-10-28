$(function () {
  const slug = window.location.pathname.split('/')[2]

  getArticleDetail(slug);
  getCommentList(slug)
});

const detailPageDiv = $("#detailPage")

function getArticleDetail(slug) {
  const url = `/api/v1/blog/articles/${slug}/`
  $.ajax({
      type: "GET",
      url: url,
      success: handleDetailPage,
  })
}


const handleDetailPage = (article) => {
  const render = renderDetailPage(article);
  detailPageDiv.append(render)
  $('#likeArticle').click(articleLikeRequest);
  $('#dislikeArticle').click(articleLikeRequest);

}
const tagTemplate = (tag) => {
  return `<a href="#"><span class="badge badge-info">${tag}</span></a>`
}

const likeTemplate = (articleId, likes, dislikes, likeStatus) => {
  const likeStatusClass = likeStatus === 1 ? "fas fa-thumbs-up" : "far fa-thumbs-up"
  const dislikeStatusClass = likeStatus === -1 ? "fas fa-thumbs-down" : "far fa-thumbs-down"
  return `
    <ul>
      <li id="likeArticle" data-id="${articleId}" data-type="article" data-vote=1 title="Likes">
        <i id="articleLikeIcon" class="${likeStatusClass}"></i>
        <span id="articleLikeCount"> ${likes}</span>
      </li>
      <li id="dislikeArticle" data-id="${articleId}" data-type="article" data-vote=-1 title="Dislikes">
        <i id="articleDislikeIcon" class="${dislikeStatusClass}"></i>
        <span id="articleDislikeCount"> ${dislikes}</span>
      </li>
    </ul>
  `
}

const renderDetailPage = (article) => {
  const tags = article.tag_list.map((tag) => tagTemplate(tag)).join('')
  const likes = likeTemplate(article.id, article.likes, article.dislikes, article.like_status)
  return `
    <h1><a href="${article.url}">${article.title}</a></h1>
    <p class="lead">
      <i class="fa fa-user"></i> by <a href="${article.author.url}">${article.author.full_name}</a>
    </p><hr>
    <p><i class="fa fa-calendar"></i> Posted on ${article.created}</p>
    <p><i class="fa fa-tags"></i> Tags: ${tags}</p>
    <div>${likes}</div>
    <hr>
    <img src="${article.image}" class="img-responsive" width="700" height="300">
    <hr>
    <p class="lead">${article.content}</p>
    <br/>
    <hr>
  `

}


function addParentToComment(commentAuthor, parent_id) {
  document.getElementById("commentParent").value = parent_id;
  document.getElementById("textComment").innerText = commentAuthor + ', ';
}

const error_class_name = "has-error"

function leftComment(e) {
  e.preventDefault()
  let form = $(this);
  $.ajax({
    url: form.attr("action"),
    type: form.attr("method"),
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      $(".help-block").remove()
      let groups = ['#emailGroup', '#textAreaGroup']
      for (let group of groups) {
        $(group).removeClass(error_class_name);
      }
      if (data.responseJSON.email) {
        help_block("#emailGroup", data.responseJSON.email)
      }
      if (data.responseJSON.content) {
        help_block("#textAreaGroup", data.responseJSON.content)
      }
    }
  })
}


function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}


function getCommentList(slug) {
  console.log('comments')
}
