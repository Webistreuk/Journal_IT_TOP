let currentPairId = null;
let currentGroup = null;
let currentSubject = null;
let currentTime = null;
let pairData = {};
let autoCheckInterval = null;
let isViewMode = false;
let autoSaveInterval = null;

document.addEventListener('DOMContentLoaded', function() {
    checkExpiredPairs();
    
    autoCheckInterval = setInterval(function() {
        checkExpiredPairs();
    }, 60000);
    
    document.querySelectorAll('.btn-mark').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            currentPairId = this.dataset.pairId;
            currentGroup = this.dataset.group;
            currentSubject = this.dataset.subject;
            currentTime = this.dataset.time;
            const action = this.dataset.action || (this.disabled ? 'view' : 'mark');
            isViewMode = (this.dataset.status === 'completed' || this.dataset.status === 'missed' || action === 'view');
            
            const savedData = localStorage.getItem('attendance_pair_' + currentPairId);
            if (savedData) {
                pairData[currentPairId] = JSON.parse(savedData);
            } else {
                pairData[currentPairId] = {
                    topic: '',
                    students: {}
                };
            }
            
            loadStudents(currentPairId, currentGroup, currentSubject, currentTime, isViewMode);
        });
    });

    var closeBtn = document.getElementById('closeModalBtn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            document.getElementById('attendanceModal').style.display = 'none';
            if (autoSaveInterval) {
                clearInterval(autoSaveInterval);
                autoSaveInterval = null;
            }
        });
    }
});

function startAutoSave() {
    if (autoSaveInterval) {
        clearInterval(autoSaveInterval);
    }
    autoSaveInterval = setInterval(function() {
        if (pairData[currentPairId] && document.getElementById('attendanceModal').style.display === 'flex') {
            saveToLocalStorage();
        }
    }, 30000);
}

function checkExpiredPairs() {
    var now = new Date();
    var currentTimeMinutes = now.getHours() * 60 + now.getMinutes();
    
    var pairs = document.querySelectorAll('.pair-item');
    for (var i = 0; i < pairs.length; i++) {
        var pairElement = pairs[i];
        var pairId = pairElement.dataset.pairId;
        var pairStatus = pairElement.dataset.pairStatus;
        var pairEndTime = pairElement.dataset.pairEndTime;
        
        if (pairStatus === 'completed' || pairStatus === 'missed') {
            continue;
        }
        
        if (pairEndTime) {
            var endParts = pairEndTime.split(':');
            var endHour = parseInt(endParts[0]);
            var endMin = parseInt(endParts[1]);
            var endMinutes = endHour * 60 + endMin + 10;
            
            if (endMinutes > 24 * 60) {
                endMinutes = 24 * 60;
            }
            
            if (currentTimeMinutes > endMinutes) {
                fetch('/api/attendance/pair/' + pairId + '/miss/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.success) {
                        pairElement.dataset.pairStatus = 'missed';
                        var statusSpan = pairElement.querySelector('.status-badge');
                        statusSpan.className = 'status-badge missed';
                        statusSpan.innerHTML = '❌ Не проведена';
                        pairElement.style.borderLeftColor = '#dc3545';
                        pairElement.style.background = '#2a1e1e';
                        
                        var button = pairElement.querySelector('.btn-mark');
                        button.disabled = false;
                        button.style.cursor = 'pointer';
                        button.style.opacity = '1';
                        button.innerHTML = 'Просмотр';
                        button.dataset.action = 'view';
                        button.dataset.status = 'missed';
                        
                        localStorage.removeItem('attendance_pair_' + pairId);
                    }
                });
            }
        }
    }
}

