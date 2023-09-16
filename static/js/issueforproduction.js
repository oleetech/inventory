






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
                        // const quantityInput = tr.find('.field-quantity input');
                        // const codeInput = tr.find('.field-code input');                        
                        // const nameInput = tr.find('.field-name input');
                        // const uomInput = tr.find('.field-uom input');

                        const salesorderInput = tr.find('.field-salesOrder input');
                        
                        // Update the value of the name input field
                        // codeInput.val(response.code);
                        // nameInput.val(response.name);
                        // uomInput.val(response.uom);

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


(function($) {
  $(document).ready(function() {

                      // ইনপুট এর পাশে ক্লিকেবল আইকন যোগ করা       
                      // Find all input elements with the specified id format and add spans after them
                      $('input[name^="issueforproductionitem_set-"][name$="-lineNo"]').each(function() {
                        // Create a new <span> element
                        var span = $("<span>")
                        .attr("id", "icon")   // Set the id attribute to "icon"
                        .addClass("icon")     // Add the "icon" class
                        .text("🔍"); // Set the text content

                        // Insert the <span> element after the current input element
                          $(this).after(span);
  
                });




                     // Add click event handler for the "icon" elements
                     $('span.icon').on('click', function() {
                      var constTr = $(this).closest('tr');
                      var closestTd = $(this).closest('td');
                      var input = closestTd.find('input[name^="issueforproductionitem_set-"][name$="-lineNo"]');
                      var order = constTr.find('input[name^="issueforproductionitem_set-"][name$="-salesOrder"]');
      
                      // Get the value from the input field
                      var inputValue = input.val();
                      var orderNo = order.val();
                     
      
                      $.ajax({
                        type: 'POST',
                        url: '/production/get_production_order_info/',
                        data: {
                            'docNo': orderNo
               
                          
                        },
                        dataType: 'json',
                        success: function(response) {
                        // Assuming response.data contains your code and names arrays
                        var lineNoArray = response.lineNo;
                        var codeArray = response.code;
                        var nameArray = response.name;
                        var quantityArray = response.quantity;                        

  
                        
                    // Assuming you have an element with id "olee" where you want to insert the table
                    var $olee = $('#olee');
  
  
  
                    // Create a table element
                    var $table = $('<table>');
  
                    // Create table headers
                    var $thead = $('<thead>').appendTo($table);
                    var $headerRow = $('<tr>').appendTo($thead);
                    $('<th>').text('lineNo').appendTo($headerRow);
                    $('<th>').text('Code').appendTo($headerRow);
                    $('<th>').text('Name').appendTo($headerRow);
                    $('<th>').text('Quantity').appendTo($headerRow);

  
                    // Create table body
                    var $tbody = $('<tbody>').appendTo($table);
  
                    // Loop through the arrays and populate the table rows
                    for (var i = 0; i < codeArray.length; i++) {
                      var $row = $('<tr>').appendTo($tbody);
                      $('<td>').text(lineNoArray[i]).appendTo($row);
                      $('<td>').text(codeArray[i]).appendTo($row);
                      $('<td>').text(nameArray[i]).appendTo($row);
                      $('<td>').text(quantityArray[i]).appendTo($row);                      

  
                    }
  
                    // Append the table to the "olee" element
                    $olee.html('').append($table);
            
            
                // Get the table element by its ID
                var table = document.getElementById("olee");
                
                table.getElementsByTagName("table")[0].classList.add("table","table-responsive",'table-bordered','datatable');
                // Add a border to the table
                table.getElementsByTagName("table")[0].style.border = "1px solid black";   
                  
                                    
                            console.log(response);
                        }
                    });
                    
                    
                        });              

  });
})(jQuery);



         // production order item   থেকে লাইন নম্বর অনুসারে ডেটা নিয়ে এসে ইনপুট এ সেট করি 
         (function($) {
          $(document).ready(function() {


              $('input[name^="issueforproductionitem_set-"][name$="-orderlineNo"]').each(function() {


                $(this).on('change', function() {
                  const orderlineNoinput = $(this);
                  const inputElement = $(this);
                  const orderlineNo = $(this).val();

                  const tr = inputElement.closest('tr');              
                  const orderno = tr.find('.field-salesOrder input').val();  
        
                    $.ajax({
                      type: 'POST',
                      url: '/production/orderline_by_data/',
                      data: {

                          'orderno':orderno,
                          'orderlineNo': orderlineNo,
             
                        
                      },
                      dataType: 'json',
                      success: function(response) {
                    
                        const codeInput = tr.find('.field-code input').val(response.code);                        
                        const nameInput = tr.find('.field-name input').val(response.name);  
                        const uomInput = tr.find('.field-uom input').val(response.uom);  

           
                          console.log(response);
                      }
                  });
                  
            
                        // /
                      
        
                  });
              });
              

              

        
          });
        })(jQuery);