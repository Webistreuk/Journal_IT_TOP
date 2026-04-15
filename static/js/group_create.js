document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createGroupForm');
    const nameInput = document.getElementById('id_name');
    const courseSelect = document.getElementById('id_course');
    const directionSelect = document.getElementById('id_direction');
    const yearSelect = document.getElementById('id_academic_year');

    form.addEventListener('submit', function(e) {
        let hasError = false;
        let errorMessage = '';

        if (!nameInput.value.trim()) {
            hasError = true;
            errorMessage = 'Введите название группы';
            nameInput.style.borderColor = '#dc3545';
        }

        if (!courseSelect.value) {
            hasError = true;
            errorMessage = 'Выберите курс';
            courseSelect.style.borderColor = '#dc3545';
        }

        if (!directionSelect.value) {
            hasError = true;
            errorMessage = 'Выберите направление';
            directionSelect.style.borderColor = '#dc3545';
        }

        if (!yearSelect.value) {
            hasError = true;
            errorMessage = 'Выберите учебный год';
            yearSelect.style.borderColor = '#dc3545';
        }

        if (hasError) {
            e.preventDefault();
            alert(errorMessage);
        }
    });

    const inputs = [nameInput, courseSelect, directionSelect, yearSelect];
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.style.borderColor = '#ddd';
        });
        input.addEventListener('change', function() {
            this.style.borderColor = '#ddd';
        });
    });
});