document.addEventListener('DOMContentLoaded', function() {
    const rewardCards = document.querySelectorAll('.reward-card');
    
    rewardCards.forEach(card => {
        card.addEventListener('click', function() {
            const rewardName = this.querySelector('.reward-name').textContent;
            console.log(`Просмотр награды: ${rewardName}`);
        });
    });
});