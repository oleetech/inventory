
// আইটেম কোড লিখলে আইটেমের নাম ITEM মডেল থেকে অটো আসবে 
(function($) {
    $(document).ready(function() {
  
        $('input[name^="customercomplaintitem_set-"][name$="-code"]').each(function() {
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
                //   const uomInput = tr.find('.field-uom input'); 
  
                  
                  // Update the value of the name input field
                  nameInput.val(response.name);  
                //   uomInput.val(response.unit_name);                                  
                    console.log(response);
                }
            });
            
        
  
  
            });
        });
        
  
    });
  })(jQuery);