document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const gradeFilter = document.getElementById('gradeFilter');
    const examCards = document.querySelectorAll('.exam-card');

    function filterExams() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedGrade = gradeFilter.value;

        examCards.forEach(card => {
            const subject = card.getAttribute('data-subject') || '';
            const grade = card.getAttribute('data-grade') || '';
            
            const matchesSearch = subject.toLowerCase().includes(searchTerm);
            const matchesGrade = !selectedGrade || grade === selectedGrade;
            
            if (matchesSearch && matchesGrade) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterExams);
    gradeFilter.addEventListener('change', filterExams);
});