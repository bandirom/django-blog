$(function () {
  getTags();
})

function getTags() {
  $.ajax({
      type: "GET",
      url: "/api/v1/blog/tags/",
      success: getTagsHandler,
  })
}

function getTagsHandler(data) {
  const tagList = $('#tagList')
  const tags = data.map((tag) => tagCloudTemplate(tag)).join("");
  tagList.append(tags)
  $('.tag-list').click(tagClickHandler)
}

const tagCloudTemplate = (tag) => {
  return `<li><a class="tag-list" data-slug="${tag.slug}"><span class="badge badge-info">${tag.name}</span></a></li>`
}


function tagClickHandler() {
  const tag = $(this)

  // const queryParams = new URLSearchParams(window.location.search);

  const newURL = new URL(window.location.href);
  newURL.searchParams.set('tags', tag.attr('data-slug'));
  window.history.pushState({}, '', newURL);
}
