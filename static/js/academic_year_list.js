document.addEventListener('DOMContentLoaded', function() {
    const setCurrentButtons = document.querySelectorAll('.btn-set-current');
    const editButtons = document.querySelectorAll('.btn-edit');
    const deleteButtons = document.querySelectorAll('.btn-delete');

    setCurrentButtons.forEach(button => {
        button.addEventListener('click', function() {
            const yearId = this.getAttribute('data-id');
            if (confirm(`Сделать этот учебный год текущим? Предыдущий текущий год перестанет быть текущим.`)) {
                alert(`Учебный год ${yearId} установлен как текущий`);
            }
        });
    });

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const yearId = this.getAttribute('data-id');
            alert(`Редактирование учебного года ID: ${yearId}`);
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const yearId = this.getAttribute('data-id');
            if (!button.disabled) {
                if (confirm(`Вы уверены, что хотите удалить учебный год?`)) {
                    alert(`Учебный год ${yearId} удален`);
                }
            }
        });
    });
});