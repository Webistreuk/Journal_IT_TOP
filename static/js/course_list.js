document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.btn-edit');
    const deleteButtons = document.querySelectorAll('.btn-delete');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const courseId = this.getAttribute('data-id');
            const courseNumber = this.getAttribute('data-number');
            alert(`Редактирование курса №${courseNumber} (ID: ${courseId})`);
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const courseId = this.getAttribute('data-id');
            const courseNumber = this.getAttribute('data-number');
            if (confirm(`Вы уверены, что хотите удалить ${courseNumber} курс?`)) {
                alert(`Курс ${courseNumber} удален`);
            }
        });
    });
});