const resetPasswordDiv = document.querySelector('.Journal');
const ElementaryDiv = document.querySelector('.Journal_remove_password');
const ForgotButton = document.querySelector('.Forgot_your_password');
const ReturnButton = document.querySelector('.Return_to_the_login_page');

function showResetForm() {
    resetPasswordDiv.style.display = 'none';
    ElementaryDiv.style.display = 'block';
};

function showElementaryForm() {
    resetPasswordDiv.style.display = 'block';
    ElementaryDiv.style.display = 'none';
};

if (ForgotButton) ForgotButton.addEventListener('click', showResetForm);
if (ReturnButton) ReturnButton.addEventListener('click', showElementaryForm);