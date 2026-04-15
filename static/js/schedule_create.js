document.addEventListener('DOMContentLoaded', function() {
    let pairCount = 1;
    const pairsList = document.getElementById('pairsList');
    const addPairBtn = document.getElementById('addPairBtn');
    const form = document.getElementById('scheduleForm');

    addPairBtn.addEventListener('click', function() {
        const newPair = document.createElement('div');
        newPair.className = 'pair-item';
        newPair.setAttribute('data-index', pairCount);
        
        newPair.innerHTML = `
            <div class="pair-header">
                <span class="pair-number">Пара ${pairCount + 1}</span>
                <button type="button" class="btn-remove-pair">🗑️</button>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>День недели</label>
                    <select name="weekday_${pairCount}" class="form-control weekday-select">
                        <option value="1">Понедельник</option>
                        <option value="2">Вторник</option>
                        <option value="3">Среда</option>
                        <option value="4">Четверг</option>
                        <option value="5">Пятница</option>
                        <option value="6">Суббота</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Порядковый номер</label>
                    <input type="number" name="pair_order_${pairCount}" class="form-control pair-order" value="${pairCount + 1}" min="1" max="7">
                </div>
                <div class="form-group">
                    <label>Предмет</label>
                    <select name="subject_${pairCount}" class="form-control subject-select">
                        <option value="">Выберите предмет</option>
                        ${document.querySelector('.subject-select').innerHTML}
                    </select>
                </div>
                <div class="form-group">
                    <label>Преподаватель</label>
                    <select name="professor_${pairCount}" class="form-control professor-select">
                        <option value="">Выберите преподавателя</option>
                        ${document.querySelector('.professor-select').innerHTML}
                    </select>
                </div>
                <div class="form-group">
                    <label>Аудитория</label>
                    <select name="classroom_${pairCount}" class="form-control classroom-select">
                        <option value="">Выберите аудиторию</option>
                        ${document.querySelector('.classroom-select').innerHTML}
                    </select>
                </div>
            </div>
        `;
        
        pairsList.appendChild(newPair);
        pairCount++;
        
        const removeBtns = document.querySelectorAll('.btn-remove-pair');
        removeBtns.forEach(btn => {
            btn.disabled = false;
        });
        
        newPair.querySelector('.btn-remove-pair').addEventListener('click', function() {
            newPair.remove();
            pairCount--;
            if (pairCount === 1) {
                document.querySelector('.btn-remove-pair').disabled = true;
            }
        });
    });

    form.addEventListener('submit', function(e) {
        const group = document.getElementById('id_group').value;
        const semester = document.getElementById('id_semester').value;
        const weekStart = document.getElementById('id_week_start_date').value;
        
        if (!group || !semester || !weekStart) {
            e.preventDefault();
            alert('Пожалуйста, заполните все обязательные поля');
        }
    });
});