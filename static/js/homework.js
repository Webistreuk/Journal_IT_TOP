document.querySelectorAll('.btn-show-more').forEach(button => {
        const targetId = button.getAttribute('data-target');
        const grid = document.getElementById(targetId);
        const items = grid.querySelectorAll('.homework-card');
        let visibleCount = 6;
        
        if (items.length <= 6) {
            button.style.display = 'none';
        }
        
        for (let i = 6; i < items.length; i++) {
            items[i].style.display = 'none';
        }
        
        button.addEventListener('click', function() {
            let nextCount = visibleCount + 6;
            for (let i = visibleCount; i < nextCount && i < items.length; i++) {
                items[i].style.display = 'block';
            }
            visibleCount = nextCount;
            
            if (visibleCount >= items.length) {
                button.style.display = 'none';
            }
            
            if (button.parentElement) {
                button.parentElement.appendChild(button);
            }
        });
    });