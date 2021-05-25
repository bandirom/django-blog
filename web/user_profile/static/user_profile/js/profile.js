$(function () {
  $("#fileUpload").on('change', uploadPhoto);
});

function uploadPhoto(e) {
  let data = new FormData();
  let files = $(this)[0].files;
  data.append('avatar', files[0]);

  $.ajax({
    type: 'POST',
    url: $(this).data('href'),
    data: data,
    contentType: false,
    processData: false,
    success: function (data) {
      $("#avatar").attr("src",data.avatar);
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}
