document.addEventListener('DOMContentLoaded', function() {
    const studentNameFilter = document.getElementById('studentNameFilter');
    const groupFilter = document.getElementById('groupFilter');
    const resetBtn = document.getElementById('resetFilters');
    const reviewCards = document.querySelectorAll('.review-card');
    
    function filterReviews() {
        const searchName = studentNameFilter ? studentNameFilter.value.toLowerCase().trim() : '';
        const selectedGroup = groupFilter ? groupFilter.value : 'all';
        
        reviewCards.forEach(card => {
            const studentName = card.getAttribute('data-student') || '';
            const studentGroup = card.getAttribute('data-group') || '';
            
            let show = true;
            
            if (searchName && !studentName.toLowerCase().includes(searchName)) {
                show = false;
            }
            
            if (show && selectedGroup !== 'all' && studentGroup !== selectedGroup) {
                show = false;
            }
            
            card.style.display = show ? 'block' : 'none';
        });
    }
    
    function resetFilters() {
        if (studentNameFilter) studentNameFilter.value = '';
        if (groupFilter) groupFilter.value = 'all';
        filterReviews();
    }
    
    if (studentNameFilter) studentNameFilter.addEventListener('input', filterReviews);
    if (groupFilter) groupFilter.addEventListener('change', filterReviews);
    if (resetBtn) resetBtn.addEventListener('click', resetFilters);
    
    filterReviews();
});