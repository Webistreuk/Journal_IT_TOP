// static/js/student_review_create.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reviewForm');
    const studentSelect = document.getElementById('id_student');
    const professorSelect = document.getElementById('id_professor');
    const subjectSelect = document.getElementById('id_subject');
    const commentTextarea = document.getElementById('id_comment');
    const charCountSpan = document.getElementById('charCount');

    commentTextarea.addEventListener('input', function() {
        const length = this.value.length;
        charCountSpan.textContent = `${length}/800`;
        
        if (length > 800) {
            charCountSpan.style.color = '#dc3545';
        } else {
            charCountSpan.style.color = '#999';
        }
    });

    form.addEventListener('submit', function(e) {
        if (!studentSelect.value) {
            e.preventDefault();
            alert('Выберите студента');
            studentSelect.focus();
            return;
        }
        
        if (!professorSelect.value) {
            e.preventDefault();
            alert('Выберите преподавателя');
            professorSelect.focus();
            return;
        }
        
        if (!subjectSelect.value) {
            e.preventDefault();
            alert('Выберите предмет');
            subjectSelect.focus();
            return;
        }
        
        if (!commentTextarea.value.trim()) {
            e.preventDefault();
            alert('Введите текст отзыва');
            commentTextarea.focus();
            return;
        }
        
        if (commentTextarea.value.length > 800) {
            e.preventDefault();
            alert('Текст отзыва не должен превышать 800 символов');
            return;
        }
    });
});