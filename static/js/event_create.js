document.addEventListener('DOMContentLoaded', function() {
    const isForAllCheckbox = document.getElementById('id_is_for_all');
    const groupsContainer = document.getElementById('groupsContainer');
    const form = document.getElementById('eventForm');
    const titleInput = document.getElementById('id_title');
    const eventTypeSelect = document.getElementById('id_event_type');
    const startDateInput = document.getElementById('id_start_date');
    const endDateInput = document.getElementById('id_end_date');
    const descriptionTextarea = document.getElementById('id_description');

    const now = new Date();
    const nowStr = now.toISOString().slice(0, 16);
    startDateInput.min = nowStr;
    endDateInput.min = nowStr;

    isForAllCheckbox.addEventListener('change', function() {
        if (this.checked) {
            groupsContainer.style.display = 'none';
            const groupInputs = document.querySelectorAll('.group-input');
            groupInputs.forEach(input => input.checked = false);
        } else {
            groupsContainer.style.display = 'block';
        }
    });

    startDateInput.addEventListener('change', function() {
        endDateInput.min = this.value;
        if (endDateInput.value && endDateInput.value < this.value) {
            endDateInput.value = '';
        }
    });

    form.addEventListener('submit', function(e) {
        if (!titleInput.value.trim()) {
            e.preventDefault();
            alert('Введите название события');
            titleInput.focus();
            return;
        }
        
        if (!eventTypeSelect.value) {
            e.preventDefault();
            alert('Выберите тип события');
            eventTypeSelect.focus();
            return;
        }
        
        if (!startDateInput.value) {
            e.preventDefault();
            alert('Укажите дату и время начала');
            startDateInput.focus();
            return;
        }
        
        if (!endDateInput.value) {
            e.preventDefault();
            alert('Укажите дату и время окончания');
            endDateInput.focus();
            return;
        }
        
        if (endDateInput.value <= startDateInput.value) {
            e.preventDefault();
            alert('Дата окончания должна быть позже даты начала');
            return;
        }
        
        if (!descriptionTextarea.value.trim()) {
            e.preventDefault();
            alert('Введите описание события');
            descriptionTextarea.focus();
            return;
        }
        
        if (!isForAllCheckbox.checked) {
            const checkedGroups = document.querySelectorAll('.group-input:checked');
            if (checkedGroups.length === 0) {
                e.preventDefault();
                alert('Выберите хотя бы одну группу или отметьте "Для всех"');
                return;
            }
        }
    });
});