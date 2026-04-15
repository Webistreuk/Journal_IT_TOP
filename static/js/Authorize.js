const resetPasswordDiv = document.querySelector('.Journal');
const ElementaryDiv = document.querySelector('.Journal_remove_password');
const ForgotButton = document.querySelector('.Forgot_your_password');
const ReturnButton = document.querySelector('.Return_to_the_login_page');
const errorMessageDiv = document.querySelector('.error-message');

function showResetForm() {
    resetPasswordDiv.style.display = 'none';
    ElementaryDiv.style.display = 'block';
    hideError();
}

function showElementaryForm() {
    resetPasswordDiv.style.display = 'block';
    ElementaryDiv.style.display = 'none';
    hideError();
}

function showError(message) {
    if (errorMessageDiv) {
        errorMessageDiv.textContent = message;
        errorMessageDiv.classList.add('visible');
    }
}

function hideError() {
    if (errorMessageDiv) {
        errorMessageDiv.classList.remove('visible');
        errorMessageDiv.textContent = '';
    }
}

if (ForgotButton) ForgotButton.addEventListener('click', showResetForm);
if (ReturnButton) ReturnButton.addEventListener('click', showElementaryForm);