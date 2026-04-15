document.addEventListener('DOMContentLoaded', function() {
    const dateSearch = document.getElementById('dateSearch');
    const statusFilter = document.getElementById('statusFilter');
    const subjectFilter = document.getElementById('subjectFilter');
    const table = document.getElementById('attendanceTable');
    const rows = table.querySelectorAll('tbody tr:not(.empty-row)');

    function filterTable() {
        const searchTerm = dateSearch.value.toLowerCase();
        const selectedStatus = statusFilter.value;
        const selectedSubject = subjectFilter.value;

        rows.forEach(row => {
            const date = row.getAttribute('data-date') || '';
            const status = row.getAttribute('data-status') || '';
            const subject = row.getAttribute('data-subject') || '';
            
            const matchesDate = !searchTerm || date.includes(searchTerm);
            const matchesStatus = !selectedStatus || status === selectedStatus;
            const matchesSubject = !selectedSubject || subject === selectedSubject;
            
            if (matchesDate && matchesStatus && matchesSubject) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    dateSearch.addEventListener('input', filterTable);
    statusFilter.addEventListener('change', filterTable);
    subjectFilter.addEventListener('change', filterTable);
});