function loadStudents(pairId, group, subject, time, viewMode) {
    var url = '/api/attendance/students/' + pairId + '/?group=' + encodeURIComponent(group);
    fetch(url)
        .then(function(response) { return response.json(); })
        .then(function(data) {
            if (data.success) {
                renderModal(data, group, subject, time, viewMode);
                document.getElementById('attendanceModal').style.display = 'flex';
                startAutoSave();
            } else {
                alert('Ошибка загрузки студентов');
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            alert('Ошибка загрузки данных');
        });
}

function renderModal(data, group, subject, time, viewMode) {
    var modalBody = document.getElementById('modalBody');
    document.getElementById('modalTitle').innerHTML = subject + ' - ' + group;
    
    var url = '/api/attendance/pair/' + currentPairId + '/get/';
    fetch(url)
        .then(function(response) { return response.json(); })
        .then(function(pairInfo) {
            var savedTopic = pairInfo.topic || '';
            var studentsData = pairInfo.students || {};
            var isMissed = pairInfo.is_missed === true;
            var isCompleted = pairInfo.is_completed === true;
            
            var html = '';
            html += '<div class="modal-info">';
            html += '<div class="info-row"><span class="info-label">📚 Предмет:</span><span class="info-value">' + subject + '</span></div>';
            html += '<div class="info-row"><span class="info-label">👥 Группа:</span><span class="info-value">' + group + '</span></div>';
            html += '<div class="info-row"><span class="info-label">⏰ Время:</span><span class="info-value">' + time + '</span></div>';
            html += '</div>';
            
            html += '<div class="topic-section">';
            html += '<label>📝 Тема занятия</label>';
            html += '<input type="text" id="topicInput" class="topic-input" placeholder="Введите тему занятия..." value="' + escapeHtml(pairData[currentPairId]?.topic || savedTopic) + '"' + (viewMode ? ' disabled' : '') + '>';
            html += '</div>';
            
            html += '<div class="students-section">';
            html += '<h4>👨‍🎓 Студенты группы ' + group + '</h4>';
            html += '<div class="students-table-wrapper">';
            html += '<table class="students-table">';
            html += '<thead><tr><th>Студент</th><th>Статус</th>';
            if (!viewMode) {
                html += '<th>Оценка (1-5)</th>';
            } else {
                html += '<th>Оценка</th>';
            }
            html += '<th>Комментарий</th>';
            if (!viewMode) {
                html += '<th>Бонусы</th>';
            }
            html += '</thead>';
            html += '<tbody id="studentsBody">';
            
            if (isMissed) {
                html += '<tr><td colspan="4" class="empty-state" style="text-align: center; padding: 40px;">❌ Пара не была проведена<br><small>Статусы студентов не отмечались</small></td></tr>';
            } else {
                for (var i = 0; i < data.students.length; i++) {
                    var student = data.students[i];
                    var studentInfo = studentsData[student.id] || {};
                    var localStudentData = (pairData[currentPairId] && pairData[currentPairId].students[student.id]) || {};
                    var savedStatus = localStudentData.status || studentInfo.status || '';
                    var savedGrade = localStudentData.grade || studentInfo.grade || '';
                    var savedComment = localStudentData.comment || studentInfo.comment || '';
                    
                    if (!viewMode && !isCompleted && savedStatus === '') {
                        savedStatus = 'presence';
                    }
                    
                    if (viewMode || isCompleted) {
                        var statusText = '—';
                        if (savedStatus === 'presence') statusText = '✅ Присутствует';
                        else if (savedStatus === 'late') statusText = '⏰ Опоздал';
                        else if (savedStatus === 'absence') statusText = '❌ Отсутствует';
                        
                        html += '<tr data-student-id="' + student.id + '">';
                        html += '<td class="student-cell"><div class="student-info"><div class="student-avatar">' + student.initials + '</div><div class="student-name">' + student.full_name + '</div></div></td>';
                        html += '<td class="status-cell"><div class="status-display">' + statusText + '</div></td>';
                        html += '<td class="grade-cell"><div class="grade-display">' + (savedGrade || '—') + '</div></td>';
                        html += '<td class="comment-cell"><div class="comment-display">' + escapeHtml(savedComment || '—') + '</div></td>';
                        html += '</tr>';
                    } else {
                        var activePresence = (savedStatus === 'presence') ? 'active' : '';
                        var activeLate = (savedStatus === 'late') ? 'active' : '';
                        var activeAbsence = (savedStatus === 'absence') ? 'active' : '';
                        
                        html += '<tr data-student-id="' + student.id + '">';
                        html += '<td class="student-cell"><div class="student-info"><div class="student-avatar">' + student.initials + '</div><div class="student-name">' + student.full_name + '</div></div></td>';
                        html += '<td class="status-cell">';
                        html += '<div class="status-buttons">';
                        html += '<button type="button" class="status-btn presence ' + activePresence + '" data-status="presence">✅</button>';
                        html += '<button type="button" class="status-btn late ' + activeLate + '" data-status="late">⏰</button>';
                        html += '<button type="button" class="status-btn absence ' + activeAbsence + '" data-status="absence">❌</button>';
                        html += '</div>';
                        html += '<input type="hidden" class="attendance-input" value="' + savedStatus + '">';
                        html += '</td>';
                        html += '<td class="grade-cell">';
                        html += '<select class="grade-select" data-student="' + student.id + '">';
                        html += '<option value="">—</option>';
                        html += '<option value="1"' + (savedGrade === '1' ? ' selected' : '') + '>1</option>';
                        html += '<option value="2"' + (savedGrade === '2' ? ' selected' : '') + '>2</option>';
                        html += '<option value="3"' + (savedGrade === '3' ? ' selected' : '') + '>3</option>';
                        html += '<option value="4"' + (savedGrade === '4' ? ' selected' : '') + '>4</option>';
                        html += '<option value="5"' + (savedGrade === '5' ? ' selected' : '') + '>5</option>';
                        html += '</select>';
                        html += '</td>';
                        html += '<td class="comment-cell">';
                        html += '<input type="text" class="comment-input" placeholder="Комментарий..." value="' + escapeHtml(savedComment) + '" data-student-id="' + student.id + '">';
                        html += '</td>';
                        html += '<td class="bonus-cell">';
                        html += '<div class="bonus-controls">';
                        html += '<button type="button" class="bonus-btn" data-bonus="5" data-student="' + student.id + '">+5₿</button>';
                        html += '<button type="button" class="bonus-btn" data-bonus="10" data-student="' + student.id + '">+10₿</button>';
                        html += '<button type="button" class="bonus-btn" data-bonus="20" data-student="' + student.id + '">+20₿</button>';
                        html += '<input type="number" class="bonus-custom" placeholder="Своё" min="1" max="100" data-student="' + student.id + '">';
                        html += '</div>';
                        html += '</td>';
                        html += '</tr>';
                    }
                }
            }
            
            html += '</tbody></table></div></div>';
            
            if (!viewMode && !isMissed && !isCompleted) {
                html += '<div class="form-actions"><button id="completePairBtn" class="btn-complete">✅ Завершить пару</button></div>';
            }
            
            modalBody.innerHTML = html;
            
            if (!viewMode && !isMissed && !isCompleted) {
                attachModalEvents();
            }
        });
}

function attachModalEvents() {
    var statusBtns = document.querySelectorAll('.status-btn');
    for (var i = 0; i < statusBtns.length; i++) {
        var btn = statusBtns[i];
        btn.addEventListener('click', function(e) {
            var row = this.closest('tr');
            var status = this.dataset.status;
            var buttons = row.querySelectorAll('.status-btn');
            var hiddenInput = row.querySelector('.attendance-input');
            
            for (var j = 0; j < buttons.length; j++) {
                buttons[j].classList.remove('active');
            }
            this.classList.add('active');
            hiddenInput.value = status;
            
            var studentId = row.dataset.studentId;
            if (!pairData[currentPairId]) {
                pairData[currentPairId] = { topic: '', students: {} };
            }
            if (!pairData[currentPairId].students[studentId]) {
                pairData[currentPairId].students[studentId] = {};
            }
            pairData[currentPairId].students[studentId].status = status;
            saveToLocalStorage();
        });
    }
    
    var bonusBtns = document.querySelectorAll('.bonus-btn');
    for (var i = 0; i < bonusBtns.length; i++) {
        var btn = bonusBtns[i];
        btn.addEventListener('click', function(e) {
            var studentId = this.dataset.student;
            var bonus = parseInt(this.dataset.bonus);
            var commentInput = document.querySelector('.comment-input[data-student-id="' + studentId + '"]');
            var currentComment = commentInput ? commentInput.value : '';
            var newComment = currentComment ? currentComment + ' | +' + bonus + '₿' : '+' + bonus + '₿';
            if (commentInput) commentInput.value = newComment;
            
            fetch('/api/add-bonus/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ student_id: studentId, bonus: bonus })
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                if (data.success) {
                    if (!pairData[currentPairId]) {
                        pairData[currentPairId] = { topic: '', students: {} };
                    }
                    if (!pairData[currentPairId].students[studentId]) {
                        pairData[currentPairId].students[studentId] = {};
                    }
                    pairData[currentPairId].students[studentId].bonus = (pairData[currentPairId].students[studentId].bonus || 0) + bonus;
                    pairData[currentPairId].students[studentId].comment = newComment;
                    
                    saveToLocalStorage();
                    showToast('+' + bonus + ' топкоинов добавлено студенту', 'success');
                } else {
                    showToast('Ошибка начисления бонусов', 'error');
                }
            })
            .catch(function(error) {
                console.error('Error:', error);
                showToast('Ошибка сервера', 'error');
            });
        });
    }
    
    var bonusCustoms = document.querySelectorAll('.bonus-custom');
    for (var i = 0; i < bonusCustoms.length; i++) {
        var input = bonusCustoms[i];
        input.addEventListener('change', function(e) {
            var studentId = this.dataset.student;
            var bonus = parseInt(this.value);
            if (bonus && bonus > 0 && bonus <= 100) {
                var commentInput = document.querySelector('.comment-input[data-student-id="' + studentId + '"]');
                var currentComment = commentInput ? commentInput.value : '';
                var newComment = currentComment ? currentComment + ' | +' + bonus + '₿' : '+' + bonus + '₿';
                if (commentInput) commentInput.value = newComment;
                
                fetch('/api/add-bonus/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ student_id: studentId, bonus: bonus })
                })
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    if (data.success) {
                        if (!pairData[currentPairId]) {
                            pairData[currentPairId] = { topic: '', students: {} };
                        }
                        if (!pairData[currentPairId].students[studentId]) {
                            pairData[currentPairId].students[studentId] = {};
                        }
                        pairData[currentPairId].students[studentId].bonus = (pairData[currentPairId].students[studentId].bonus || 0) + bonus;
                        pairData[currentPairId].students[studentId].comment = newComment;
                        
                        saveToLocalStorage();
                        showToast('+' + bonus + ' топкоинов добавлено студенту', 'success');
                        this.value = '';
                    } else {
                        showToast('Ошибка начисления бонусов', 'error');
                    }
                });
            }
        });
    }
    
    var gradeSelects = document.querySelectorAll('.grade-select');
    for (var i = 0; i < gradeSelects.length; i++) {
        var select = gradeSelects[i];
        select.addEventListener('change', function(e) {
            var studentId = this.dataset.student;
            var grade = this.value;
            if (!pairData[currentPairId]) {
                pairData[currentPairId] = { topic: '', students: {} };
            }
            if (!pairData[currentPairId].students[studentId]) {
                pairData[currentPairId].students[studentId] = {};
            }
            pairData[currentPairId].students[studentId].grade = grade;
            saveToLocalStorage();
        });
    }
    
    var commentInputs = document.querySelectorAll('.comment-input');
    for (var i = 0; i < commentInputs.length; i++) {
        var input = commentInputs[i];
        input.addEventListener('input', function(e) {
            var studentId = this.dataset.studentId;
            var comment = this.value;
            if (!pairData[currentPairId]) {
                pairData[currentPairId] = { topic: '', students: {} };
            }
            if (!pairData[currentPairId].students[studentId]) {
                pairData[currentPairId].students[studentId] = {};
            }
            pairData[currentPairId].students[studentId].comment = comment;
            saveToLocalStorage();
        });
    }
    
    var topicInput = document.getElementById('topicInput');
    if (topicInput) {
        topicInput.addEventListener('input', function(e) {
            if (!pairData[currentPairId]) {
                pairData[currentPairId] = { topic: '', students: {} };
            }
            pairData[currentPairId].topic = this.value;
            saveToLocalStorage();
        });
    }
    
    var completeBtn = document.getElementById('completePairBtn');
    if (completeBtn) {
        completeBtn.addEventListener('click', function(e) {
            var topic = document.getElementById('topicInput').value;
            var allStudents = document.querySelectorAll('#studentsBody tr');
            var allMarked = true;
            
            if (!topic.trim()) {
                showToast('Сначала введите тему занятия!', 'error');
                return;
            }
            
            for (var i = 0; i < allStudents.length; i++) {
                var status = allStudents[i].querySelector('.attendance-input').value;
                if (!status) {
                    allMarked = false;
                    break;
                }
            }
            
            if (!allMarked) {
                showToast('Отметьте статус для всех студентов!', 'error');
                return;
            }
            
            if (confirm('Завершить пару? Это действие сохранит посещаемость и отметит пару как проведённую.')) {
                saveToServer(true);
            }
        });
    }
}

