var currentTab = 0;

$(document).ready(function(){
// Current tab is set to be the first tab (0)
  showTab(currentTab); // Display the current tab
});


  function showTab(n) {
    // This function will display the specified tab of the form...
    var tabs = $('.tab')
    tabs.eq(n).css('display', 'block')
    //... and fix the Previous/Next buttons:
    if (n == 0) {
      $('#Previous-Button').css('display', 'none')
    } else {
      $('#Previous-Button').css('display', 'inline')
    }

    if(n == 1){
      if($('#use-as-billing-address').is(':checked')){
        $('input[id^=credit-cards-]').each(function(){
          $(this).prop('checked', false)
        })
        $('#selected-credit-card-billing-address').css('display', 'none')
        $('#new-credit-card-form').css('display', 'block')
        $('#billing-address-form').css('display', 'block')
        use_shipping_as_billing();
      }
    }

    if (n == (tabs.length - 1)) {
      $('#form-div').css('display','none')
      $('#order-summary').css('display', 'none')
      //$('Previous-Button').css('display','none')
      $('#Continue-Button').css('display', 'none')
      $('#shipping-summary').after("<p id='ship-summary-1'>" + $('#city').val() + ", " + $('#state-select').val() + " " + $('#zip-code').val() +"</p>")
      $('#shipping-summary').after("<p id='ship-summary-2'>" + $('#address-1').val() + " " + $('#address-2').val() + "</p>")
      $('#shipping-summary').after("<p id='ship-summary-3'>" + $('#first-name').val() + " " + $('#last-name').val() + "</p>")

      if($('#shipping-choice-1').is(':checked')){
        $('#ship-method').after("<p id='ship-summary-4'>STANDARD</p>")
      }else if($('#shipping-choice-2').is(':checked')){
        $('#ship-method').after("<p id='ship-summary-4'>EXPRESS</p>")
      }

      if($('input[id^=credit-cards-]:checkbox:checked').length == 0){

        $('#billing-summary').after("<p id='billing-summary-1'>" + $('#billing-city').val() + ", " + $('#billing-state-select').val() + " " + $('#billing-zip-code').val() +"</p>")
        $('#billing-summary').after("<p id='billing-summary-2'>" + $('#billing-address-1').val() + " " + $('#billing-address-2').val() + "</p>")
        $('#billing-summary').after("<p id='billing-summary-3'>" + $('#billing-first-name').val() + " " + $('#billing-last-name').val() + "</p>")
        $('#payment-summary').after("<p id='payment-summary-1'>Price: $" + $('#order-price').val() + "</p>")
        $('#payment-summary').after("<p id='payment-summary-2'>Exp. " + $('#month-select').val() + "/" + $('#year-select').val() + "</p>")
        $('#payment-summary').after("<p id='payment-summary-3'>**** **** **** " + $('#credit-card-number').val().slice(-4) + "</p>")
        $('#payment-summary').after("<p id='payment-summary-4'>" + $('#credit-card-name').val() + "</p>")

        $('#order_total').html('$' + $('#order-price').val())
      }else{
        var checked_box = $('input[id^=credit-cards-]:checkbox:checked')
        var label = $('label[for="' + checked_box.attr('id') + '"]')
        $('#billing-summary').after("<p id='billing-summary-1'>" + $('#selected-credit-card-billing-address').val() + "</p>")
        $('#payment-summary').append("<p id='payment-summary-1'></p>")
        $('#payment-summary-1').append(label.html())
      }

    } else {
      $('#form-div').css('display', 'block')
      $('#order-summary').css('display', 'block')
      $('#Continue-Button').css('display', 'block')
      $('#Continue-Button').html("Next")
      $('p[id^=ship-summary-]').each(function(){
        $(this).remove()
      })
      $('p[id^=billing-summary-]').each(function(){
        $(this).remove()
      })
      $('p[id^=payment-summary-]').each(function(){
        $(this).remove()
      })
    }
    window.scrollTo(0,0)
  }

