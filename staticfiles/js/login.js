// Page transition effect
document.querySelectorAll('.transition-link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        document.body.classList.add('fade-out');
        setTimeout(() => {
            window.location.href = this.href;
        }, 300); // match with transition duration
    });
});

// Toggle password visibility
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

// Form submission
document.getElementById('login-form').addEventListener('submit', function (e) {
    const spinner = document.getElementById('spinner');
    spinner.classList.remove('hidden');

    // In production, remove the setTimeout and e.preventDefault()
    setTimeout(() => {
        spinner.classList.add('hidden');
    }, 2000);

    e.preventDefault(); // Remove this line in production
});