function saveToLocalStorage() {
    if (pairData[currentPairId]) {
        localStorage.setItem('attendance_pair_' + currentPairId, JSON.stringify(pairData[currentPairId]));
    }
}

function saveToServer(complete) {
    var topic = document.getElementById('topicInput').value;
    var students = [];
    
    var rows = document.querySelectorAll('#studentsBody tr');
    for (var i = 0; i < rows.length; i++) {
        var row = rows[i];
        var studentId = row.dataset.studentId;
        var status = row.querySelector('.attendance-input').value;
        var gradeSelect = row.querySelector('.grade-select');
        var grade = gradeSelect ? gradeSelect.value : '';
        var comment = row.querySelector('.comment-input').value;
        var bonus = (pairData[currentPairId] && pairData[currentPairId].students[studentId]) ? pairData[currentPairId].students[studentId].bonus || 0 : 0;
        
        if (status) {
            students.push({ 
                id: studentId, 
                status: status, 
                grade: grade,
                comment: comment,
                bonus: bonus
            });
        }
    }
    
    fetch('/api/attendance/save/' + currentPairId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ students: students, topic: topic, complete: complete })
    })
    .then(function(response) { return response.json(); })
    .then(function(data) {
        if (data.success) {
            if (complete) {
                localStorage.removeItem('attendance_pair_' + currentPairId);
                showToast('Пара завершена!', 'success');
                document.getElementById('attendanceModal').style.display = 'none';
                if (autoSaveInterval) {
                    clearInterval(autoSaveInterval);
                    autoSaveInterval = null;
                }
                markPairAsCompleted(currentPairId);
            }
        }
    });
}

