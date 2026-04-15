document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createForm');
    const fileInput = document.getElementById('id_file');
    const dateInput = document.getElementById('id_date_final');
    const groupSelect = document.getElementById('id_group');
    const subjectSelect = document.getElementById('id_subject');
    const commentTextarea = document.getElementById('id_comment');

    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;

    form.addEventListener('submit', function(e) {
        let hasError = false;
        let errorMessage = '';

        if (!groupSelect.value) {
            hasError = true;
            errorMessage = 'Выберите группу';
            groupSelect.style.borderColor = '#dc3545';
        }

        if (!subjectSelect.value) {
            hasError = true;
            errorMessage = 'Выберите предмет';
            subjectSelect.style.borderColor = '#dc3545';
        }

        if (!fileInput.files.length) {
            hasError = true;
            errorMessage = 'Прикрепите файл с заданием';
            fileInput.style.borderColor = '#dc3545';
        } else {
            const file = fileInput.files[0];
            const maxSize = 20 * 1024 * 1024;
            if (file.size > maxSize) {
                hasError = true;
                errorMessage = 'Файл не должен превышать 20MB';
                fileInput.style.borderColor = '#dc3545';
            }
        }

        if (!commentTextarea.value.trim()) {
            hasError = true;
            errorMessage = 'Напишите комментарий к заданию';
            commentTextarea.style.borderColor = '#dc3545';
        }

        if (!dateInput.value) {
            hasError = true;
            errorMessage = 'Укажите срок сдачи';
            dateInput.style.borderColor = '#dc3545';
        } else if (dateInput.value < today) {
            hasError = true;
            errorMessage = 'Срок сдачи не может быть в прошлом';
            dateInput.style.borderColor = '#dc3545';
        }

        if (hasError) {
            e.preventDefault();
            alert(errorMessage);
        }
    });

    groupSelect.addEventListener('change', function() {
        this.style.borderColor = '#ddd';
    });

    subjectSelect.addEventListener('change', function() {
        this.style.borderColor = '#ddd';
    });

    fileInput.addEventListener('change', function() {
        this.style.borderColor = '#ddd';
    });

    commentTextarea.addEventListener('input', function() {
        this.style.borderColor = '#ddd';
    });

    dateInput.addEventListener('change', function() {
        this.style.borderColor = '#ddd';
    });
});