document.addEventListener('DOMContentLoaded', function() {
    const studentSearch = document.getElementById('studentSearch');
    const studentResults = document.getElementById('studentResults');
    const selectedStudentInput = document.getElementById('selectedStudent');
    const submitBtn = document.getElementById('submitBtn');
    const commentTextarea = document.getElementById('id_comment');
    const charCountSpan = document.getElementById('charCount');
    let selectedStudentId = null;
    let searchTimeout = null;
    const allStudents = window.allStudents || [];

    function updateCharCount() {
        const length = commentTextarea.value.length;
        charCountSpan.textContent = length;
        if (length > 700) {
            charCountSpan.style.color = '#FFC619';
        } else if (length > 750) {
            charCountSpan.style.color = '#dc3545';
        } else {
            charCountSpan.style.color = '#F69020';
        }
    }

    function searchStudents() {
        const query = studentSearch.value.toLowerCase().trim();
        
        if (query.length < 2) {
            studentResults.classList.remove('active');
            studentResults.innerHTML = '';
            return;
        }
        
        const filtered = allStudents.filter(s => 
            s.full_name.toLowerCase().includes(query)
        );
        
        if (filtered.length === 0) {
            studentResults.innerHTML = '<div class="student-result-item" style="color: rgba(255,255,255,0.5);">😔 Студенты не найдены</div>';
            studentResults.classList.add('active');
            return;
        }
        
        studentResults.innerHTML = '';
        filtered.forEach(student => {
            const div = document.createElement('div');
            div.className = 'student-result-item';
            div.innerHTML = `
                <div class="student-result-name">${student.full_name}</div>
                <div class="student-result-group">${student.group || 'Группа не указана'}</div>
            `;
            div.addEventListener('click', () => {
                selectStudent(student.id, student.full_name);
            });
            studentResults.appendChild(div);
        });
        studentResults.classList.add('active');
    }

    function selectStudent(id, fullName) {
        selectedStudentId = id;
        selectedStudentInput.value = id;
        studentSearch.value = fullName;
        studentResults.classList.remove('active');
        studentResults.innerHTML = '';
        checkFormValidity();
    }

    function checkFormValidity() {
        const subject = document.getElementById('id_subject').value;
        const comment = commentTextarea.value.trim();
        
        if (selectedStudentId && subject && comment) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    if (studentSearch) {
        studentSearch.addEventListener('input', function() {
            if (searchTimeout) clearTimeout(searchTimeout);
            searchTimeout = setTimeout(searchStudents, 300);
        });
    }

    document.addEventListener('click', function(e) {
        if (studentSearch && !studentSearch.contains(e.target) && studentResults && !studentResults.contains(e.target)) {
            studentResults.classList.remove('active');
        }
    });

    const subjectSelect = document.getElementById('id_subject');
    if (subjectSelect) {
        subjectSelect.addEventListener('change', checkFormValidity);
    }

    if (commentTextarea) {
        commentTextarea.addEventListener('input', function() {
            checkFormValidity();
            updateCharCount();
        });
        updateCharCount();
    }

    const form = document.getElementById('reviewForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!selectedStudentId) {
                e.preventDefault();
                alert('Пожалуйста, выберите студента из списка');
                return;
            }
        });
    }
});