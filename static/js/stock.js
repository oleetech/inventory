
  

// আইটেম কোড লিখলে আইটেমের নাম ITEM মডেল থেকে অটো আসবে 


(function($) {
  $(document).ready(function() {
    $('#id_code').on('change', function() {
      const code = $(this).val();
      const inputElement = $(this);

      // Make an AJAX request to the server
      $.ajax({
        type: 'POST',
        url: '/itemMasterData/item/',
        data: {
          'code': code
        },
        dataType: 'json',
        success: function(response) {
          const nameInput = $('#id_name');

          // Update the value of the name input field with the response from the server
          nameInput.val(response.name);
          console.log(response);
        },
        error: function(error) {
          console.error(error);
        }
      });
    });
  });
})(jQuery);





     

  









  
  