(function ($) {
  $(document).ready(function(){
      $('#id_name, #id_quantity').on('change',function(){
          var initialname = $('#id_name').val();
          var initialquantity = $('#id_quantity').val();
          if (initialname.trim() !== '' && initialquantity.trim() !== '') {
              $.ajax({
                  type: 'POST',
                  url: '/production/ajax/',
                  data: {
                      'name': initialname,
                      'quantity': initialquantity
                  },
                  dataType: 'json',
                  success: function(response){
                      updateFormset(response);
                      
                      // $('#id_production_components-0-quantity').val(response.quantity);

                  }
              });
          }

      });

      function updateFormset(data) {
     
        var formsetTable = $('fieldset table');
        formsetTable.empty();
  
        // Add table header
        var tableHeader = $('<thead>').appendTo(formsetTable);
        var headerRow = $('<tr>').appendTo(tableHeader);
        $('<th>').addClass('column-code required').text('Code').appendTo(headerRow);
        $('<th>').addClass('column-name required').text('Name').appendTo(headerRow);
        $('<th>').addClass('column-uom required').text('Uom').appendTo(headerRow);
        $('<th>').addClass('column-quantity required').text('Quantity').appendTo(headerRow);
        $('<th>').addClass('column-lineNo required').text('lineNo').appendTo(headerRow);

        $('<th>').text('Delete?').appendTo(headerRow);
  
        // Add table body
        var tableBody = $('<tbody>').appendTo(formsetTable);
  
        data.forEach(function (component, index) {
          var row = $('<tr>');

          var codeCell = $('<td>');
          var codeInput = $('<input type="text" maxlength="20" class="vTextField">');
          codeInput.attr('name', 'production_components-' + index + '-code');
          codeInput.val(component.code);
          codeCell.append(codeInput);

          var nameCell = $('<td>');
          var nameInput = $('<input type="text" maxlength="100" class="vTextField">');
          nameInput.attr('name', 'production_components-' + index + '-name');
          nameInput.val(component.name);
          nameCell.append(nameInput);

          var uomCell = $('<td>');
          var uomInput = $('<input type="text" maxlength="20" class="vTextField">');
          uomInput.attr('name', 'production_components-' + index + '-uom');
          uomInput.val(component.uom);
          uomCell.append(uomInput);

          var quantityCell = $('<td>');
          var quantityInput = $('<input type="number" min="0" step="0.0001" required>');
          quantityInput.attr('name', 'production_components-' + index + '-quantity');
          quantityInput.val(component.quantity);
          quantityCell.append(quantityInput);

          var lineNoCell = $('<td>');
          var lineNoInput = $('<input type="number" min="0" step="1" required>');
          lineNoInput.attr('name', 'production_components-' + index + '-lineNo');
          lineNoInput.val(0);
          lineNoCell.append(lineNoInput);

          var deleteCell = $('<td >');
          var deleteButton = $('<button>').text('Delete');
          deleteButton.addClass('delete-button');
          deleteButton.on('click', function() {
            // Handle delete button click
            row.remove();
            updateTotalForms(); // Update the total forms count
          });
          deleteCell.append(deleteButton);
  
          row.append(codeCell, nameCell, uomCell, quantityCell, lineNoCell, deleteCell);
          formsetTable.append(row);
        });
  
        updateTotalForms(); // Update the total forms count
      
      }


      function updateTotalForms() {
        var formsetTable = $('table');
        var totalForms = formsetTable.find('tbody tr').length;
        $('.last-related #id_production_components-TOTAL_FORMS').val(totalForms);
      }
        
        
  });
})(jQuery);


  // আইটেম কোড লিখলে আইটেমের নাম ITEM মডেল থেকে অটো আসবে 
  (function($) {
    $(document).ready(function() {
  
       
            $("#id_code").on('change', function() {
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
                          
                  const nameInput = $('#id_name');  
                  const uomInput = $('#id_uom');  
  
                  
                  // Update the value of the name input field
                  nameInput.val(response.name);    
                  uomInput.val(response.unit_name);                                  
                    console.log(response);
                }
            });
            
        
  
  
            });
     
        
  
    });
  })(jQuery);



