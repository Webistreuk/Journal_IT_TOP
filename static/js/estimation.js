document.addEventListener('DOMContentLoaded', function() {
    const dateSearch = document.getElementById('dateSearch');
    const studentSearch = document.getElementById('studentSearch');
    const groupFilter = document.getElementById('groupFilter');
    const gradeFilter = document.getElementById('gradeFilter');
    const resetBtn = document.getElementById('resetFilters');
    const tableBody = document.getElementById('tableBody');
    
    let lastValue = '';
    
    function formatDateInput(input) {
        let cursorPosition = input.selectionStart;
        let rawValue = input.value.replace(/\D/g, '');
        
        let year = '';
        let month = '';
        let day = '';
        
        if (rawValue.length > 0) {
            let yearRaw = rawValue.slice(0, 4);
            let yearNum = parseInt(yearRaw);
            
            if (rawValue.length >= 1) {
                if (yearRaw.length >= 1 && parseInt(yearRaw[0]) > 2) {
                    yearRaw = '2';
                }
            }
            if (rawValue.length >= 2) {
                if (parseInt(yearRaw.slice(0, 2)) > 20) {
                    yearRaw = '20';
                }
            }
            if (rawValue.length >= 3) {
                if (parseInt(yearRaw.slice(0, 3)) > 203) {
                    yearRaw = '203';
                }
            }
            if (rawValue.length >= 4) {
                if (yearNum < 2000) yearNum = 2000;
                if (yearNum > 2030) yearNum = 2030;
                yearRaw = yearNum.toString();
            }
            
            year = yearRaw;
            
            if (rawValue.length >= 4) {
                month = rawValue.slice(4, 6);
                if (month && parseInt(month) > 12) {
                    month = '12';
                }
            }
            if (rawValue.length >= 6) {
                day = rawValue.slice(6, 8);
                let maxDay = 31;
                if (year && month) {
                    maxDay = new Date(parseInt(year), parseInt(month), 0).getDate();
                }
                if (day && parseInt(day) > maxDay) {
                    day = maxDay.toString();
                }
            }
        }
        
        let formatted = '';
        if (year) {
            formatted = year;
            if (month) {
                formatted += '-' + month;
                if (day) {
                    formatted += '-' + day;
                }
            }
        }
        
        input.value = formatted;
        
        let newCursorPos = cursorPosition;
        if (formatted.length > lastValue.length) {
            if (formatted[cursorPosition - 1] === '-') {
                newCursorPos = cursorPosition + 1;
            }
        } else if (formatted.length < lastValue.length) {
            if (lastValue[cursorPosition] === '-') {
                newCursorPos = cursorPosition;
            }
        }
        
        lastValue = formatted;
        input.setSelectionRange(newCursorPos, newCursorPos);
    }
    
    if (!tableBody) return;
    
    const rows = Array.from(tableBody.querySelectorAll('tr:not(.empty-row)'));
    
    function filterTable() {
        const searchDate = dateSearch ? dateSearch.value.toLowerCase() : '';
        const searchStudent = studentSearch ? studentSearch.value.toLowerCase() : '';
        const selectedGroup = groupFilter ? groupFilter.value : 'all';
        const selectedGrade = gradeFilter ? gradeFilter.value : 'all';
        
        rows.forEach(row => {
            const date = row.getAttribute('data-date') || '';
            const grade = row.getAttribute('data-grade') || '';
            const student = row.getAttribute('data-student') || '';
            const group = row.getAttribute('data-group') || '';
            
            let show = true;
            
            if (searchDate && !date.includes(searchDate)) show = false;
            if (searchStudent && !student.toLowerCase().includes(searchStudent)) show = false;
            if (selectedGroup !== 'all' && group !== selectedGroup) show = false;
            if (selectedGrade !== 'all' && grade !== selectedGrade) show = false;
            
            row.style.display = show ? '' : 'none';
        });
    }
    
    function resetFilters() {
        if (dateSearch) {
            dateSearch.value = '';
            lastValue = '';
        }
        if (studentSearch) studentSearch.value = '';
        if (groupFilter) groupFilter.value = 'all';
        if (gradeFilter) gradeFilter.value = 'all';
        filterTable();
    }
    
    if (dateSearch) {
        dateSearch.addEventListener('input', function(e) {
            formatDateInput(this);
            filterTable();
        });
    }
    if (studentSearch) studentSearch.addEventListener('input', filterTable);
    if (groupFilter) groupFilter.addEventListener('change', filterTable);
    if (gradeFilter) gradeFilter.addEventListener('change', filterTable);
    if (resetBtn) resetBtn.addEventListener('click', resetFilters);
    
    filterTable();
});