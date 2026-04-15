document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const userItems = document.querySelectorAll('.user-item');
    const usersList = document.getElementById('usersList');
    const selectedInfo = document.getElementById('selectedInfo');
    const selectedName = document.getElementById('selectedName');
    const targetUserId = document.getElementById('targetUserId');
    const submitBtn = document.getElementById('submitBtn');
    const clearSelected = document.getElementById('clearSelected');

    let selectedId = null;

    function filterUsers() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        let hasVisible = false;
        
        userItems.forEach(item => {
            const name = item.getAttribute('data-name').toLowerCase();
            const username = item.getAttribute('data-username').toLowerCase();
            const email = item.getAttribute('data-email').toLowerCase();
            
            if (name.includes(searchTerm) || username.includes(searchTerm) || email.includes(searchTerm)) {
                item.style.display = 'block';
                hasVisible = true;
            } else {
                item.style.display = 'none';
            }
        });
        
        const existingNoResults = document.querySelector('.no-results');
        if (!hasVisible) {
            if (!existingNoResults) {
                const div = document.createElement('div');
                div.className = 'no-results';
                div.innerHTML = '👤 Пользователи не найдены<br><small>Попробуйте другой запрос</small>';
                usersList.appendChild(div);
            }
        } else if (existingNoResults) {
            existingNoResults.remove();
        }
    }

    userItems.forEach(item => {
        item.addEventListener('click', function() {
            userItems.forEach(i => i.classList.remove('selected'));
            this.classList.add('selected');
            selectedId = this.getAttribute('data-id');
            selectedName.textContent = this.getAttribute('data-name');
            targetUserId.value = selectedId;
            selectedInfo.style.display = 'flex';
            submitBtn.disabled = false;
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', filterUsers);
    }

    if (clearSelected) {
        clearSelected.addEventListener('click', function() {
            selectedId = null;
            targetUserId.value = '';
            selectedInfo.style.display = 'none';
            submitBtn.disabled = true;
            userItems.forEach(i => i.classList.remove('selected'));
        });
    }

    const form = document.getElementById('createChatForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!targetUserId.value) {
                e.preventDefault();
                alert('Пожалуйста, выберите собеседника');
            }
        });
    }
});