const firebaseConfig = {
  apiKey: "AIzaSyD5pqDw2o4AyjiARrFEP8nBwG4g2kmRStQ",
  authDomain: "nhan-3660d.firebaseapp.com",
  databaseURL: "https://nhan-3660d-default-rtdb.firebaseio.com",
  projectId: "nhan-3660d",
  storageBucket: "nhan-3660d.appspot.com",
  messagingSenderId: "1054276103106",
  appId: "1:1054276103106:web:428ec651a347fa0b39045b",
  measurementId: "G-27TGW7MZDB"
};
firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();

//-----------------TOAST MESSAGE----------------------
const toastContainer = document.getElementById('toast');

function toast({ title = "", message = "", type = "success", duration = 3000 }) {
  const main = document.getElementById("toast");
  if (main) {
      const toast = document.createElement("div");

      const autoRemoveId = setTimeout(function () {
          main.removeChild(toast);
      }, duration + 1000);

      toast.onclick = function (e) {
          if (e.target.closest(".toast__close")) {
              main.removeChild(toast);
              clearTimeout(autoRemoveId);
          }
      };

      const icons = {
          success: "fas fa-check-circle",
          info: "fas fa-info-circle",
          warning: "fas fa-exclamation-circle",
          error: "fas fa-exclamation-circle"
      };
      const icon = icons[type];
      const delay = (duration / 1000).toFixed(2);

      toast.classList.add("toast", `toast--${type}`);
      toast.style.animation = `slideInLeft ease .3s, fadeOut linear 1s ${delay}s forwards`;

      toast.innerHTML = `
          <div class="toast__icon">
              <i class="${icon}"></i>
          </div>
          <div class="toast__body">
              <h3 class="toast__title">${title}</h3>
              <p class="toast__msg">${message}</p>
          </div>
          <div class="toast__close">
              <i class="fas fa-times"></i>
          </div>
      `;
      main.appendChild(toast);
  }
}

function showSuccessToast() {
  toast({
      title: "Success",
      message: "Account created successfully! Verification email sent.",
      type: "success",
      duration: 3000
  });
}

function showErrorToast(message) {
  toast({
      title: "Error",
      message: message,
      type: "error",
      duration: 3000
  });
}

//-----------------HANDLE SIGN UP----------------------
const signupForm = document.getElementById('signup-form');
signupForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('confirm-password');
  const emailErrorMessage = document.getElementById('email-error-message');
  const passwordErrorMessage = document.getElementById('password-error-message');

  const email = emailInput.value;
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;

  let isValid = true;

  emailErrorMessage.textContent = '';
  passwordErrorMessage.textContent = '';

  if (!email) {
      emailErrorMessage.textContent = "Please enter your email.";
      isValid = false;
  }

  if (password.length < 6) {
      passwordErrorMessage.textContent = "Password must be at least 6 characters.";
      isValid = false;
  }

  if (password !== confirmPassword) {
      passwordErrorMessage.textContent = "Passwords do not match.";
      isValid = false;
  }

  if (!isValid) {
      return;
  }

  //--------Register users using Firebase Authentication-------
  firebase.auth().createUserWithEmailAndPassword(email, password)
      .then((userCredential) => {
          const user = userCredential.user;

          // Send verification email
          user.sendEmailVerification()
              .then(() => {
                  showSuccessToast();
                  localStorage.setItem('registeredEmail', email);
                  localStorage.setItem('registeredPassword', password);
                  setTimeout(() => {
                      window.location.href = './index.html';
                  }, 3000);
              })
              .catch((error) => {
                  showErrorToast("Failed to send verification email. Please try again.");
                  console.error('Error sending verification email:', error);
              });
      })
      .catch(error => {
          const errorCode = error.code;
          const errorMessage = error.message;

          if (errorCode === 'auth/email-already-in-use') {
              showErrorToast("Email is already in use.");
          } else {
              showErrorToast(errorMessage);
              console.error('Registration error:', errorCode, errorMessage);
          }
      });
});

//-----------------EYE PASSWORD----------------------
const togglePassword1 = document.getElementById('toggleIcon1');
const togglePassword2 = document.getElementById('toggleIcon2');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm-password');

togglePassword1.addEventListener('click', function () {
  const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
  passwordInput.setAttribute('type', type);
  this.classList.toggle('fa-eye');
  this.classList.toggle('fa-eye-slash');
});

togglePassword2.addEventListener('click', function () {
  const type = confirmPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
  confirmPasswordInput.setAttribute('type', type);
  this.classList.toggle('fa-eye');
  this.classList.toggle('fa-eye-slash');
});
