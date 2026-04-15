document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.btn-edit');
    const deleteButtons = document.querySelectorAll('.btn-delete');
    const assignButtons = document.querySelectorAll('.btn-assign');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const subjectId = this.getAttribute('data-id');
            alert(`Редактирование предмета ID: ${subjectId}`);
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const subjectId = this.getAttribute('data-id');
            if (confirm(`Вы уверены, что хотите удалить предмет ID: ${subjectId}?`)) {
                alert(`Предмет ${subjectId} удален`);
            }
        });
    });

    assignButtons.forEach(button => {
        button.addEventListener('click', function() {
            const subjectId = this.getAttribute('data-id');
            alert(`Назначение преподавателя для предмета ID: ${subjectId}`);
        });
    });
});