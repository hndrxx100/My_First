$(document).ready(function() {
    // Handle form submission to update table dynamically
    $('#registrationTypeForm').submit(function(event) {
        event.preventDefault();
        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function(response) {
                if (response.error) {
                    // Display error message in modal
                    $('#errorMessage').text(response.error);
                    $('#errorModal').modal('show');
                } else {
                    displayTable(response.registrations);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                // Handle other types of errors here if needed
            }
        });
    });

    // Function to display table based on registrations data
    function displayTable(registrations) {
        var tableBody = $('#registrationTableContainer').find('tbody');
        tableBody.empty();
        $.each(registrations, function(index, registration) {
            var id = index + 1;  // Increment id based on the index of the registration
            var row = '<tr>' +
                '<td>' + id + '</td>' +
                '<td>' + registration.FirstName + '</td>' +
                '<td>' + registration.LastName + '</td>' +
                '<td>' + registration.Email + '</td>' +
                '<td>' + registration.PhoneNumber + '</td>' +
                '<td>' + registration.Registration_type + '</td>' +
                '<td>';
            if (registration.SnackPreferences) {
                $.each(registration.SnackPreferences.split(', '), function(idx, preference) {
                    row += preference + '<br>';
                });
            } else {
                row += 'None';
            }
            row += '</td>' +
                '<td>' + (registration.ExtraServices ? 'Yes' : 'No') + '</td>' +
                '</tr>';
            tableBody.append(row);
        });
    }
});
