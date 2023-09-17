









(function($) {
    $(document).ready(function() {
      // Your code here
  
      // Example: Changing IDs with prefix
      var prefix = '#id_purchasequotetionitem_set-';
      var pricePrefix = '#id_purchasequotetionitem_set-{0}-price';
      var quantityPrefix = '#id_purchasequotetionitem_set-{0}-quantity';
      var priceTotalPrefix = '#id_purchasequotetionitem_set-{0}-priceTotal';
  
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
        $('input[name^="purchasequotetionitem_set-"][name$="-priceTotal"]').each(function() {
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
  $('input[name^="purchasequotetionitem_set-"][name$="-quantity"]').each(function() {
    var quantity = parseFloat($(this).val());
    if (!isNaN(quantity)) {
      total += quantity;
    }
  });
  return total.toFixed(4);
  } 
      // Example: Handle changes in Price and Quantity fields
      function handleFieldChanges() {
        $('input[name^="purchasequotetionitem_set-"][name$="-price"], input[name^="purchasequotetionitem_set-"][name$="-quantity"]').on('change', function() {
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
  
  
  
  

  // আইটেম কোড লিখলে আইটেমের নাম ITEM মডেল থেকে অটো আসবে 
  (function($) {
    $(document).ready(function() {
  
        $('input[name^="purchasequotetionitem_set-"][name$="-code"]').each(function() {
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
                  const uomInput = tr.find('.field-uom input');    
                  
                  // Update the value of the name input field
                  nameInput.val(response.name);                         
                  uomInput.val(response.unit_name);                                    

                    console.log(response);
                }
            });
            
        
  
  
            });
        });
        
  
    });
  })(jQuery);
  
  
  
  
  
  
  