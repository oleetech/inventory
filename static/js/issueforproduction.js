






  (function($) {
    $(document).ready(function() {

    
        $('input[name^="issueforproductionitem_set-"][name$="-productionNo"]').each(function() {
            $(this).on('change', function() {
                const inputValue = parseInt($(this).val(), 10); // Convert inputValue to an integer
        
                // Store a reference to the input element
                const inputElement = $(this);
        
                // Send the AJAX request using jQuery's $.ajax method
                $.ajax({
                    type: 'POST',
                    url: '/production/receiptproduction/',
                    data: {
                        'productionNo': inputValue
                    },
                    dataType: 'json',
                    success: function(response) {
                        const tr = inputElement.closest('tr');
                        const quantityInput = tr.find('.field-quantity input');
                        const codeInput = tr.find('.field-code input');                        
                        const nameInput = tr.find('.field-name input');
                        const uomInput = tr.find('.field-uom input');

                        const salesorderInput = tr.find('.field-salesOrder input');
                        
                        // Update the value of the name input field
                        codeInput.val(response.code);
                        nameInput.val(response.name);
                        uomInput.val(response.uom);

                        // quantityInput.val(response.quantity);
                        salesorderInput.val(response.salesOrder);
        
                        console.log(response);
                    },
                    error: function(error) {
                        console.error('Error:', error);
                    }
                });
            });
        });
        









    });
})(jQuery);




// আইটেম কোড লিখলে আইটেমের নাম ITEM মডেল থেকে অটো আসবে 
(function($) {
  $(document).ready(function() {

      $('input[name^="issueforproductionitem_set-"][name$="-code"]').each(function() {
          $(this).on('change', function() {
            const code = $(this).val();
            const inputElement = $(this);

            $.ajax({
              type: 'POST',
              url: '/itemMasterData/item/',
              data: {
                  'code': code
     
                
              },
              dataType: 'json',
              success: function(response) {
                const tr = inputElement.closest('tr');              
                const nameInput = tr.find('.field-name input');  

                
                // Update the value of the name input field
                nameInput.val(response.name);                                    
                  console.log(response);
              }
          });
          
      


          });
      });
      

  });
})(jQuery);


