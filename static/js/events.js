document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.btn-edit');
    const deleteButtons = document.querySelectorAll('.btn-delete');

    editButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const eventId = this.getAttribute('data-id');
            alert(`Редактирование события ID: ${eventId}`);
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const eventId = this.getAttribute('data-id');
            if (confirm(`Вы уверены, что хотите удалить событие?`)) {
                alert(`Событие ${eventId} удалено`);
            }
        });
    });
});