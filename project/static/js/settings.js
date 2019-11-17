/**
When the user adds a profile picture, display a preview of it
*/

$(document).ready(function(){
  $('#id_Profile_Picture').change(function(){
    var File_Reader = new FileReader();
    File_Reader.onload = function(event){
      $('#avatar-pic').attr('src', event.target.result);
    }

    File_Reader.readAsDataURL(this.files[0]);
  })
})
