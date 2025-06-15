// Fade-out effect for page transition
document.querySelectorAll('.transition-link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        document.body.classList.add('fade-out');
        setTimeout(() => {
            window.location.href = this.href;
        }, 300);
    });
});

// Password visibility toggle
function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.password-toggle');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Form validation
function validateForm() {
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    let isValid = true;

    // Reset error messages
    document.querySelectorAll('.error-message').forEach(el => {
        el.style.display = 'none';
    });

    // Email validation
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        document.getElementById('email-error').style.display = 'block';
        isValid = false;
    }

    // Username validation
    if (username.length < 3) {
        document.getElementById('username-error').style.display = 'block';
        isValid = false;
    }

    // Password validation
    if (password.length < 8) {
        document.getElementById('password-error').style.display = 'block';
        isValid = false;
    }

    if (!isValid) {
        document.getElementById('spinner').classList.add('hidden');
        return false;
    }

    return true;
}

// Real-time validation
document.getElementById('email').addEventListener('input', function () {
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.value)) {
        document.getElementById('email-error').style.display = 'none';
    }
});

document.getElementById('username').addEventListener('input', function () {
    if (this.value.length >= 3) {
        document.getElementById('username-error').style.display = 'none';
    }
});

document.getElementById('password').addEventListener('input', function () {
    if (this.value.length >= 8) {
        document.getElementById('password-error').style.display = 'none';
    }
});

// Form submission handler
document.getElementById('register-form').addEventListener('submit', function(e) {
    if (validateForm()) {
        document.getElementById('spinner').classList.remove('hidden');
        // Form will submit normally if validation passes
    } else {
        e.preventDefault();
    }
});