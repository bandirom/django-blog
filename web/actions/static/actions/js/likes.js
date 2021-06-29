$(function () {
  $('#likeArticle').click(articleLikeRequest);
  $('#dislikeArticle').click(articleLikeRequest);
  $('.commentLike').click(commentLike);
});

function articleLikeRequest(e) {
  let like = $(this);
  let data = {
    'object_id': like.data('id'),
    'model': like.data('type'),
    'vote': like.data('vote'),
  }
  $.ajax({
    url: like.data('href'),
    type: 'post',
    data: data,
    success: function (data) {
      $('#articleLikeCount').text(' ' + data.like_count)
      $('#articleDislikeCount').text(' ' + data.dislike_count)
      switch (data.status) {
        case 'liked':
          liked_style();
          break
        case 'disliked':
          dislike_status()
          break
        default:
          default_status()
          break
      }
    },
    error: function (data) {
      console.log(data, "Error")
    }
  })
}

function liked_style() {
  $('#articleLikeIcon').removeClass('far', 'fa-thumbs-up')
  $('#articleLikeIcon').addClass('fas', 'fa-thumbs-up')

  $('#articleDislikeIcon').addClass('far', 'fa-thumbs-down')
  $('#articleDislikeIcon').removeClass('fas', 'fa-thumbs-down')
}

function dislike_status() {
  $('#articleLikeIcon').removeClass('fas', 'fa-thumbs-up')
  $('#articleLikeIcon').addClass('far', 'fa-thumbs-up')

  $('#articleDislikeIcon').addClass('fas', 'fa-thumbs-down')
  $('#articleDislikeIcon').removeClass('far', 'fa-thumbs-down')

}

function default_status() {
  $('#articleLikeIcon').removeClass('fas', 'fa-thumbs-up')
  $('#articleLikeIcon').addClass('far', 'fa-thumbs-up')

  $('#articleDislikeIcon').removeClass('fas', 'fa-thumbs-down')
  $('#articleDislikeIcon').addClass('far', 'fa-thumbs-down')
}


function commentLike(e) {
  e.preventDefault()
  console.log('like')
  let like = $(this);
  let data = {
    'object_id': like.data('id'),
    'model': like.data('type'),
    'vote': like.data('vote'),
  }
  console.log(data)
  $.ajax({
    url: like.data('href'),
    type: 'post',
    data: data,
    success: function (data) {
      console.log(data, "success")

    },
    error: function (data) {
      console.log(data, "Error")
    }
  })
}
