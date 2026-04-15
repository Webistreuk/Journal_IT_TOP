let currentEditId = null;
let currentFile = null;

function scrollToBottom() {
    const messages = document.getElementById('chatMessages');
    messages.scrollTop = messages.scrollHeight;
}

scrollToBottom();

document.getElementById('emojiBtn').addEventListener('click', function() {
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

document.getElementById('attachBtn').addEventListener('click', function() {
    const input = document.createElement('input');
    input.type = 'file';
    input.onchange = function(e) {
        currentFile = e.target.files[0];
        document.getElementById('fileName').textContent = currentFile.name;
        document.getElementById('filePreview').style.display = 'flex';
    };
    input.click();
});

document.getElementById('removeFileBtn').addEventListener('click', function() {
    currentFile = null;
    document.getElementById('filePreview').style.display = 'none';
});

function sendMessage() {
    const text = document.getElementById('messageText').value.trim();
    if (!text && !currentFile) return;

    const formData = new FormData();
    if (currentEditId) {
        formData.append('edit_id', currentEditId);
    }
    formData.append('text', text);
    if (currentFile) {
        formData.append('file', currentFile);
    }

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('messageText').value = '';
            currentFile = null;
            currentEditId = null;
            document.getElementById('filePreview').style.display = 'none';
            location.reload();
        }
    });
}

document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('messageText').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function editMessage(msgId) {
    const messageDiv = document.querySelector(`.message[data-id="${msgId}"]`);
    const oldText = messageDiv.getAttribute('data-text');
    const newText = prompt('Редактировать сообщение:', oldText);
    if (newText && newText !== oldText) {
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
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
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
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