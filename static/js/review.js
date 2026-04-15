document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reviewForm');
    const platformSelect = document.getElementById('id_type_a_social_network');
    const fileInput = document.getElementById('id_confirmation_review');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const removeImageBtn = document.querySelector('.btn-remove-image');

    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            const maxSize = 5 * 1024 * 1024;
            
            if (file.size > maxSize) {
                alert('Файл слишком большой. Максимальный размер 5MB');
                this.value = '';
                return;
            }
            
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                imagePreview.style.display = 'inline-block';
            };
            reader.readAsDataURL(this.files[0]);
        }
    });

    removeImageBtn.addEventListener('click', function() {
        fileInput.value = '';
        imagePreview.style.display = 'none';
        previewImg.src = '#';
    });

    form.addEventListener('submit', function(e) {
        if (!platformSelect.value) {
            e.preventDefault();
            alert('Выберите платформу, где оставлен отзыв');
            platformSelect.focus();
            return;
        }
        
        if (!fileInput.files.length) {
            e.preventDefault();
            alert('Загрузите скриншот отзыва');
            return;
        }
    });
});