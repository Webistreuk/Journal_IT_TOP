document.addEventListener('DOMContentLoaded', function() {
    const scheduleSelect = document.getElementById('scheduleSelect');
    const pairSelect = document.getElementById('pairSelect');
    const formContainer = document.getElementById('attendanceFormContainer');
    const studentsList = document.getElementById('studentsList');
    const scheduleIdInput = document.getElementById('scheduleId');
    const pairIdInput = document.getElementById('pairId');
    const groupNameSpan = document.getElementById('groupName');
    const scheduleDateSpan = document.getElementById('scheduleDate');
    const pairInfoSpan = document.getElementById('pairInfo');

    function getStudentsByScheduleAndPair(scheduleId, pairId) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch(`/api/get-students/?schedule_id=${scheduleId}&pair_id=${pairId}`, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                groupNameSpan.textContent = data.group_name;
                scheduleDateSpan.textContent = data.schedule_date;
                pairInfoSpan.textContent = data.pair_info;
                scheduleIdInput.value = scheduleId;
                pairIdInput.value = pairId;
                
                studentsList.innerHTML = '';
                data.students.forEach(student => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><strong>${student.name}</strong></td>
                        <td>
                            <select name="status_${student.id}" class="status-select">
                                <option value="presence">✅ Присутствует</option>
                                <option value="late">⚠️ Опоздал</option>
                                <option value="absence">❌ Отсутствует</option>
                            </select>
                        </td>
                        <td>
                            <input type="text" name="comment_${student.id}" class="comment-input" placeholder="Комментарий">
                        </td>
                    `;
                    studentsList.appendChild(row);
                });
                
                formContainer.style.display = 'block';
            }
        });
    }

    scheduleSelect.addEventListener('change', function() {
        const scheduleId = this.value;
        if (scheduleId) {
            fetch(`/api/get-pairs/?schedule_id=${scheduleId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    pairSelect.innerHTML = '<option value="">Выберите пару</option>';
                    data.pairs.forEach(pair => {
                        const option = document.createElement('option');
                        option.value = pair.id;
                        option.textContent = `${pair.number} пара: ${pair.subject} (${pair.professor})`;
                        pairSelect.appendChild(option);
                    });
                    pairSelect.style.display = 'block';
                    formContainer.style.display = 'none';
                }
            });
        } else {
            pairSelect.style.display = 'none';
            formContainer.style.display = 'none';
        }
    });

    pairSelect.addEventListener('change', function() {
        const scheduleId = scheduleSelect.value;
        const pairId = this.value;
        
        if (scheduleId && pairId) {
            getStudentsByScheduleAndPair(scheduleId, pairId);
        }
    });

    const quickButtons = document.querySelectorAll('.btn-quick');
    quickButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const status = this.getAttribute('data-status');
            const selects = document.querySelectorAll('.status-select');
            selects.forEach(select => {
                select.value = status;
                select.className = `status-select ${status}`;
            });
        });
    });

    document.addEventListener('change', function(e) {
        if (e.target.classList && e.target.classList.contains('status-select')) {
            e.target.className = `status-select ${e.target.value}`;
        }
    });
});