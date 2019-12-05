
/**
Sends an AJAX request for login
*/

$(document).ready(function(){
  $('#login-submit').click(function(e){
    e.preventDefault();
    console.log($('#username').val())
    $.ajax(
      {
        type:"POST",
        url: "/login-request/",
        data: {
          username: $('#username').val(),
          password: $('#password').val(),
        },
        success: function(data){
          $("div[id$=feedback]").each(function(){
            $(this).remove()
          });
          $('.is-invalid').each(function(){
            $(this).removeClass('is-invalid')
          });

          if(data['username'] == 'Not found'){
            $('#username').after('<div id="username-feedback" class="invalid-feedback">Username not found</div>')
            $('#username').addClass("is-invalid");
          }
          if(data['password'] == 'Incorrect'){
            $('#password').after('<div id="password-feedback" class="invalid-feedback">Password is incorrect</div>')
            $('#password').addClass("is-invalid");
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
