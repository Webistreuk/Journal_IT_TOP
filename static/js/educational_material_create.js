document.addEventListener('DOMContentLoaded', function() {
    const isPublicCheckbox = document.getElementById('id_is_public');
    const groupsContainer = document.getElementById('groupsContainer');
    const fileInput = document.getElementById('id_file');
    const fileInfo = document.getElementById('fileInfo');
    const fileNameSpan = document.getElementById('fileName');
    const fileSizeSpan = document.getElementById('fileSize');
    const removeFileBtn = document.querySelector('.btn-remove-file');
    const form = document.getElementById('materialForm');
    const titleInput = document.getElementById('id_title');

    isPublicCheckbox.addEventListener('change', function() {
        if (this.checked) {
            groupsContainer.style.display = 'none';
            const groupInputs = document.querySelectorAll('.group-input');
            groupInputs.forEach(input => input.checked = false);
        } else {
            groupsContainer.style.display = 'block';
        }
    });

    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            const maxSize = 50 * 1024 * 1024;
            
            if (file.size > maxSize) {
                alert('Файл слишком большой. Максимальный размер 50MB');
                this.value = '';
                fileInfo.style.display = 'none';
                return;
            }
            
            fileNameSpan.textContent = file.name;
            fileSizeSpan.textContent = (file.size / 1024 / 1024).toFixed(2) + ' MB';
            fileInfo.style.display = 'flex';
        }
    });

    removeFileBtn.addEventListener('click', function() {
        fileInput.value = '';
        fileInfo.style.display = 'none';
    });

    form.addEventListener('submit', function(e) {
        if (!titleInput.value.trim()) {
            e.preventDefault();
            alert('Введите название материала');
            titleInput.focus();
            return;
        }
        
        if (!fileInput.files.length) {
            e.preventDefault();
            alert('Выберите файл для загрузки');
            return;
        }
        
        if (!isPublicCheckbox.checked) {
            const checkedGroups = document.querySelectorAll('.group-input:checked');
            if (checkedGroups.length === 0) {
                e.preventDefault();
                alert('Выберите хотя бы одну группу или отметьте "Для всех групп"');
                return;
            }
        }
    });
});