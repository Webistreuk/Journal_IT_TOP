document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleLeaderboard');
    const courseBoard = document.getElementById('courseLeaderboard');
    const groupBoard = document.getElementById('groupLeaderboard');
    const title = document.getElementById('leaderboardTitle');
    
    let showCourse = true;
    let currentPage = 1;
    const itemsPerPage = 10;
    
    let courseData = window.courseData || [];
    const currentStudentId = window.studentId;
    
    function renderCoursePage(page) {
        if (!courseData || courseData.length === 0) {
            const tbody = document.getElementById('courseTableBody');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="4" class="empty-state">Нет данных для отображения</td></tr>';
            }
            const paginationDiv = document.getElementById('coursePagination');
            if (paginationDiv) paginationDiv.innerHTML = '';
            return;
        }
        
        const totalPages = Math.ceil(courseData.length / itemsPerPage);
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const pageData = courseData.slice(start, end);
        
        const tbody = document.getElementById('courseTableBody');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        
        for (let i = 0; i < pageData.length; i++) {
            const item = pageData[i];
            const row = tbody.insertRow();
            const rankCell = row.insertCell(0);
            const nameCell = row.insertCell(1);
            const groupCell = row.insertCell(2);
            const topmoneyCell = row.insertCell(3);
            
            let rankHtml = '';
            if (item.rank === 1) rankHtml = '🥇 1';
            else if (item.rank === 2) rankHtml = '🥈 2';
            else if (item.rank === 3) rankHtml = '🥉 3';
            else rankHtml = item.rank;
            
            rankCell.className = 'rank-cell rank-' + item.rank;
            rankCell.innerHTML = rankHtml;
            
            nameCell.className = 'student-name';
            nameCell.textContent = item.student.surname + ' ' + item.student.name + ' ' + item.student.patronymic;
            
            groupCell.className = 'group-name';
            groupCell.textContent = item.student.group.name;
            
            topmoneyCell.className = 'topmoney-value';
            topmoneyCell.textContent = item.topmoney;
            
            if (item.student.id === currentStudentId) {
                row.classList.add('current-user');
            }
        }
        
        const emptyRows = 10 - pageData.length;
        for (let i = 0; i < emptyRows; i++) {
            const row = tbody.insertRow();
            row.style.height = '53px';
            const emptyCell = row.insertCell(0);
            emptyCell.colSpan = 4;
            emptyCell.style.border = 'none';
            emptyCell.style.backgroundColor = 'transparent';
            emptyCell.style.pointerEvents = 'none';
        }
        
        renderPagination(totalPages, page);
        currentPage = page;
    }
    
    function renderPagination(totalPages, currentPage) {
        const paginationDiv = document.getElementById('coursePagination');
        if (!paginationDiv) return;
        
        if (totalPages <= 1) {
            paginationDiv.innerHTML = '';
            return;
        }
        
        let html = '';
        
        html += '<button class="pagination-btn ' + (currentPage === 1 ? 'disabled' : '') + '" data-page="first">⏮ Первая</button>';
        html += '<button class="pagination-btn ' + (currentPage === 1 ? 'disabled' : '') + '" data-page="prev">◀ Назад</button>';
        
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, currentPage + 2);
        
        if (startPage > 1) {
            html += '<button class="pagination-btn" data-page="1">1</button>';
            if (startPage > 2) html += '<span class="pagination-dots">...</span>';
        }
        
        for (let i = startPage; i <= endPage; i++) {
            html += '<button class="pagination-btn ' + (i === currentPage ? 'active' : '') + '" data-page="' + i + '">' + i + '</button>';
        }
        
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) html += '<span class="pagination-dots">...</span>';
            html += '<button class="pagination-btn" data-page="' + totalPages + '">' + totalPages + '</button>';
        }
        
        html += '<button class="pagination-btn ' + (currentPage === totalPages ? 'disabled' : '') + '" data-page="next">Вперед ▶</button>';
        html += '<button class="pagination-btn ' + (currentPage === totalPages ? 'disabled' : '') + '" data-page="last">Последняя ⏭</button>';
        
        paginationDiv.innerHTML = html;
        
        const buttons = paginationDiv.querySelectorAll('.pagination-btn');
        for (let i = 0; i < buttons.length; i++) {
            const btn = buttons[i];
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                if (this.classList.contains('disabled')) return;
                
                const action = this.getAttribute('data-page');
                let newPage = currentPage;
                
                if (action === 'first') newPage = 1;
                else if (action === 'prev') newPage = Math.max(1, currentPage - 1);
                else if (action === 'next') newPage = Math.min(totalPages, currentPage + 1);
                else if (action === 'last') newPage = totalPages;
                else newPage = parseInt(action);
                
                if (newPage !== currentPage) {
                    renderCoursePage(newPage);
                }
            });
        }
    }
    
    function updateView() {
        if (showCourse) {
            courseBoard.classList.add('active');
            groupBoard.classList.remove('active');
            title.innerHTML = '🏆 Рейтинг курса';
            toggleBtn.innerHTML = '📊 Рейтинг группы';
            if (courseData.length > 0) {
                renderCoursePage(1);
            } else {
                const tbody = document.getElementById('courseTableBody');
                if (tbody) {
                    tbody.innerHTML = '<tr><td colspan="4" class="empty-state">Нет данных для отображения</td></tr>';
                }
            }
        } else {
            courseBoard.classList.remove('active');
            groupBoard.classList.add('active');
            title.innerHTML = '🏆 Рейтинг группы';
            toggleBtn.innerHTML = '🎓 Рейтинг курса';
        }
    }
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            showCourse = !showCourse;
            updateView();
        });
    }
    
    updateView();
});