document.addEventListener('DOMContentLoaded', function() {
    const viewButtons = document.querySelectorAll('.btn-view');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const studentId = this.getAttribute('data-student');
            alert(`Просмотр профиля студента ID: ${studentId}`);
        });
    });
    
    const rows = document.querySelectorAll('.leaderboard-table tbody tr');
    rows.forEach(row => {
        row.addEventListener('click', function(e) {
            if (e.target.tagName !== 'BUTTON') {
                const studentName = this.querySelector('.student-name').textContent;
                console.log(`Выбран студент: ${studentName}`);
            }
        });
    });
});