
/**
Sends an AJAX request for login
*/

$(document).ready(function(){
  $('#login-submit').click(function(e){
    e.preventDefault();
    $.ajax(
      {
        type:"POST",
        url: "/login-request/",
        data: {
          username: $('#username').val(),
          password: $('#password').val(),
        },
        success: function(data){
          if(data['username'] == 'Not found'){
            $('#username').addClass("is-invalid");
          }
          if(data['password'] == 'Not found'){
            $('#password').addClass("is-invalid");
          }else if(data['password'] == 'Incorrect'){
            $('#password').addClass("is-invalid");
            $('#password-feedback').html("Password is incorrect")
          }
          if(data['message'] == 'Success'){
            location.reload()
          }
        },
        error: function(response){
          alert(response.status)
        },
      }
    )
  })
})
