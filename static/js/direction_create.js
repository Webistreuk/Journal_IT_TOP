document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('directionForm');
    const codeInput = document.getElementById('id_code');
    const nameInput = document.getElementById('id_name');
    const previewCode = document.getElementById('previewCode');
    const previewName = document.getElementById('previewName');

    function updatePreview() {
        previewCode.textContent = codeInput.value || 'Код направления';
        previewName.textContent = nameInput.value || 'Название направления';
    }

    codeInput.addEventListener('input', updatePreview);
    nameInput.addEventListener('input', updatePreview);

    form.addEventListener('submit', function(e) {
        if (!codeInput.value.trim()) {
            e.preventDefault();
            alert('Введите код направления');
            codeInput.focus();
            return;
        }
        
        if (!nameInput.value.trim()) {
            e.preventDefault();
            alert('Введите название направления');
            nameInput.focus();
            return;
        }
        
        if (codeInput.value.length > 20) {
            e.preventDefault();
            alert('Код направления не должен превышать 20 символов');
            return;
        }
        
        if (nameInput.value.length > 100) {
            e.preventDefault();
            alert('Название направления не должно превышать 100 символов');
            return;
        }
    });
});