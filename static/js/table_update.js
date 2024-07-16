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
                '<td>' + Participants.Firstname + '</td>' +
                '<td>' + Participants.Lastname + '</td>' +
                '<td>' + Participants.Email + '</td>' +
                '<td>' + Participants.Phonenumber + '</td>' +
                '<td>' + Participants.Registration_type + '</td>' +
                '<td>';
            if (Participants.Snackpreferences) {
                $.each(Participants.Snackpreferences.split(', '), function(idx, preference) {
                    row += preference + '<br>';
                });
            } else {
                row += 'None';
            }
            row += '</td>' +
                '<td>' + (Participants.Extraservices ? 'Yes' : 'No') + '</td>' +
                '</tr>';
            tableBody.append(row);
        });
    }
});
