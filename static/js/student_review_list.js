document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const groupFilter = document.getElementById('groupFilter');
    const subjectFilter = document.getElementById('subjectFilter');
    const reviewCards = document.querySelectorAll('.review-card');
    const deleteButtons = document.querySelectorAll('.btn-delete');

    function filterReviews() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedGroup = groupFilter.value;
        const selectedSubject = subjectFilter.value;

        reviewCards.forEach(card => {
            const studentName = card.getAttribute('data-student') || '';
            const group = card.getAttribute('data-group') || '';
            const subject = card.getAttribute('data-subject') || '';
            
            const matchesSearch = studentName.toLowerCase().includes(searchTerm);
            const matchesGroup = !selectedGroup || group === selectedGroup;
            const matchesSubject = !selectedSubject || subject === selectedSubject;
            
            if (matchesSearch && matchesGroup && matchesSubject) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterReviews);
    groupFilter.addEventListener('change', filterReviews);
    subjectFilter.addEventListener('change', filterReviews);

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const reviewId = this.getAttribute('data-id');
            if (confirm('Вы уверены, что хотите удалить этот отзыв?')) {
                alert(`Отзыв ${reviewId} удален`);
            }
        });
    });
});