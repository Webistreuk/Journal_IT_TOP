document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const subjectFilter = document.getElementById('subjectFilter');
    const materialsGrid = document.getElementById('materialsGrid');
    const materialCards = document.querySelectorAll('.material-card');

    function filterMaterials() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedSubject = subjectFilter.value;

        materialCards.forEach(card => {
            const title = card.querySelector('.material-title').textContent.toLowerCase();
            const description = card.querySelector('.material-description').textContent.toLowerCase();
            const subject = card.getAttribute('data-subject') || '';
            
            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
            const matchesSubject = !selectedSubject || subject === selectedSubject;
            
            if (matchesSearch && matchesSubject) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterMaterials);
    subjectFilter.addEventListener('change', filterMaterials);
});