document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('appealForm');
    const typeSelect = document.getElementById('id_Select_the_signal_type');
    const questionTextarea = document.getElementById('id_question');
    const charCountSpan = document.getElementById('charCount');

    questionTextarea.addEventListener('input', function() {
        const length = this.value.length;
        charCountSpan.textContent = `${length}/500`;
        
        if (length > 500) {
            charCountSpan.style.color = '#dc3545';
        } else {
            charCountSpan.style.color = '#999';
        }
    });

    form.addEventListener('submit', function(e) {
        if (!typeSelect.value) {
            e.preventDefault();
            alert('Выберите тип обращения');
            typeSelect.focus();
            return;
        }
        
        if (!questionTextarea.value.trim()) {
            e.preventDefault();
            alert('Введите текст обращения');
            questionTextarea.focus();
            return;
        }
        
        if (questionTextarea.value.length > 500) {
            e.preventDefault();
            alert('Текст обращения не должен превышать 500 символов');
            return;
        }
    });
});