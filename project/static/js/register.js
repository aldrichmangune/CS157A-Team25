
function check_register(){
  $("div[id$=feedback]").each(function(){
    $(this).remove()
  });
  $('.is-invalid').each(function(){
    $(this).removeClass('is-invalid')
  });

  var valid_form = true

  if($('#id_email').val().length == 0){
    $('#id_email').after("<div id='email-feedback' class='invalid-feedback small-text'>Fill out this field</div>");
    $('#id_email').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_first_name').val().length == 0){
    $('#id_first_name').after("<div id='first-name-feedback' class='invalid-feedback small-text'>Fill out this field</div>");
    $('#id_first_name').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_last_name').val().length == 0){
    $('#id_last_name').after("<div id='last-name-feedback' class='invalid-feedback small-text'>Fill out this field</div>");
    $('#id_last_name').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_password1').val().length == 0){
    $('#id_password1').after("<div id='password-feedback' class='invalid-feedback small-text'>Fill out this field</div>");
    $('#id_password1').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_password2').val().length == 0){
    $('#id_password2').after("<div id='password-confirm-feedback' class='invalid-feedback small-text'>Fill out this field</div>");
    $('#id_password2').addClass("is-invalid");
    valid_form = false;
  }

  if($('#id_password1').val() != $('#id_password2').val() && $('#id_password2').val().length != 0){
    $('#id_password2').after("<div id='password-confirm-feedback' class='invalid-feedback small-text'>Password doesn't match</div>");
    $('#id_password2').addClass("is-invalid");
    valid_form = false;
  }


  if(valid_form){
    $('#register-form').submit()
  }else{
    return false;
  }
};
