document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('checkForm');
    const gradeSelect = document.getElementById('id_grade');
    const isCheckedCheckbox = document.getElementById('id_is_checked');

    form.addEventListener('submit', function(e) {
        let hasError = false;
        
        if (gradeSelect.value === '') {
            hasError = true;
            gradeSelect.style.borderColor = '#dc3545';
            alert('Пожалуйста, выставьте оценку');
        } else {
            gradeSelect.style.borderColor = '#ddd';
        }
        
        if (hasError) {
            e.preventDefault();
        }
    });

    gradeSelect.addEventListener('change', function() {
        this.style.borderColor = '#ddd';
        if (this.value !== '' && !isCheckedCheckbox.checked) {
            isCheckedCheckbox.checked = true;
        }
    });
});