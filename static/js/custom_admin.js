document.addEventListener("DOMContentLoaded", function() {

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
        submitButtons.forEach(function(button) {
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
            'btn-sm', 'waves-effect', 'waves-light'




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


    // Get all <td> elements with the class "original"
    var tdElements = document.querySelectorAll(".original");

    // Loop through each <td> element
    tdElements.forEach(function(tdElement) {
        // Get all <p> elements inside the <td>
        var pElements = tdElement.querySelectorAll("p");

        // Loop through and remove each <p> element
        pElements.forEach(function(pElement) {
            pElement.remove();
        });
    });



});


// Accordion menu
function myFunction(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}

//   ফর্ম সাবমিট করার সময় টেবিলের ইনপুট লাইন নাম্বার অটো সেট হবে 
document.addEventListener('DOMContentLoaded', function() {
    var saveButton = document.querySelector('input[name="_save"]');
    if (saveButton) {
        saveButton.addEventListener('click', function(e) {
            const lineNoInputs = document.querySelectorAll('input[name^="productionreceiptitem_set-"][id^="id_productionreceiptitem_set-"][id$="-lineNo"]');
            lineNoInputs.forEach(function(input, index) {
                input.value = index + 1;
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var saveButton = document.querySelector('input[name="_save"]');
    if (saveButton) {
        saveButton.addEventListener('click', function(e) {
            const lineNoInputs = document.querySelectorAll('input[name^="salesorderitem_set-"][id^="id_salesorderitem_set-"][id$="-lineNo"]');
            lineNoInputs.forEach(function(input, index) {
                input.value = index + 1;
            });
        });
    }
});