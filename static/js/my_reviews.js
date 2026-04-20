document.addEventListener('DOMContentLoaded', function() {
    const filter = document.getElementById('mySubjectFilter');
    const cards = document.querySelectorAll('.my-review-card');
    const container = document.getElementById('myReviewsList');
    
    function filterReviews() {
        const value = filter.value;
        let visibleCount = 0;
        
        cards.forEach(card => {
            const subject = card.getAttribute('data-subject');
            if (value === 'all' || subject === value) {
                card.style.display = 'block';
                card.style.animation = 'none';
                card.offsetHeight;
                card.style.animation = 'cardFadeIn 0.5s ease-out';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        const emptyDiv = document.querySelector('.my-reviews-empty');
        if (visibleCount === 0 && cards.length > 0) {
            if (!emptyDiv) {
                const noResults = document.createElement('div');
                noResults.className = 'my-reviews-empty';
                noResults.innerHTML = '😔 Нет отзывов по выбранному предмету';
                noResults.style.animation = 'emptyFadeIn 0.5s ease-out';
                container.appendChild(noResults);
            }
        } else if (emptyDiv && visibleCount > 0) {
            emptyDiv.remove();
        }
    }
    
    filter.addEventListener('change', function() {
        filterReviews();
    });
    
    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });
    
    filterReviews();
});