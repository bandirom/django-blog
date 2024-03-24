$(function () {
  $('.category-select').select2();
  $('#createArticleForm').submit(postCreate);
  getCategories();
});

const error_class_name = "has-error"

function getCategories() {
  $.ajax({
    url: '/api/v1/blog/categories/',
    type: 'GET',
    success: getCategoriesHandler,
  })
}

function getCategoriesHandler (data) {
  const selector = $('.category-select')
  data.forEach((category) => selector.append(new Option(category.name, category.id)))
}

function postCreate(event) {
  event.preventDefault()
  let form = $(this)
  const formData = new FormData(form[0]);
  $.ajax({
    url: '/api/v1/blog/articles/new/',
    type: form.attr('method'),
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {
      console.log('success', data)
      $('#successModal').modal('show');
    },
    error: function (data) {
      $(".help-block").remove()
      let groups = ['#categoryGroup', '#titleGroup', '#contentGroup', '#posterGroup']
      for (let group of groups) {
        $(group).removeClass(error_class_name);
      }
      if (data.responseJSON.category) {
        help_block("#categoryGroup", data.responseJSON.category)
      }
      if (data.responseJSON.title) {
        help_block("#titleGroup", data.responseJSON.title)
      }
      if (data.responseJSON.content) {
        help_block("#contentGroup", data.responseJSON.content)
      }
      if (data.responseJSON.image) {
        help_block("#posterGroup", data.responseJSON.image)
      }
    },
  })
}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}
