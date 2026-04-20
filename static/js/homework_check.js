document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('checkForm');
    const gradeInput = document.getElementById('id_grade');

    function validateAndFixGrade() {
        let value = parseInt(gradeInput.value);
        
        if (isNaN(value) || gradeInput.value === '') {
            gradeInput.value = '';
            return;
        }
        
        if (value < 1) {
            gradeInput.value = 1;
            showToast('Оценка не может быть меньше 1. Установлено значение 1', 'warning');
        } else if (value > 5) {
            gradeInput.value = 5;
            showToast('Оценка не может быть больше 5. Установлено значение 5', 'warning');
        }
    }

    gradeInput.addEventListener('blur', function() {
        validateAndFixGrade();
        if (gradeInput.value === '') {
            gradeInput.style.borderColor = '#dc3545';
        } else {
            gradeInput.style.borderColor = '#28a745';
        }
    });

    gradeInput.addEventListener('input', function() {
        if (gradeInput.value !== '') {
            gradeInput.style.borderColor = '#ddd';
        }
    });

    form.addEventListener('submit', function(e) {
        let hasError = false;
        
        validateAndFixGrade();
        
        if (gradeInput.value === '') {
            hasError = true;
            gradeInput.style.borderColor = '#dc3545';
            showToast('Пожалуйста, выставьте оценку!', 'error');
        } else {
            gradeInput.style.borderColor = '#28a745';
        }
        
        if (hasError) {
            e.preventDefault();
        } else {
            showToast('Работа проверена!', 'success');
        }
    });

    function showToast(message, type) {
        const existingToast = document.querySelector('.toast-notification');
        if (existingToast) existingToast.remove();
        
        const toast = document.createElement('div');
        toast.className = `toast-notification ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    if (gradeInput.value) {
        validateAndFixGrade();
    }
});