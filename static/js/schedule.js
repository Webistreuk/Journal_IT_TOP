let currentWeekOffset = 0;
let isLoading = false;

function loadSchedule(offset) {
    if (isLoading) return;
    isLoading = true;
    
    fetch(`/api/schedule/${window.groupId}/?offset=${offset}`)
        .then(response => response.json())
        .then(data => {
            renderSchedule(data);
            currentWeekOffset = offset;
            isLoading = false;
            
            const goToTodayBtn = document.getElementById('goToTodayBtn');
            if (goToTodayBtn) {
                if (offset !== 0) {
                    goToTodayBtn.style.display = 'block';
                } else {
                    goToTodayBtn.style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('scheduleContent').innerHTML = '<div class="empty-state">❌ Ошибка загрузки расписания</div>';
            isLoading = false;
        });
}

function renderSchedule(data) {
    const contentDiv = document.getElementById('scheduleContent');
    const weekdays = [
        {num: 1, name: 'Понедельник'},
        {num: 2, name: 'Вторник'},
        {num: 3, name: 'Среда'},
        {num: 4, name: 'Четверг'},
        {num: 5, name: 'Пятница'},
        {num: 6, name: 'Суббота'},
        {num: 7, name: 'Воскресенье'}
    ];
    
    let html = `<div class="schedule-week"><div class="schedule-days">`;
    
    for (let i = 0; i < weekdays.length; i++) {
        const day = weekdays[i];
        const daySchedules = data.schedules.filter(s => s.weekday === day.num);
        daySchedules.sort((a, b) => a.pair_order - b.pair_order);
        
        let dayDate = '';
        if (data.dates && data.dates[day.num]) {
            dayDate = data.dates[day.num];
        }
        
        html += `
            <div class="day-column">
                <div class="day-header">
                    <span class="day-name">${day.name}</span>
                    ${dayDate ? `<span class="day-date">${dayDate}</span>` : ''}
                </div>
                <div class="day-pairs">
        `;
        
        if (daySchedules.length === 0) {
            html += `<div class="empty-pairs">Нет пар</div>`;
        } else {
            for (let j = 0; j < daySchedules.length; j++) {
                const pair = daySchedules[j];
                html += `
                    <div class="pair-card">
                        <div class="pair-time">${pair.pair_time}</div>
                        <div class="pair-subject">${pair.subject}</div>
                        <div class="pair-professor">${pair.professor}</div>
                        <div class="pair-classroom">${pair.classroom || '-'}</div>
                    </div>
                `;
            }
        }
        
        html += `
                </div>
            </div>
        `;
    }
    
    html += `</div></div>`;
    contentDiv.innerHTML = html;
}

function goToToday() {
    loadSchedule(0);
}

document.addEventListener('DOMContentLoaded', function() {
    const prevBtn = document.getElementById('prevWeekBtn');
    const nextBtn = document.getElementById('nextWeekBtn');
    const goToTodayBtn = document.getElementById('goToTodayBtn');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            loadSchedule(currentWeekOffset - 1);
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            loadSchedule(currentWeekOffset + 1);
        });
    }
    
    if (goToTodayBtn) {
        goToTodayBtn.addEventListener('click', function() {
            goToToday();
        });
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            loadSchedule(currentWeekOffset - 1);
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            loadSchedule(currentWeekOffset + 1);
        }
    });
    
    loadSchedule(0);
});