document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('estimationForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const student = document.getElementById('id_student');
            const subject = document.getElementById('id_subject');
            const grade = document.getElementById('id_type_estimation');
            
            let hasError = false;
            let errorMessage = '';
            
            if (!student.value) {
                hasError = true;
                errorMessage = 'Выберите студента';
                student.style.borderColor = '#dc3545';
            }
            
            if (!subject.value) {
                hasError = true;
                errorMessage = 'Выберите предмет';
                subject.style.borderColor = '#dc3545';
            }
            
            if (!grade.value) {
                hasError = true;
                errorMessage = 'Выберите оценку';
                grade.style.borderColor = '#dc3545';
            }
            
            if (hasError) {
                e.preventDefault();
                alert(errorMessage);
            }
        });
        
        const inputs = document.querySelectorAll('#estimationForm select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                this.style.borderColor = '#ddd';
            });
        });
    }
});