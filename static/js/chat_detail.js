let currentEditId = null;
let currentFile = null;

function scrollToBottom() {
    const messages = document.getElementById('chatMessages');
    if (messages) messages.scrollTop = messages.scrollHeight;
}

scrollToBottom();

const emojiBtn = document.getElementById('emojiBtn');
if (emojiBtn) {
    emojiBtn.addEventListener('click', function() {
        const picker = document.getElementById('emojiPicker');
        if (picker.style.display === 'none') {
            picker.style.display = 'block';
            $('#emojiPicker').emojioneArea({
                pickerPosition: 'top',
                events: {
                    emojibtn_click: function(btn, event) {
                        const emoji = btn.children()[0].alt;
                        const input = document.getElementById('messageText');
                        input.value += emoji;
                        picker.style.display = 'none';
                    }
                }
            });
        } else {
            picker.style.display = 'none';
        }
    });
}

const attachBtn = document.getElementById('attachBtn');
if (attachBtn) {
    attachBtn.addEventListener('click', function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.onchange = function(e) {
            if (e.target.files && e.target.files[0]) {
                currentFile = e.target.files[0];
                const fileNameSpan = document.getElementById('fileName');
                const filePreviewDiv = document.getElementById('filePreview');
                if (fileNameSpan) fileNameSpan.textContent = currentFile.name;
                if (filePreviewDiv) filePreviewDiv.style.display = 'flex';
            }
        };
        input.click();
    });
}

const removeFileBtn = document.getElementById('removeFileBtn');
if (removeFileBtn) {
    removeFileBtn.addEventListener('click', function() {
        currentFile = null;
        const filePreviewDiv = document.getElementById('filePreview');
        if (filePreviewDiv) filePreviewDiv.style.display = 'none';
    });
}

function sendMessage() {
    const textarea = document.getElementById('messageText');
    const text = textarea ? textarea.value.trim() : '';
    
    if (!text && !currentFile) return;

    const formData = new FormData();
    if (currentEditId) formData.append('edit_id', currentEditId);
    if (text) formData.append('text', text);
    if (currentFile) formData.append('file', currentFile);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken ? csrfToken.value : ''
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (textarea) textarea.value = '';
            currentFile = null;
            currentEditId = null;
            const filePreviewDiv = document.getElementById('filePreview');
            if (filePreviewDiv) filePreviewDiv.style.display = 'none';
            location.reload();
        }
    });
}

const sendBtn = document.getElementById('sendBtn');
if (sendBtn) sendBtn.addEventListener('click', sendMessage);

const messageText = document.getElementById('messageText');
if (messageText) {
    messageText.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

function editMessage(msgId) {
    const messageDiv = document.querySelector(`.message[data-id="${msgId}"]`);
    if (!messageDiv) return;
    
    const oldText = messageDiv.getAttribute('data-text') || '';
    const newText = prompt('Редактировать сообщение:', oldText);
    if (newText && newText !== oldText) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken ? csrfToken.value : '',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `edit_id=${msgId}&text=${encodeURIComponent(newText)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) location.reload();
        });
    }
}

function deleteMessage(msgId) {
    if (confirm('Удалить сообщение?')) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken ? csrfToken.value : '',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `delete_id=${msgId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) location.reload();
        });
    }
}