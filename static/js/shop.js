document.addEventListener('DOMContentLoaded', function() {
    const buyForms = document.querySelectorAll('.buy-form');
    
    buyForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('.btn-buy');
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('.product-name').textContent;
            
            if (confirm(`Вы уверены, что хотите купить "${productName}"?`)) {
                button.textContent = 'Покупка...';
                button.disabled = true;
            } else {
                e.preventDefault();
            }
        });
    });
    
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.cursor = 'pointer';
        });
    });
});