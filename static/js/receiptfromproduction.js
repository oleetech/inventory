

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
              const inputValue = $(this).val();

              
              // Construct the URL for your AJAX endpoint
              const url = '{% url "home" %}';

              
              // Construct the data to be sent in the request
              const data = {
                value: inputValue

              };
              
              // Send the AJAX request using jQuery's $.ajax method
              $.ajax({
                url: url,
                method: 'POST', // or 'GET', 'PUT', etc.
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function(response) {
                  // Handle the response data if needed
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
  







  
  
