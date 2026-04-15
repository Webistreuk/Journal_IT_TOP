document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.btn-edit');
    const deleteButtons = document.querySelectorAll('.btn-delete');

    editButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const announcementId = this.getAttribute('data-id');
            alert(`Редактирование объявления ID: ${announcementId}`);
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const announcementId = this.getAttribute('data-id');
            if (confirm(`Вы уверены, что хотите удалить объявление?`)) {
                alert(`Объявление ${announcementId} удалено`);
            }
        });
    });

    const announcementCards = document.querySelectorAll('.announcement-card');
    announcementCards.forEach(card => {
        card.addEventListener('click', function() {
            const title = this.querySelector('.announcement-title').textContent;
            console.log(`Открыто объявление: ${title}`);
        });
    });
});