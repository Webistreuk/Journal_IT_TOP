document.addEventListener('DOMContentLoaded', function() {
    const isForAllCheckbox = document.getElementById('id_is_for_all');
    const groupsContainer = document.getElementById('groupsContainer');
    const photoInput = document.getElementById('id_photo');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const removeImageBtn = document.querySelector('.btn-remove-image');
    const form = document.getElementById('announcementForm');
    const titleInput = document.getElementById('id_title');
    const descriptionTextarea = document.getElementById('id_description');

    isForAllCheckbox.addEventListener('change', function() {
        if (this.checked) {
            groupsContainer.style.display = 'none';
            const groupInputs = document.querySelectorAll('.group-input');
            groupInputs.forEach(input => input.checked = false);
        } else {
            groupsContainer.style.display = 'block';
        }
    });

    photoInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                imagePreview.style.display = 'inline-block';
            };
            reader.readAsDataURL(this.files[0]);
        }
    });

    removeImageBtn.addEventListener('click', function() {
        photoInput.value = '';
        imagePreview.style.display = 'none';
        previewImg.src = '#';
    });

    form.addEventListener('submit', function(e) {
        if (!titleInput.value.trim()) {
            e.preventDefault();
            alert('Введите заголовок объявления');
            titleInput.focus();
            return;
        }
        
        if (!descriptionTextarea.value.trim()) {
            e.preventDefault();
            alert('Введите текст объявления');
            descriptionTextarea.focus();
            return;
        }
        
        if (!isForAllCheckbox.checked) {
            const checkedGroups = document.querySelectorAll('.group-input:checked');
            if (checkedGroups.length === 0) {
                e.preventDefault();
                alert('Выберите хотя бы одну группу или отметьте "Для всех"');
                return;
            }
        }
    });
});