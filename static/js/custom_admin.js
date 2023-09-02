




  document.addEventListener("DOMContentLoaded", function () {


    // Select the <div> element by its ID "header"
    var headerDiv = document.getElementById('header');
    
    // Check if the element exists before proceeding
    if (headerDiv) {
        // Add your custom class to the <div> element
        headerDiv.classList.add('bg-dark', 'waves-effect', 'waves-light');
    }

    // Select the <h2> element in the admin panel
    var adminHeader = document.querySelector('fieldset.module h2');
    // Select the parent container <div class="submit-row">

    
    // Check if the element exists before adding a class
    if (adminHeader) {
        // Add your custom class to the <h2> element
        adminHeader.classList.add('bg-dark');

    }
    // Find the <p> element
    var pElement = document.querySelector('td.original p');

    // Check if the <p> element exists
    if (pElement) {
        // Remove the <p> element from its parent
        pElement.parentNode.removeChild(pElement);
    }
    var submitRow = document.querySelector('.submit-row');
        // Check if the container exists before proceeding
        if (submitRow) {
            // Get all the input elements with type="submit" inside the container
            var submitButtons = submitRow.querySelectorAll('input[type="submit"]');
            
            // Loop through each input element and add your custom class
       // Loop through each input element and add your custom classes
       submitButtons.forEach(function (button) {
        button.classList.add(
            'btn',
            'btn-sm',
            'btn-elegant',
            'btn-rounded',
            'waves-effect',
            'waves-light'
        );
    });
        }

        var deletelink = document.querySelector('a.deletelink');
        if (deletelink) {
            // Add your custom class to the table
            deletelink.classList.add(
                'btn',
                'btn-danger',
                'btn-rounded',
                'btn-sm','waves-effect','waves-light'



            
            );
             // Add height and padding to the element
             deletelink.style.height = '40px'; // Change '40px' to your desired height
             deletelink.style.padding = '10px'; // Change '10px' to your desired padding

        }
 

            // Select the table you want to add a class to
            var table = document.querySelector('fieldset.module table'); // Replace with your actual CSS selector
            
            // Check if the table exists before proceeding
            if (table) {
                // Add your custom class to the table
                table.classList.add(
                    'table',
                    'table-responsive'
                
                );
            }
     
                // Select the <td> element with the class "original"
    var originalTd = document.querySelector('td.original');

    // Check if the element exists before proceeding
    if (originalTd) {
        // Select the <p> element inside the <td>
        var pElement = originalTd.querySelector('p');

        // Check if the <p> element exists inside the <td>
        if (pElement) {
            // Remove the <p> element from the <td>
            originalTd.removeChild(pElement);
        }
    }
               
    var fieldsets = document.querySelectorAll('fieldset');
    for (var i = 0; i < fieldsets.length; i++) {
        fieldsets[i].style.width = 'fit-content';
    }

    
});
function myFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
      x.className += " w3-show";
    } else {
      x.className = x.className.replace(" w3-show", "");
    }
  }
  
