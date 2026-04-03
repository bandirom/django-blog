$(function(){
    confirmEmail()
})

function confirmEmail(){
    const urlSearchParams = new URLSearchParams(window.location.search)
    const data = {'key' : urlSearchParams.get("key")}
    $.ajax({
        url: "/api/v1/auth/sign-up/verify/",
        type: "POST",
        data: data,
        success: function(data) {
            console.log("Success", data)
        },
        error: function(data) {
            console.log("Error", data)
        }
    })
}