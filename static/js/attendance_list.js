document.addEventListener('DOMContentLoaded', function() {
    const dateSearch = document.getElementById('dateSearch');
    const statusFilter = document.getElementById('statusFilter');
    const subjectFilter = document.getElementById('subjectFilter');
    const resetBtn = document.getElementById('resetBtn');
    const tableBody = document.getElementById('tableBody');
    
    if (!tableBody) return;
    
    let lastValue = '';
    
    function validateDatePart(year, month, day) {
        if (year) {
            let yearNum = parseInt(year);
            if (yearNum < 2000) yearNum = 2000;
            if (yearNum > 2030) yearNum = 2030;
            year = yearNum.toString();
        }
        
        if (month && (parseInt(month) < 1 || parseInt(month) > 12)) {
            return false;
        }
        
        if (year && month && day) {
            const dayNum = parseInt(day);
            const monthNum = parseInt(month);
            const yearNum = parseInt(year);
            
            const daysInMonth = new Date(yearNum, monthNum, 0).getDate();
            if (dayNum < 1 || dayNum > daysInMonth) {
                return false;
            }
        } else if (month && day) {
            const dayNum = parseInt(day);
            if (dayNum < 1 || dayNum > 31) {
                return false;
            }
        }
        return true;
    }
    
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
    
    function filterTable() {
        const searchDate = dateSearch ? dateSearch.value.toLowerCase() : '';
        const selectedStatus = statusFilter ? statusFilter.value : 'all';
        const selectedSubject = subjectFilter ? subjectFilter.value : 'all';
        
        const rows = tableBody.querySelectorAll('tr');
        
        rows.forEach(row => {
            if (row.classList.contains('empty-row')) return;
            
            const date = row.getAttribute('data-date') || '';
            const status = row.getAttribute('data-status') || '';
            const subject = row.getAttribute('data-subject') || '';
            
            let show = true;
            
            if (searchDate && !date.includes(searchDate)) show = false;
            if (selectedStatus !== 'all' && status !== selectedStatus) show = false;
            if (selectedSubject !== 'all' && subject !== selectedSubject) show = false;
            
            row.style.display = show ? '' : 'none';
        });
    }
    
    function resetFilters() {
        if (dateSearch) {
            dateSearch.value = '';
            lastValue = '';
            filterTable();
        }
        if (statusFilter) statusFilter.value = 'all';
        if (subjectFilter) subjectFilter.value = 'all';
        filterTable();
    }
    
    if (dateSearch) {
        dateSearch.addEventListener('input', function(e) {
            formatDateInput(this);
            filterTable();
        });
    }
    if (statusFilter) statusFilter.addEventListener('change', filterTable);
    if (subjectFilter) subjectFilter.addEventListener('change', filterTable);
    if (resetBtn) resetBtn.addEventListener('click', resetFilters);
    
    filterTable();
});