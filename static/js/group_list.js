document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.btn-edit');
    const deleteButtons = document.querySelectorAll('.btn-delete');
    const viewButtons = document.querySelectorAll('.btn-view-students');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const groupId = this.getAttribute('data-id');
            alert(`Редактирование группы ID: ${groupId}`);
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const groupId = this.getAttribute('data-id');
            if (confirm(`Вы уверены, что хотите удалить группу ID: ${groupId}?`)) {
                alert(`Группа ${groupId} удалена`);
            }
        });
    });

    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const groupId = this.getAttribute('data-id');
            alert(`Просмотр студентов группы ID: ${groupId}`);
        });
    });
});