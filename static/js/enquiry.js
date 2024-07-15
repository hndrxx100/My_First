// flash.js

// Function to handle form submission and display response in modal
document.addEventListener('DOMContentLoaded', function () {
  var enquiryForm = document.getElementById('enquiryForm');
  if (enquiryForm) {
    enquiryForm.addEventListener('submit', function (event) {
      event.preventDefault(); // Prevent default form submission

      var formData = new FormData(this);

      fetch('/', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          var modalMessage = document.getElementById('modalMessage');
          if (data.status === 'success') {
            modalMessage.textContent = data.message;
            enquiryForm.reset();
            $('#responseModal').modal('show');
          } else {
            modalMessage.textContent = data.message;
            $('#responseModal').modal('show');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          var modalMessage = document.getElementById('modalMessage');
          modalMessage.textContent = 'An error occurred. Please try again.';
          $('#responseModal').modal('show');
        });
    });
  }
});
