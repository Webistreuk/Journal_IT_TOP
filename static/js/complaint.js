document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('complaintForm');
    const claimTextarea = document.getElementById('id_claim');
    const charCountSpan = document.getElementById('charCount');
    const confirmCheckbox = document.getElementById('confirmCheck');

    claimTextarea.addEventListener('input', function() {
        const length = this.value.length;
        charCountSpan.textContent = `${length}/500`;
        
        if (length > 500) {
            charCountSpan.style.color = '#dc3545';
        } else {
            charCountSpan.style.color = '#999';
        }
    });

    form.addEventListener('submit', function(e) {
        if (!claimTextarea.value.trim()) {
            e.preventDefault();
            alert('Введите текст жалобы');
            claimTextarea.focus();
            return;
        }
        
        if (claimTextarea.value.length > 500) {
            e.preventDefault();
            alert('Текст жалобы не должен превышать 500 символов');
            return;
        }
        
        if (!confirmCheckbox.checked) {
            e.preventDefault();
            alert('Подтвердите достоверность указанной информации');
            return;
        }
    });
});