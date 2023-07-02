
$(function () {
  getArticleComments();
});

let requestedNewPage = false

$(window).scroll(function () {
  let pagination = $('#comments-list')
  console.log(pagination.height() - $(this).height(), $(this).scrollTop())
  if (pagination.height() - $(this).height() <= $(this).scrollTop() && !requestedNewPage) {
    nextUrl = pagination.attr('data-href-next')
    if (nextUrl && nextUrl != 'None'){
       requestedNewPage = true
       console.log(nextUrl)
    }
  }
});

function getArticleComments(){
  pagination = $('#paginationComment')
  url = pagination.attr('data-href-next')
  $.ajax({
   url: url,
   type: 'get',
   success: function (data) {
     if (data.results) {
        addLinks(pagination, data.next)
        if (renderComments(pagination, data)) {
           requestedNewPage = false;
        }
      }
   },
   error: function (data) {
     console.log('error', data)
   }
  })
}

function addLinks(pagination, next) {
  pagination.attr('data-href-next', next)

}


function renderComments(pagination, data){
  comments = data.results
  $.each(comments, function(i){
    var templateString = `
      <li>
				<div class="comment-main-level">
					<div class="comment-avatar"><img src="http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg" alt=""></div>
					<div class="comment-box">
						<div class="comment-head">
							<h6 class="comment-name by-author"><a href="#">${comments[i].author}</a></h6>
							<span>${comments[i].updated}</span>
              <a href="#formReview" onclick="addParentToComment('${comments[i].author}', '${comments[i].id}')"><i class="fa fa-reply"></i></a>
               <i class="fa fa-heart commentLike"
                  data-id="${comments[i].id}" data-vote=1
                  data-href="{% url 'actions:like_dislike' %}"da
                  data-type="comment"></i>
						</div>
						<div class="comment-content">
							${comments[i].content}
						</div>
					</div>
				</div>
				<!-- Comments reply -->
				<ul class="comments-list reply-list">

				</ul>
			</li>

    `
   pagination.append(templateString);
  })
  return true;
}