function switchTab(n) {
  // This function will figure out which tab to display
  if(!validateForm(currentTab + n)){
    return false;
  }
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:

  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm(n) {

  $("div[id$=feedback]").each(function(){
    $(this).remove()
  });
  $('.is-invalid').each(function(){
    $(this).removeClass('is-invalid')
  });

  var valid = true;
  if(n == 1){
    if($('#first-name').val().length == 0){
      $('#first-name').after("<div id='first-name-feedback' class='invalid-feedback small-text'>Must enter a first name</div>");
      $('#first-name').addClass("is-invalid");
      valid = false;
    }
    if($('#last-name').val().length == 0){
      $('#last-name').after("<div id='last-name-feedback' class='invalid-feedback small-text'>Must enter a last name</div>");
      $('#last-name').addClass("is-invalid");
      valid = false;
    }
    if($('#address-1').val().length == 0){
      $('#address-1').after("<div id='address-1-feedback' class='invalid-feedback small-text'>Must enter an address</div>");
      $('#address-1').addClass("is-invalid");
      valid = false;
    }
    if($('#state-select').val() == 'STATE'){
      $('#state-select').after("<div id='state-select-feedback' class='invalid-feedback small-text'>Must select a state</div>");
      $('#state-select').addClass("is-invalid");
      valid = false;
    }
    if($('#city').val().length == 0){
      $('#city').after("<div id='city-feedback' class='invalid-feedback small-text'>Must enter a city</div>");
      $('#city').addClass("is-invalid");
      valid = false;
    }
    if($('#zip-code').val().length != 5){
      $('#zip-code').after("<div id='zip-code-feedback' class='invalid-feedback small-text'>Must enter a zip code. (Length of 5)</div>");
      $('#zip-code').addClass("is-invalid");
      valid = false;
    }
    if(!$('#shipping-choice-1').is(':checked') && !$('#shipping-choice-2').is(':checked')){
      $('#shipping-select').after("<div id='shipping-select-feedback' class='invalid-feedback small-text'>Must select a shipping option.</div>");
      $('#shipping-select').addClass("is-invalid");
    }

  }else if(n == 2){
    if($('input[id^=credit-cards-]:checkbox:checked').length > 0){
      return true;
    }

    if($('#billing-first-name').val().length == 0){
      $('#billing-first-name').after("<div id='billing-first-name-feedback' class='invalid-feedback small-text'>Must enter a first name</div>");
      $('#billing-first-name').addClass("is-invalid");
      valid = false;
    }
    if($('#billing-last-name').val().length == 0){
      $('#billing-last-name').after("<div id='billing-last-name-feedback' class='invalid-feedback small-text'>Must enter a last name</div>");
      $('#billing-last-name').addClass("is-invalid");
      valid = false;
    }
    if($('#billing-address-1').val().length == 0){
      $('#billing-address-1').after("<div id='billing-address-1-feedback' class='invalid-feedback small-text'>Must enter an address</div>");
      $('#billing-address-1').addClass("is-invalid");
      valid = false;
    }
    if($('#billing-state-select').val() == 'STATE'){
      $('#billing-state-select').after("<div id='billing-state-select-feedback' class='invalid-feedback small-text'>Must select a state</div>");
      $('#billing-state-select').addClass("is-invalid");
      valid = false;
    }
    if($('#billing-city').val().length == 0){
      $('#billing-city').after("<div id='billing-city-feedback' class='invalid-feedback small-text'>Must enter a city</div>");
      $('#billing-city').addClass("is-invalid");
      valid = false;
    }
    if($('#billing-zip-code').val().length != 5){
      $('#billing-zip-code').after("<div id='billing-zip-code-feedback' class='invalid-feedback small-text'>Must enter a valid zip code. (Length of 5)</div>");
      $('#billing-zip-code').addClass("is-invalid");
      valid = false;
    }
    if($('#month-select').val() == 'MONTH'){
      $('#month-select').after("<div id='month-select-feedback' class='invalid-feedback small-text'>Must select a month</div>");
      $('#month-select').addClass("is-invalid");
      valid = false;
    }
    if($('#year-select').val() == 'YEAR'){
      $('#year-select').after("<div id='year-select-feedback' class='invalid-feedback small-text'>Must select a year</div>");
      $('#year-select').addClass("is-invalid");
      valid = false;
    }
    if($('#credit-card-name').val().length == 0){
      $('#credit-card-name').after("<div id='credit-card-name-feedback' class='invalid-feedback small-text'>Must enter a name</div>");
      $('#credit-card-name').addClass("is-invalid");
      valid = false;
    }
    if($('#credit-card-number').val().length != 16){
      $('#credit-card-number').after("<div id='credit-card-number-feedback' class='invalid-feedback small-text'>Must enter a valid credit card number. (Length of 16)</div>");
      $('#credit-card-number').addClass("is-invalid");
      valid = false;
    }
    if($('#credit-card-cvv').val().length != 3){
      $('#credit-card-cvv').after("<div id='credit-card-cvv-feedback' class='invalid-feedback small-text'>Must enter a valid security code. (Length of 3)</div>");
      $('#credit-card-cvv').addClass("is-invalid");
      valid = false;
    }
    if($('#credit-card-name').val().length != 0 && $('#credit-card-number').val().length == 16 && $('#credit-card-cvv').val().length == 3 && $('#month-select').val() != 'MONTH' && $('#year-select').val() != 'YEAR'){
      $.when(check_paymentinfo()).done(function(response){
        if(response['message'] == "Invalid"){
          switchTab(-1)
          $('#credit-card-number').after("<div id='credit-card-number-feedback' class='invalid-feedback small-text'>This is an invalid credit card number according to our database.</div>");
          $('#credit-card-number').addClass("is-invalid");
          valid = false;
        }
      });

    }
  }
  return valid;
}

function use_shipping_as_billing(){
  $('#billing-first-name').val($('#first-name').val())
  $('#billing-last-name').val($('#last-name').val())
  $('#billing-address-1').val($('#address-1').val())
  $('#billing-address-2').val($('#address-2').val())
  $('#billing-state-select').val($('#state-select').val())
  $('#billing-city').val($('#city').val())
  $('#billing-zip-code').val($('#zip-code').val())
}

function check_paymentinfo(){
  var billing_address = $('#billing-address-1').val() + " " + $('#billing-address-2').val() + " " + $('#billing-city').val() + ", " + $('#billing-state-select').val() + " " + $('#billing-zip-code').val()
  var credit_card_number = $('#credit-card-number').val()
  var credit_card_name = $('#credit-card-name').val()
  var credit_card_cvv = $('#credit-card-cvv').val()
  var credit_card_expiration = $('#month-select').val() + "/" + $('#year-select').val()
  return $.ajax({
    type:'GET',
    url: '/check-payment-info',
    data: {'credit_card_number': credit_card_number, 'credit_card_name': credit_card_name, 'credit_card_cvv': credit_card_cvv,
    'credit_card_expiration': credit_card_expiration, 'billing_address': billing_address},
    success:function(data){
      console.log("YO")
    },
    error: function(response){alert(response.status)},
  });
}

function checkout_Ajax(textbooks){
    var shipping_address = $('#ship-summary-2').html() + " " + $('#ship-summary-1').html();
    var order_total_price = $('#order-price').val();
    if($('#shipping-choice-1').is(':checked')){
      var ship_method = "STANDARD"
    }else if($('#shipping-choice-2').is(':checked')){
      var ship_method = "EXPRESS"
    }
  if($('input[id^=credit-cards-]:checkbox:checked').length == 0){
    var billing_address = $('#billing-summary-2').html() + " " + $('#billing-summary-1').html();
    var credit_card_number = $('#credit-card-number').val()
    var credit_card_name = $('#credit-card-name').val()
    var credit_card_cvv = $('#credit-card-cvv').val()
    var credit_card_expiration = $('#month-select').val() + "/" + $('#year-select').val()
    $.ajax({
      type: 'POST',
      url: '/checkout-request/',
      data: {'shipping_address': shipping_address, 'billing_address': billing_address, 'order_total_price': order_total_price,
            'credit_card_number': credit_card_number, 'credit_card_name': credit_card_name, 'credit_card_cvv': credit_card_cvv,
            'credit_card_expiration': credit_card_expiration, 'textbooks': JSON.stringify(textbooks), 'Shipping_Method': ship_method},
      success: function(data)
        {
          window.location.href = data['redirect']
        },
      error: function(response){ alert(response.status);},
    });
  }else{
    billing_address = $('#billing-summary-1').val()
    var checked_box = $('input[id^=credit-cards-]:checkbox:checked')
    var hidden_inputs = $('label[for="' + checked_box.attr('id') + '"] :input')
    var credit_card_name = hidden_inputs.eq(0).val()
    var credit_card_number = hidden_inputs.eq(1).val()
    var credit_card_cvv = hidden_inputs.eq(2).val()
    var credit_card_expiration = hidden_inputs.eq(3).val()

    $.ajax({
      type: 'POST',
      url: '/checkout-request/',
      data: {'shipping_address': shipping_address, 'billing_address': billing_address, 'order_total_price': order_total_price,
             'credit_card_number': credit_card_number, 'credit_card_name': credit_card_name, 'credit_card_cvv': credit_card_cvv,
             'credit_card_expiration': credit_card_expiration, 'textbooks': JSON.stringify(textbooks), 'Shipping_Method': ship_method},
      success: function(data){
        window.location.href = data['redirect']
      },
      error: function(response){ alert(response.status);},
    })

  }
}
