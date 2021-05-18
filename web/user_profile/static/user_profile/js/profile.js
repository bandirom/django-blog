$(function () {
  $("#fileUpload").on('change', uploadPhoto);
});

function uploadPhoto(e) {
  if (this.files && this.files[0]) {
    let reader = new FileReader();

    // reader.onload = function (e) {
    //   $('.avatar').attr('src', e.target.result);
    // }
    //     reader.readAsDataURL(this.files[0]);
    let data = new FormData();
    data.append('avatar', $(this).files[0]);
    console.log('url')
    console.log(data)

    $.ajax({
      type: 'POST',
      url: $(this).data('href'),
      data: data,
      // cache: false,
      success: function (data){
        console.log('success', data)
      },
      error: function (data){
        console.log('error', data)
      }
    })

  }

}
