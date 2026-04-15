document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.homework-table tbody tr');
    rows.forEach(row => {
        row.addEventListener('click', function(e) {
            if (e.target.tagName !== 'A') {
                const link = this.querySelector('.btn-submit');
                if (link) window.location.href = link.href;
            }
        });
    });
});