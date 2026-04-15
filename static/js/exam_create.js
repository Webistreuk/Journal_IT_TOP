document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('examForm');
    const studentSelect = document.getElementById('id_student');
    const subjectSelect = document.getElementById('id_subject');
    const professorSelect = document.getElementById('id_professor');
    const gradeSelect = document.getElementById('id_grade');
    const examDateInput = document.getElementById('id_exam_date');
    const semesterSelect = document.getElementById('id_semester');
    const fileInput = document.getElementById('id_exam_file');
    const fileInfo = document.getElementById('fileInfo');
    const fileNameSpan = document.getElementById('fileName');
    const removeFileBtn = document.querySelector('.btn-remove-file');

    const today = new Date().toISOString().split('T')[0];
    examDateInput.max = today;

    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            const maxSize = 10 * 1024 * 1024;
            
            if (file.size > maxSize) {
                alert('Файл слишком большой. Максимальный размер 10MB');
                this.value = '';
                fileInfo.style.display = 'none';
                return;
            }
            
            fileNameSpan.textContent = file.name;
            fileInfo.style.display = 'flex';
        }
    });

    removeFileBtn.addEventListener('click', function() {
        fileInput.value = '';
        fileInfo.style.display = 'none';
    });

    form.addEventListener('submit', function(e) {
        if (!studentSelect.value) {
            e.preventDefault();
            alert('Выберите студента');
            studentSelect.focus();
            return;
        }
        
        if (!subjectSelect.value) {
            e.preventDefault();
            alert('Выберите предмет');
            subjectSelect.focus();
            return;
        }
        
        if (!professorSelect.value) {
            e.preventDefault();
            alert('Выберите преподавателя');
            professorSelect.focus();
            return;
        }
        
        if (!gradeSelect.value) {
            e.preventDefault();
            alert('Выберите оценку');
            gradeSelect.focus();
            return;
        }
        
        if (!examDateInput.value) {
            e.preventDefault();
            alert('Укажите дату экзамена');
            examDateInput.focus();
            return;
        }
        
        if (!semesterSelect.value) {
            e.preventDefault();
            alert('Выберите семестр');
            semesterSelect.focus();
            return;
        }
    });
});