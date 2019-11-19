/**
When the user adds a profile picture, display a preview of it
*/

function check_settings(){

  $('#email-feedback').remove()
  $('#first-name-feedback').remove()
  $('#last-name-feedback').remove()
  $('#password-feedback').remove()
  $('#password-confirm-feedback').remove()
  $('#id_email').removeClass("is-invalid")
  $('#id_first_name').removeClass("is-invalid")
  $('#id_last_name').removeClass("is-invalid")
  $('#id_password').removeClass("is-invalid")
  $('#id_password_confirm').removeClass("is-invalid")

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
  if($('#id_password').val().length == 0){
    $('#id_password').after("<div id='password-feedback' class='invalid-feedback small-text'>Fill out this field</div>");
    $('#id_password').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_password_confirm').val().length == 0){
    $('#id_password_confirm').after("<div id='password-confirm-feedback' class='invalid-feedback small-text'>Fill out this field</div>");
    $('#id_password_confirm').addClass("is-invalid");
    valid_form = false;
  }

  if($('#id_password').val() != $('#id_password_confirm').val() && $('#id_password_confirm').val().length != 0){
    $('#id_password_confirm').after("<div id='password-confirm-feedback' class='invalid-feedback small-text'>Password doesn't match</div>");
    $('#id_password_confirm').addClass("is-invalid");
    valid_form = false;
  }

  if(valid_form == true){
    $('#userchangeform').submit()
  }else{
    return false;
  }
};

$(document).ready(function(){

  $('#id_Profile_Picture').change(function(){
    var File_Reader = new FileReader();
    File_Reader.onload = function(event){
      $('#avatar-pic').attr('src', event.target.result);
    }

    File_Reader.readAsDataURL(this.files[0]);
  })
})
