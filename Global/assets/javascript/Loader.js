document.addEventListener("DOMContentLoaded", function() {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const resetpasswordform = document.getElementById('reset-password-form');
  const loader = document.getElementById('loader');

  function handleFormSubmit(event, url) {
    event.preventDefault();
    loader.style.display = 'flex';

      const formData = new FormData(event.target);
      const formObject = {};
      formData.forEach((value, key) => formObject[key] = value);
  
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formObject)
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
            window.location.href = data.redirectUrl;
        } else {
            loader.style.display = 'none';
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setTimeout(function() {
          loader.style.display = 'none';
        }, 1500);
      });
  }
  if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
      handleFormSubmit(event, '/login');
    });
  }

  if (signupForm) {
    signupForm.addEventListener('submit', function(event) {
      handleFormSubmit(event, '/signup');
    });
  }

  if (resetpasswordform) {
    resetpasswordform.addEventListener('submit', function(event) {
      handleFormSubmit(event, '/signup');
    });
  }
});
