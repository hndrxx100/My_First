document.addEventListener('DOMContentLoaded', function () {
    var registrationForm = document.getElementById('registrationForm');
    var closeModalButton = document.getElementById('closeModalButton');

    // Function to handle form submissions
    function handleFormSubmit(form, endpoint) {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent default form submission

            var formData = new FormData(this);

            fetch(endpoint, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    // If response is not ok, treat it as an error
                    return response.json().then(data => Promise.reject(data));
                }
                return response.json();
            })
            .then(data => {
                var modalMessage = document.getElementById('modalMessage');
                modalMessage.textContent = data.message; // Display response message directly

                $('#responseModal').modal('show'); // Show modal with response message
            })
            .catch(error => {
                console.error('Error:', error);
                var modalMessage = document.getElementById('modalMessage');
                modalMessage.textContent = error.message || 'An error occurred. Please try again.';

                $('#responseModal').modal('show');
            });
        });
    }

    // Handle registration form submission
    if (registrationForm) {
        handleFormSubmit(registrationForm, '/registration'); // Adjust endpoint as per your Flask route
    }

    // Clear form when the modal is closed
    $('#responseModal').on('hidden.bs.modal', function () {
        if (registrationForm) {
            registrationForm.reset();
        }
    });
});
