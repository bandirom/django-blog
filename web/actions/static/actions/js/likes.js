$(function () {
  $('#likeArticle').click(like);
  $('#dislikeArticle').click(dislike);
});

function like(e) {
  e.preventDefault()
  let like = $(this);
  let dislike = like.next();
  let data = {
    'object_id': like.data('id'),
    'model': like.data('type'),
    'vote': 1,
  }
  $.ajax({
    url: like.data('href'),
    type: 'post',
    data: data,
    success: function (data) {
      console.log(data, "Success")
    },
    error: function (data) {
      console.log(data, "Error")
    }
  })
}

function dislike() {
  console.log('dislike')
  let dislike = $(this);
  let data = {
    'object_id': dislike.data('id'),
    'model': dislike.data('type'),
    'vote': -1,
  }
  $.ajax({
    url: dislike.data('href'),
    type: 'post',
    data: data,
    success: function (data) {
      console.log(data, "Success")
    },
    error: function (data) {
      console.log(data, "Error")
    }
  })

}
