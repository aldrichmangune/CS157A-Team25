
function checkform(){
  /**
    THIS FUNCTION VALIDATES THAT THE USER INPUT FOR ADDING TEXTBOOK LISTING IS CORRECT
  */

  $('#ISBN-feedback').remove()
  $('#Title-feedback').remove()
  $('#Author-feedback').remove()
  $('#Publisher-feedback').remove()
  $('#Condition-feedback').remove()
  $('#Description-feedback').remove()
  $('#hidden-feedback').remove()
  $('#Price-feedback').remove()
  $('#Category-feedback').remove()
  $('#id_ISBN').removeClass("is-invalid")
  $('#id_Title').removeClass("is-invalid")
  $('#id_Author').removeClass("is-invalid")
  $('#id_Publisher').removeClass("is-invalid")
  $('#id_Condition').removeClass("is-invalid")
  $('#id_Description').removeClass("is-invalid")
  $('#id_Price').removeClass("is-invalid")
  $('#id_Category').removeClass("is-invalid")

  var valid_form = true;

  if($('#id_ISBN').val().length != 13){
    $('#id_ISBN').after("<div id='ISBN-feedback' class='invalid-feedback small-text'>ISBN length need to be 13</div>");
    $('#id_ISBN').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Title').val() == ''){
    $('#id_Title').after("<div id='Title-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Title').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Author').val() == ''){
    $('#id_Author').after("<div id='Author-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Author').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Publisher').val() == ''){
    $('#id_Publisher').after("<div id='Publisher-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Publisher').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Cond').val() == ''){
    $('#id_Cond').after("<div id='Condition-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Cond').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Description').val() == ''){
    $('#id_Description').after("<div id='Description-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Description').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Price').val() == ''){
    $('#id_Price').after("<div id='Price-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Price').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Image').get(0).files.length == 0){
    $('#hidden-input').after("<p id='hidden-feedback' style='color: red;'>Must choose an image</p>");
    valid_form = false;
  }

  if ($('#id_Category input:checkbox:checked').length == 0){
    $('#id_Category').after("<div id='Category-feedback' class='invalid-feedback small-text'>Must select a category</div>")
    $('#id_Category').addClass("is-invalid");
    valid_form = false;
  }

  // If the user input is all correct, then submits the form
  if(valid_form){
    $('#add-listing-form').submit();
  }else{
    return false;
  }
}

function checkeditform(){

  /**
    THIS FUNCTION VALIDATES THAT THE USER INPUT FOR EDITING TEXTBOOK LISTING IS ALL CORRECT
  */
  $('#ISBN-feedback').remove()
  $('#Title-feedback').remove()
  $('#Author-feedback').remove()
  $('#Publisher-feedback').remove()
  $('#Condition-feedback').remove()
  $('#Description-feedback').remove()
  $('#hidden-feedback').remove()
  $('#Price-feedback').remove()
  $('#id_ISBN').removeClass("is-invalid")
  $('#id_Title').removeClass("is-invalid")
  $('#id_Author').removeClass("is-invalid")
  $('#id_Publisher').removeClass("is-invalid")
  $('#id_Condition').removeClass("is-invalid")
  $('#id_Description').removeClass("is-invalid")
  $('#id_Price').removeClass("is-invalid")

  var valid_form = true;

  if($('#id_ISBN').val().length != 13){
    $('#id_ISBN').after("<div id='ISBN-feedback' class='invalid-feedback small-text'>ISBN length need to be 13</div>");
    $('#id_ISBN').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Title').val() == ''){
    $('#id_Title').after("<div id='Title-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Title').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Author').val() == ''){
    $('#id_Author').after("<div id='Author-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Author').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Publisher').val() == ''){
    $('#id_Publisher').after("<div id='Publisher-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Publisher').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Cond').val() == ''){
    $('#id_Cond').after("<div id='Condition-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Cond').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Description').val() == ''){
    $('#id_Description').after("<div id='Description-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Description').addClass("is-invalid");
    valid_form = false;
  }
  if($('#id_Price').val() == ''){
    $('#id_Price').after("<div id='Price-feedback' class='invalid-feedback small-text'>Must fill out this field</div>");
    $('#id_Price').addClass("is-invalid");
    valid_form = false;
  }

  if ($('#id_Category input:checkbox:checked').length == 0){
    $('#id_Category').after("<div id='Category-feedback' class='invalid-feedback small-text'>Must select a category</div>")
    $('#id_Category').addClass("is-invalid");
    valid_form = false;
  }

  // If the form is valid, then submits it
  if(valid_form){
    $('#edit-listing-form').submit();

  }else{
    return false;
  }
}

/**
  When an image file is added to the input element, display a preview of it
*/
$(document).ready(function(){
  $('#id_Image').change(function(){
    $('#book-img').remove()
    $('#image-card').prepend("<img style='max-height:300px;max-width:300px;' id='book-img' src='' alt='Not found'>");
    var File_Reader = new FileReader();
    File_Reader.onload = function(event){
      $('#book-img').attr('src', event.target.result);
    }

    File_Reader.readAsDataURL(this.files[0]);
  })
});
