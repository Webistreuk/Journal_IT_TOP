document.addEventListener('DOMContentLoaded', function() {
    const submissionItems = document.querySelectorAll('.submission-item');
    
    submissionItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        
        item.addEventListener('mouseleave', function() {
            if (!this.classList.contains('unchecked')) {
                this.style.backgroundColor = '';
            } else {
                this.style.backgroundColor = '#fff8e1';
            }
        });
    });
});