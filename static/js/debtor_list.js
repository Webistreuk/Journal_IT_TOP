document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const groupFilter = document.getElementById('groupFilter');
    const table = document.getElementById('debtorsTable');
    const rows = table.querySelectorAll('tbody tr');

    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedGroup = groupFilter.value;

        rows.forEach(row => {
            if (row.classList.contains('empty-row')) return;
            
            const name = row.getAttribute('data-name') || '';
            const group = row.getAttribute('data-group') || '';
            
            const matchesSearch = name.toLowerCase().includes(searchTerm);
            const matchesGroup = !selectedGroup || group === selectedGroup;
            
            if (matchesSearch && matchesGroup) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterTable);
    groupFilter.addEventListener('change', filterTable);

    const notifyButtons = document.querySelectorAll('.btn-notify');
    const markPaidButtons = document.querySelectorAll('.btn-mark-paid');

    notifyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const debtorId = this.getAttribute('data-id');
            alert(`📧 Уведомление отправлено должнику ID: ${debtorId}`);
        });
    });

    markPaidButtons.forEach(button => {
        button.addEventListener('click', function() {
            const debtorId = this.getAttribute('data-id');
            if (confirm(`Отметить оплату для должника ID: ${debtorId}?`)) {
                alert(`✅ Оплата отмечена для ID: ${debtorId}`);
                this.disabled = true;
                const row = this.closest('tr');
                const statusCell = row.querySelector('.status-unpaid');
                if (statusCell) {
                    statusCell.className = 'status-paid';
                    statusCell.textContent = '✅ Оплачено';
                }
            }
        });
    });
});