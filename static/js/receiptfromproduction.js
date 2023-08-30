

(function($) {
    $(document).ready(function() {
      // Your code here
  
      // Example: Changing IDs with prefix
      var prefix = '#id_productionreceiptitem_set-';
      var pricePrefix = '#id_productionreceiptitem_set-{0}-price';
      var quantityPrefix = '#id_productionreceiptitem_set-{0}-quantity';
      var priceTotalPrefix = '#id_productionreceiptitem_set-{0}-priceTotal';
  
      // Example: Calculate PriceTotal
      function calculatePriceTotal(index) {
        var price = parseFloat($(pricePrefix.replace('{0}', index)).val());
        var quantity = parseFloat($(quantityPrefix.replace('{0}', index)).val());
        var priceTotal = price * quantity;
        $(priceTotalPrefix.replace('{0}', index)).val(priceTotal.toFixed(4));
      }
  
      // Example: Calculate the sum of all calculatePriceTotal values
      function calculateTotalAmount() {
        var total = 0;
        $('input[name^="productionreceiptitem_set-"][name$="-priceTotal"]').each(function() {
          var priceTotal = parseFloat($(this).val());
          if (!isNaN(priceTotal)) {
            total += priceTotal;
          }
        });
        return total.toFixed(4);
      }
  
      // Example: Set the TotalAmount value
      function setTotalAmount() {
        var totalAmount = calculateTotalAmount();
        $('#id_totalAmount').val(totalAmount);
      }
    // Example: Set the TotalQty value
    function setTotalQty() {
      var totalQty = calculateTotalQty();
      $('#id_totalQty').val(totalQty);
    }

function calculateTotalQty() {
  var total = 0;
  $('input[name^="productionreceiptitem_set-"][name$="-quantity"]').each(function() {
    var quantity = parseFloat($(this).val());
    if (!isNaN(quantity)) {
      total += quantity;
    }
  });
  return total.toFixed(4);
} 
      // Example: Handle changes in Price and Quantity fields
      function handleFieldChanges() {
        $('input[name^="productionreceiptitem_set-"][name$="-price"], input[name^="productionreceiptitem_set-"][name$="-quantity"]').on('change', function() {
          var index = $(this).attr('name').split('-')[1];
          calculatePriceTotal(index);
          setTotalAmount();
          setTotalQty();
        });
      }
  
      // Call the function to handle field changes
      handleFieldChanges();
  
    });
  })(jQuery);





  (function($) {
    $(document).ready(function() {

        $('input[name^="productionreceiptitem_set-"][name$="-productionNo"]').each(function() {
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
                        const nameInput = tr.find('.field-name input');
                        const salesorderInput = tr.find('.field-salesOrder input');
                        
                        // Update the value of the name input field
                        nameInput.val(response.name);
                        quantityInput.val(response.quantity);
                        salesorderInput.val(response.salesOrder);
        
                        console.log(response.name);
                    },
                    error: function(error) {
                        console.error('Error:', error);
                    }
                });
            });
        });
        









    });
})(jQuery);

(function($) {
  $(document).ready(function() {
      $('.add-row-button').on('click', function() {
          const rows = $('.dynamic-productionreceiptitem_set');

          rows.each(function(index) {
              const lineNoField = $(this).find('.field-lineNo input');
              const currentLineNo = parseInt(lineNoField.val(), 10);
              lineNoField.val(index + 1);
          });
      });
  });
})(jQuery);
  







  
  
