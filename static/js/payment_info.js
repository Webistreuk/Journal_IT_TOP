document.addEventListener('DOMContentLoaded', function() {
    const showBtn = document.getElementById('showAddFormBtn');
    const hideBtn = document.getElementById('hideFormBtn');
    const paymentForm = document.getElementById('paymentForm');
    const searchInput = document.getElementById('searchInput');
    const monthFilter = document.getElementById('monthFilter');
    const table = document.getElementById('paymentsTable');
    const rows = table.querySelectorAll('tbody tr:not(.empty-row)');

    showBtn.addEventListener('click', function() {
        paymentForm.style.display = 'block';
    });

    hideBtn.addEventListener('click', function() {
        paymentForm.style.display = 'none';
    });

    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedMonth = monthFilter.value;

        rows.forEach(row => {
            const student = row.getAttribute('data-student') || '';
            const month = row.getAttribute('data-month') || '';
            
            const matchesSearch = student.toLowerCase().includes(searchTerm);
            const matchesMonth = !selectedMonth || month === selectedMonth;
            
            row.style.display = (matchesSearch && matchesMonth) ? '' : 'none';
        });
    }

    searchInput.addEventListener('input', filterTable);
    monthFilter.addEventListener('change', filterTable);
});