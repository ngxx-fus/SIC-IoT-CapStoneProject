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
        message: "Login successful!",
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

//-----------------BUTTON LOGIN----------------------
const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('error-message');

    const email = emailInput.value;
    const password = passwordInput.value;

    errorMessage.textContent = '';

    //-----------------ADD TIME LOGIN TO FIREBASE----------------------
    firebase.auth().signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
        const now = new Date();
        const loginTime = now.toString();
        const userEmail = userCredential.user.email;
        const userEmailPrefix = userEmail.split('@')[0];

        if (userCredential.user.emailVerified) {
            firebase.database().ref(`/TimeLogin/user/${userEmailPrefix}`).set({
                loginTime: loginTime
            }).then(() => {
                showSuccessToast("Login successful!");
                setTimeout(() => {
                    window.location.href = './Home.html';
                }, 3000);
            }).catch((error) => {
                showErrorToast("Failed to log login time. Please try again.");
                console.error('Error logging login time:', error);
            });
        } else {
            showErrorToast("Please verify your email before logging in.");
            firebase.auth().signOut();
        }
    })
    .catch(error => {
        const errorCode = error.code;
        const errorMessage = error.message;
        showErrorToast(errorMessage);
        console.error('Login error:', errorCode, errorMessage);
    });
});

//-----------------AUTO-FILL----------------------
document.addEventListener('DOMContentLoaded', function () {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    const registeredEmail = localStorage.getItem('registeredEmail');
    const registeredPassword = localStorage.getItem('registeredPassword');
    if (registeredEmail && registeredPassword) {
        emailInput.value = registeredEmail;
        passwordInput.value = registeredPassword;
        localStorage.removeItem('registeredEmail');
        localStorage.removeItem('registeredPassword');
    }
});

window.onload = function() {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const savedEmail = sessionStorage.getItem('resetPasswordEmail');
    const savedPassword = sessionStorage.getItem('resetPasswordPassword');
    if (savedEmail && savedPassword) {
        emailInput.value = savedEmail;
        passwordInput.value = savedPassword;
        sessionStorage.removeItem('resetPasswordEmail');
        sessionStorage.removeItem('resetPasswordPassword');
    }
};

//-----------------EYE PASSWORD----------------------
const togglePassword = document.getElementById('toggleIcon');
const passwordInput = document.getElementById('password');

togglePassword.addEventListener('click', function () {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});

function sendPasswordReset() {
    const email = document.getElementById('email').value;
    auth.sendPasswordResetEmail(email).then(() => {
        toast({
            title: "Success",
            message: "Password reset email sent!",
            type: "success",
            duration: 3000
        });
    }).catch((error) => {
        toast({
            title: "Error",
            message: error.message,
            type: "error",
            duration: 3000
        });
    });
}
