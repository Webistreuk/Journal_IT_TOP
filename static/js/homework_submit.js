document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('submitForm');
    const fileInput = document.getElementById('id_file');
    const timeWorkInput = document.getElementById('id_time_work');
    const usefulnessSelect = document.getElementById('id_the_usefulness_of_knowledge');

    form.addEventListener('submit', function(e) {
        let hasError = false;
        let errorMessage = '';

        if (!fileInput.files.length) {
            hasError = true;
            errorMessage = 'Пожалуйста, выберите файл с работой';
            fileInput.style.borderColor = '#dc3545';
        } else {
            const file = fileInput.files[0];
            const maxSize = 10 * 1024 * 1024;
            if (file.size > maxSize) {
                hasError = true;
                errorMessage = 'Файл не должен превышать 10MB';
                fileInput.style.borderColor = '#dc3545';
            }
        }

        if (timeWorkInput.value && parseInt(timeWorkInput.value) < 0) {
            hasError = true;
            errorMessage = 'Время выполнения не может быть отрицательным';
            timeWorkInput.style.borderColor = '#dc3545';
        }

        if (hasError) {
            e.preventDefault();
            alert(errorMessage);
        }
    });

    fileInput.addEventListener('change', function() {
        this.style.borderColor = '#ddd';
    });

    timeWorkInput.addEventListener('input', function() {
        this.style.borderColor = '#ddd';
    });
});