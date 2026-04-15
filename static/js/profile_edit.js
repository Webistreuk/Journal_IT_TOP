document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('profileForm');
    const nameInput = document.getElementById('id_name');
    const surnameInput = document.getElementById('id_surname');

    form.addEventListener('submit', function(e) {
        if (!nameInput.value.trim()) {
            e.preventDefault();
            alert('Введите имя');
            nameInput.focus();
            return;
        }
        
        if (!surnameInput.value.trim()) {
            e.preventDefault();
            alert('Введите фамилию');
            surnameInput.focus();
            return;
        }
    });
});