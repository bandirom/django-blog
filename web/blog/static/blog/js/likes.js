$(function () {
  $('[data-action="like"]').click(like);
  $('[data-action="dislike"]').click(dislike);
});

function like(e) {

  e.preventDefault()
  let like = $(this);
  let type = like.data('type');
  let pk = like.data('id');
  let action = like.data('action');
  let dislike = like.next();
  console.log(type, pk, action, dislike)
  // $.ajax({
  // url:
  // })
}

function dislike() {
  console.log('dislike')
  let dislike = $(this);
  let type = dislike.data('type');
  let pk = dislike.data('id');
  let action = dislike.data('action');
  let like = dislike.prev();
  console.log(type, pk, action, dislike)

}