function markPairAsCompleted(pairId) {
    var pairElement = document.querySelector('.pair-item[data-pair-id="' + pairId + '"]');
    if (pairElement) {
        pairElement.dataset.pairStatus = 'completed';
        var statusSpan = pairElement.querySelector('.status-badge');
        statusSpan.className = 'status-badge completed';
        statusSpan.innerHTML = '✅ Проведена';
        pairElement.style.borderLeftColor = '#28a745';
        pairElement.style.background = '#1e2a1e';
        
        var button = pairElement.querySelector('.btn-mark');
        button.disabled = false;
        button.style.cursor = 'pointer';
        button.style.opacity = '1';
        button.innerHTML = 'Просмотр';
        button.dataset.action = 'view';
        button.dataset.status = 'completed';
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

function showToast(message, type) {
    var toast = document.createElement('div');
    toast.className = 'toast-notification ' + type;
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.bottom = '30px';
    toast.style.right = '30px';
    toast.style.padding = '12px 24px';
    toast.style.borderRadius = '12px';
    toast.style.zIndex = '1001';
    toast.style.fontSize = '14px';
    toast.style.fontWeight = '600';
    toast.style.animation = 'slideIn 0.3s ease';
    if (type === 'success') {
        toast.style.background = '#28a745';
        toast.style.color = 'white';
    } else if (type === 'error') {
        toast.style.background = '#dc3545';
        toast.style.color = 'white';
    }
    document.body.appendChild(toast);
    setTimeout(function() { toast.remove(); }, 3000);
}

function getCookie(name) {
    var value = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            var parts = cookie.split('=');
            if (parts[0] === name) {
                value = decodeURIComponent(parts[1]);
                break;
            }
        }
    }
    return value;
}