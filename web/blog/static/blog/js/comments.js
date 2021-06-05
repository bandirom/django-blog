
function getArticleComments(article_id, url){
  console.log(article_id, url)
   $.ajax({
     url: url,
     type: 'get',
     success: function (data) {
       console.log('success', data)
     },
     error: function (data) {
       console.log('error', data)
     }
   })
}

