
  

// আইটেম কোড লিখলে আইটেমের নাম ITEM মডেল থেকে অটো আসবে 
(function($) {
$(document).ready(function () {
  $("#id_code").on('input', function () {
    console.log($(this).val());
      var search_term = $(this).val();
      $.get('{% url "autocomplete" %}', { 'term': search_term }, function (data) {
        var results = $('#autocomplete-results');
          results.empty();
          $.each(data, function (index, item) {
              var listItem = $('<li>').text(item.name).data('code', item.code);
              results.append(listItem);
          });
      });
  });

  $('#autocomplete-results').on('click', 'li', function() {
      var selectedItem = $(this);
      // $('#id_code').val(selectedItem.text());
      $('#id_code').val(selectedItem.data('code'));
      $('#autocomplete-results').empty();
  });
});
})(jQuery);

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





     

  









  
  