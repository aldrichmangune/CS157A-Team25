$(document).ready(function(){
  $('#submit-listing').click(function(event){
      event.preventDefault();
      if($('#id_ISBN').val().length != 13){
        console.log("ISBN length need to be 13, it is only " + $('#id_ISBN').length);
        return false
      }
      if($('#id_Title').val() == '' || $('#id_Author').val() == '' ||$('#id_Publisher').val() == '' || $('#id_Condition').val() == '' || $('#id_Description').val() == '' || $('#id_Image').get(0).files.length == 0){
        console.log("Fail, must fill out all input fields")
        return false;
      }
      formdata = new FormData();
      formdata.append('ISBN', $('#id_ISBN').val());
      formdata.append('Title', $('#id_Title').val());
      formdata.append('Author', $('#id_Author').val());
      formdata.append('Publisher', $('#id_Publisher').val());
      formdata.append('Condition', $('#id_Condition').val());

      var Year = $('#id_Date_year option:selected').text();
      var Day = $('#id_Date_day option:selected').text();
      var MonthName = $('#id_Date_month option:selected').text();
      var months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12};
      var MonthNumber = months[MonthName];
      formdata.append('Date', Year + "-" + MonthNumber + "-" + Day);
      formdata.append('Description', $('#id_Description').val());
      formdata.append('Image', $('#id_Image').get(0).files[0])

      console.log("Success")
      $.ajax(
        {
          type:"POST",
          url:"/add-listing-request/",
          data: formdata,
          contentType: "multipart/form-data",
          processData: false,
          success: function(data){
            if(data['message'] == "Success")
              window.location.href = data['redirect'];
          },
          error: function(response){
            alert(response.status)
          }
        }
      )

  })
})


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
})
