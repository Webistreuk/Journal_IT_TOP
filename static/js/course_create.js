document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('courseForm');
    const numberSelect = document.getElementById('id_number');
    const previewNumber = document.getElementById('previewNumber');

    function updatePreview() {
        const selectedValue = numberSelect.options[numberSelect.selectedIndex]?.text || 'Курс';
        previewNumber.textContent = selectedValue;
    }

    numberSelect.addEventListener('change', updatePreview);

    form.addEventListener('submit', function(e) {
        if (!numberSelect.value) {
            e.preventDefault();
            alert('Выберите номер курса');
            numberSelect.focus();
            return;
        }
    });
});