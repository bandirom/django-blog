$(function () {
  getDetailData()
  //$('#formReview').submit(leftComment);
});

const detailPageDiv = $("#detailPage")

function getDetailData() {
  const slug = window.location.pathname.split('/')[2]
  const url = `/api/v1/blog/articles/${slug}/`
  $.ajax({
      type: "GET",
      url: url,
      success: handleDetailPage,
  })
}


const handleDetailPage = (data) => {
  const render = renderDetailPage(data);
  detailPageDiv.append(render)

}

const renderDetailPage = (data) => {
  console.log('success', data)

  return `
  <div class="col-lg-8">
    <h1><a href="${data.url}">${data.title}</a></h1>
    <p class="lead">
      <i class="fa fa-user"></i> by
      <a href="${data.author.url}">${data.author.full_name}</a>
    </p><hr>
    <p><i class="fa fa-calendar"></i> Posted on ${data.created}</p>

  </div>
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
