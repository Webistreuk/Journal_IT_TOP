document.addEventListener('DOMContentLoaded', function() {
    const pairCards = document.querySelectorAll('.pair-card');
    
    pairCards.forEach(card => {
        card.addEventListener('click', function() {
            const subject = this.querySelector('.pair-subject').textContent;
            const professor = this.querySelector('.pair-professor').textContent;
            const classroom = this.querySelector('.pair-classroom').textContent;
            
            console.log(`Предмет: ${subject}, Преподаватель: ${professor}, Аудитория: ${classroom}`);
        });
    });
});