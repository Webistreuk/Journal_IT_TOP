document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pollForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const selectedOption = document.querySelector('input[name="option"]:checked');
            
            if (!selectedOption) {
                e.preventDefault();
                alert('Пожалуйста, выберите вариант ответа');
            } else {
                const confirmMessage = confirm('Вы уверены, что хотите проголосовать? Голос изменить будет нельзя.');
                if (!confirmMessage) {
                    e.preventDefault();
                }
            }
        });
    }
    
    const optionItems = document.querySelectorAll('.option-item');
    optionItems.forEach(item => {
        item.addEventListener('click', function() {
            const radio = this.querySelector('input[type="radio"]');
            if (radio && !radio.disabled) {
                radio.checked = true;
                
                optionItems.forEach(oi => oi.classList.remove('selected'));
                this.classList.add('selected');
            }
        });
    });
});