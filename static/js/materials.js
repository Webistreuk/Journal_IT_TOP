document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const subjectFilter = document.getElementById('subjectFilter');
    const resetBtn = document.getElementById('resetFilters');
    const materialsGrid = document.getElementById('materialsGrid');
    
    if (!materialsGrid) return;
    
    const materialCards = Array.from(document.querySelectorAll('.material-card'));
    const isProfessor = subjectFilter && subjectFilter.options.length > 0 && subjectFilter.options[0].value !== 'all';
    
    function filterMaterials() {
        const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const selectedSubject = subjectFilter ? subjectFilter.value : (isProfessor ? '' : 'all');
        
        let visibleCount = 0;
        
        materialCards.forEach(card => {
            const title = card.getAttribute('data-title') || '';
            const subject = card.getAttribute('data-subject') || '';
            
            let show = true;
            
            if (searchTerm && !title.includes(searchTerm)) {
                show = false;
            }
            
            if (show && selectedSubject !== 'all' && subject !== selectedSubject) {
                show = false;
            }
            
            if (show) {
                card.style.display = 'flex';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        const emptyMessage = materialsGrid.querySelector('.empty-materials');
        if (visibleCount === 0 && materialCards.length > 0) {
            if (!emptyMessage) {
                const noDataDiv = document.createElement('div');
                noDataDiv.className = 'empty-materials';
                noDataDiv.textContent = '❌ Нет материалов, соответствующих фильтрам';
                materialsGrid.appendChild(noDataDiv);
            }
        } else {
            if (emptyMessage && materialCards.length > 0) {
                emptyMessage.remove();
            }
        }
    }
    
    function resetFilters() {
        if (searchInput) searchInput.value = '';
        if (subjectFilter && subjectFilter.options.length > 0 && subjectFilter.options[0].value === 'all') {
            subjectFilter.value = 'all';
        }
        filterMaterials();
    }
    
    if (searchInput) searchInput.addEventListener('input', filterMaterials);
    if (subjectFilter && subjectFilter.options.length > 0 && subjectFilter.options[0].value === 'all') {
        subjectFilter.addEventListener('change', filterMaterials);
    }
    if (resetBtn) resetBtn.addEventListener('click', resetFilters);
    
    filterMaterials();
});