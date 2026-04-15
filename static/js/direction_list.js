document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const directionCards = document.querySelectorAll('.direction-card');
    const editButtons = document.querySelectorAll('.btn-edit');
    const deleteButtons = document.querySelectorAll('.btn-delete');

    function filterDirections() {
        const searchTerm = searchInput.value.toLowerCase();

        directionCards.forEach(card => {
            const name = card.getAttribute('data-name') || '';
            const code = card.getAttribute('data-code') || '';
            
            const matchesSearch = name.toLowerCase().includes(searchTerm) || code.toLowerCase().includes(searchTerm);
            
            if (matchesSearch) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterDirections);

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const directionId = this.getAttribute('data-id');
            alert(`Редактирование направления ID: ${directionId}`);
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const directionId = this.getAttribute('data-id');
            if (confirm(`Вы уверены, что хотите удалить направление ID: ${directionId}?`)) {
                alert(`Направление ${directionId} удалено`);
            }
        });
    });
});