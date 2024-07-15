document.addEventListener('DOMContentLoaded', function () {
    var loginForm = document.getElementById('loginForm');

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

                // Show modal with response message
                $('#responseModal').modal('show');

                // If login is successful, store the redirect URL
                if (data.status === "success") {
                    $('#responseModal').data('redirect-url', data.redirect_url);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                var modalMessage = document.getElementById('modalMessage');
                modalMessage.textContent = error.message || 'An error occurred. Please try again.';

                $('#responseModal').modal('show');
            });
        });
    }

    // Handle login form submission
    if (loginForm) {
        handleFormSubmit(loginForm, '/login'); // Adjust endpoint as per your Flask route
    }

    // Redirect to dashboard when the modal is closed and login was successful
    $('#responseModal').on('hidden.bs.modal', function () {
        var redirectUrl = $(this).data('redirect-url');
        if (redirectUrl) {
            window.location.href = redirectUrl;
        }
        if (loginForm) {
            loginForm.reset();
        }
    });
});
