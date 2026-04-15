document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('academicYearForm');
    const nameInput = document.getElementById('id_name');
    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');
    const previewName = document.getElementById('previewName');
    const previewDates = document.getElementById('previewDates');

    function updatePreview() {
        previewName.textContent = nameInput.value || 'Учебный год';
        
        if (startDateInput.value && endDateInput.value) {
            const start = new Date(startDateInput.value).toLocaleDateString('ru-RU');
            const end = new Date(endDateInput.value).toLocaleDateString('ru-RU');
            previewDates.textContent = `${start} - ${end}`;
        } else if (startDateInput.value) {
            const start = new Date(startDateInput.value).toLocaleDateString('ru-RU');
            previewDates.textContent = `${start} - ...`;
        } else if (endDateInput.value) {
            const end = new Date(endDateInput.value).toLocaleDateString('ru-RU');
            previewDates.textContent = `... - ${end}`;
        } else {
            previewDates.textContent = '';
        }
    }

    nameInput.addEventListener('input', updatePreview);
    startDateInput.addEventListener('change', updatePreview);
    endDateInput.addEventListener('change', updatePreview);

    const today = new Date().toISOString().split('T')[0];
    startDateInput.min = today;

    startDateInput.addEventListener('change', function() {
        endDateInput.min = this.value;
        if (endDateInput.value && endDateInput.value < this.value) {
            endDateInput.value = '';
        }
    });

    form.addEventListener('submit', function(e) {
        if (!nameInput.value.trim()) {
            e.preventDefault();
            alert('Введите название учебного года');
            nameInput.focus();
            return;
        }
        
        const namePattern = /^\d{4}-\d{4}$/;
        if (!namePattern.test(nameInput.value.trim())) {
            e.preventDefault();
            alert('Название должно быть в формате ГГГГ-ГГГГ (например, 2024-2025)');
            nameInput.focus();
            return;
        }
        
        if (!startDateInput.value) {
            e.preventDefault();
            alert('Выберите дату начала учебного года');
            startDateInput.focus();
            return;
        }
        
        if (!endDateInput.value) {
            e.preventDefault();
            alert('Выберите дату окончания учебного года');
            endDateInput.focus();
            return;
        }
        
        if (endDateInput.value <= startDateInput.value) {
            e.preventDefault();
            alert('Дата окончания должна быть позже даты начала');
            return;
        }
    });
});