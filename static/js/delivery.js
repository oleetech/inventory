

(function($) {
    $(document).ready(function() {




      // Example: Changing IDs with prefix
      var prefix = '#id_deliveryitem_set-';
      var pricePrefix = '#id_deliveryitem_set-{0}-price';
      var quantityPrefix = '#id_deliveryitem_set-{0}-quantity';
      var priceTotalPrefix = '#id_deliveryitem_set-{0}-priceTotal';
  
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
        $('input[name^="deliveryitem_set-"][name$="-priceTotal"]').each(function() {
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
  $('input[name^="deliveryitem_set-"][name$="-quantity"]').each(function() {
    var quantity = parseFloat($(this).val());
    if (!isNaN(quantity)) {
      total += quantity;
    }
  });
  return total.toFixed(4);
} 
      // Example: Handle changes in Price and Quantity fields
      function handleFieldChanges() {
        
        $('input[name^="deliveryitem_set-"][name$="-lineNo"]').on('change', function() {
          var index = $(this).attr('name').split('-')[1];
          calculatePriceTotal(index);
          setTotalAmount();
          setTotalQty();
        });

        $('input[name^="deliveryitem_set-"][name$="-price"], input[name^="deliveryitem_set-"][name$="-quantity"],input[name^="deliveryitem_set-"][name$="-lineNo"]').on('change', function() {
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

        $('input[name^="deliveryitem_set-"][name$="-lineNo"]').each(function() {
            $(this).on('change', function() {

              
              const inputValue = parseInt($(this).val(), 10);
              const receiptNo = $(this).closest('tr').find('.field-receiptNo input').val();

              const inputElement = $(this);

              $.ajax({
                type: 'POST',
                url: '/sales/delivery/',
                data: {
                    'receiptNo': receiptNo,
                    'lineNo':inputValue
                  
                },
                dataType: 'json',
                success: function(response) {
                  const tr = inputElement.closest('tr');
                  const codeInput = tr.find('.field-code input');  
                  const nameInput = tr.find('.field-name input');  
                  const quantityInput = tr.find('.field-quantity input'); 
                  const orderInput = tr.find('.field-orderNo input');                 
                  const orderlineNoInput = tr.find('.field-orderlineNo input');                 
                  const uomInput = tr.find('.field-uom input');    
                  const sizeInput = tr.find('.field-size input');                 
                  const colorInput = tr.find('.field-color input');                     
                  const priceInput = tr.find('.field-price input');     
                  const priceTotalInput = tr.find('.field-priceTotal input');                       
                  // Update the value of the name input field
                  codeInput.val(response.code); 
                  nameInput.val(response.name); 
                  quantityInput.val(response.quantity);
                  orderInput.val(response.salesOrder);   
                  orderlineNoInput.val(response.orderlineNo);   
                  uomInput.val(response.uom);   
                  sizeInput.val(response.size);   
                  colorInput.val(response.color);   
                  priceInput.val(response.price);   
                  priceTotalInput.val(response.priceTotal);                                       
                    console.log(response);
                }
            });
            
        


            });
        });
        

    });
})(jQuery);
  

// আইটেম কোড লিখলে আইটেমের নাম ITEM মডেল থেকে অটো আসবে 
(function($) {
  $(document).ready(function() {

      $('input[name^="deliveryitem_set-"][name$="-code"]').each(function() {
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



(function($) {
  $(document).ready(function() {

     
          $("#id_salesOrder").on('change', function() {
            const orderNo = $(this).val();
            const inputElement = $(this);

            $.ajax({
              type: 'POST',
              url: '/sales/deliveryinfo/',
              data: {
                  'orderNo': orderNo
     
                
              },
              dataType: 'json',
              success: function(response) {
                        
                const customerInput = $('#id_customerName');  
                const addressInput = $('#id_address');  
                const salesemployeeInput = $('#id_sales_employee');    

                
                // // Update the value of the name input field
                customerInput.val(response.customerName);   
                addressInput.val(response.address);    
                salesemployeeInput.val(response.sales_employee);                                  
                  console.log(response);
              }
          });
          
      


          });
   
      

  });
})(jQuery);


