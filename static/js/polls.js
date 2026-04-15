document.addEventListener('DOMContentLoaded', function() {
    const pollCards = document.querySelectorAll('.poll-card');
    
    pollCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                const link = this.querySelector('.btn-poll');
                if (link) {
                    window.location.href = link.href;
                }
            }
        });
    });
});