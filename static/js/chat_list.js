let pollingInterval = null;
let currentUserId = null;
let currentChatId = null;
let emojiPickerWrapper = null;
let selectedFile = null;
let typingTimeout = null;
let isTyping = false;

document.addEventListener('DOMContentLoaded', function() {
    initMenuToggle();
    initChatSelection();
    initSearch();
    initMessageSending();
    initDeleteChat();
    initDragAndDrop();
    initEmojiPicker();
    initChatMenu();
    initProfileSidebar();
    initMoreSubmenu();
    initMenuButtons();
    initMessageContextMenu();
    startPolling(1000);
    scrollToBottom();
    initTypingIndicator();
});

function initMenuToggle() {
    const menuIcon = document.getElementById('menuIcon');
    const sidebarMenu = document.getElementById('sidebarMenu');
    if (menuIcon && sidebarMenu) {
        menuIcon.addEventListener('click', function(e) {
            e.stopPropagation();
            sidebarMenu.classList.toggle('show');
        });
        document.addEventListener('click', function(e) {
            if (!sidebarMenu.contains(e.target) && !menuIcon.contains(e.target)) {
                sidebarMenu.classList.remove('show');
            }
        });
    }
}

function initMenuButtons() {
    const addAccountBtn = document.getElementById('addAccountBtn');
    const savedMessagesBtn = document.getElementById('savedMessagesBtn');
    const archivedChatsBtn = document.getElementById('archivedChatsBtn');
    const myStoriesBtn = document.getElementById('myStoriesBtn');
    const contactsBtn = document.getElementById('contactsBtn');
    const walletBtn = document.getElementById('walletBtn');
    const settingsBtn = document.getElementById('settingsBtn');

    if (addAccountBtn) {
        addAccountBtn.addEventListener('click', () => {
            window.location.href = '/profile/settings/';
        });
    }
    if (savedMessagesBtn) {
        savedMessagesBtn.addEventListener('click', () => {
            window.location.href = '/saved-messages/';
        });
    }
    if (archivedChatsBtn) {
        archivedChatsBtn.addEventListener('click', () => {
            window.location.href = '/archived-chats/';
        });
    }
    if (myStoriesBtn) {
        myStoriesBtn.addEventListener('click', () => {
            window.location.href = '/my-stories/';
        });
    }
    if (contactsBtn) {
        contactsBtn.addEventListener('click', () => {
            window.location.href = '/contacts/';
        });
    }
    if (walletBtn) {
        walletBtn.addEventListener('click', () => {
            window.location.href = '/wallet/';
        });
    }
    if (settingsBtn) {
        settingsBtn.addEventListener('click', () => {
            window.location.href = '/settings/';
        });
    }
}

function initChatSelection() {
    document.querySelectorAll('.chat-item').forEach(item => {
        item.addEventListener('click', function() {
            const chatId = this.dataset.chatId;
            window.location.href = `/chats/${chatId}/`;
        });
    });
}

function initSearch() {
    const searchInput = document.getElementById('searchChats');
    if (!searchInput) return;
    searchInput.addEventListener('input', debounce(function() {
        const term = this.value.toLowerCase();
        document.querySelectorAll('.chat-item').forEach(item => {
            const name = item.querySelector('.chat-name').innerText.toLowerCase();
            const lastMsg = item.querySelector('.chat-last-msg').innerText.toLowerCase();
            item.style.display = (name.includes(term) || lastMsg.includes(term)) ? 'flex' : 'none';
        });
    }, 300));
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showFilePreview() {
    const inputField = document.querySelector('.input-field');
    if (!inputField) return;
    
    const existingPreview = document.querySelector('.file-preview');
    if (existingPreview) existingPreview.remove();
    
    if (selectedFile) {
        const preview = document.createElement('div');
        preview.className = 'file-preview';
        preview.innerHTML = `
            <span>📎 ${selectedFile.name}</span>
            <button type="button" class="remove-file-btn">✖</button>
        `;
        preview.querySelector('.remove-file-btn').onclick = function() {
            selectedFile = null;
            document.getElementById('fileInput').value = '';
            preview.remove();
        };
        inputField.appendChild(preview);
    }
}

function initMessageSending() {
    const sendBtn = document.getElementById('sendMsgBtn');
    const msgInput = document.getElementById('messageInput');
    const attachBtn = document.getElementById('attachFileBtn');
    const fileInput = document.getElementById('fileInput');

    if (!sendBtn || !msgInput) return;

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                selectedFile = this.files[0];
                showFilePreview();
            }
        });
    }

    async function sendMessage() {
        const text = msgInput.value.trim();
        const file = selectedFile;
        if (!text && !file) return;

        const formData = new FormData();
        formData.append('text', text);
        if (file) formData.append('file', file);

        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: formData
        });
        const data = await response.json();
        if (data.success) {
            msgInput.value = '';
            msgInput.style.height = 'auto';
            if (fileInput) fileInput.value = '';
            selectedFile = null;
            const preview = document.querySelector('.file-preview');
            if (preview) preview.remove();
            stopTyping();
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    
    msgInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    msgInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
        handleTyping();
    });

    if (attachBtn && fileInput) {
        attachBtn.addEventListener('click', () => fileInput.click());
    }

    bindEditDeleteEvents();
}

function handleTyping() {
    const msgInput = document.getElementById('messageInput');
    if (!msgInput) return;
    
    if (!isTyping && msgInput.value.trim()) {
        isTyping = true;
        sendTypingStatus(true);
    }
    
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        if (isTyping) {
            isTyping = false;
            sendTypingStatus(false);
        }
    }, 1000);
}

function stopTyping() {
    if (isTyping) {
        isTyping = false;
        sendTypingStatus(false);
    }
    clearTimeout(typingTimeout);
}

function sendTypingStatus(typing) {
    const chatId = document.getElementById('chatMessages')?.dataset.chatId;
    if (!chatId) return;
    
    fetch('/typing-status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            chat_id: chatId,
            is_typing: typing
        })
    }).catch(e => console.warn('Typing error:', e));
}

function initTypingIndicator() {
    const wsScheme = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsScheme}//${window.location.host}/ws/typing/`;
    const ws = new WebSocket(wsUrl);
    
    ws.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const typingIndicator = document.getElementById('typingIndicator');
        const currentChatId = document.getElementById('chatMessages')?.dataset.chatId;
        
        if (data.chat_id == currentChatId && data.user_id != currentUserId) {
            if (data.is_typing) {
                typingIndicator.style.display = 'flex';
            } else {
                typingIndicator.style.display = 'none';
            }
        }
    };
}

async function handleEditClick(btn) {
    const msgId = btn.dataset.id;
    const msgDiv = btn.closest('.message');
    const oldText = msgDiv.querySelector('.message-text').innerText;
    const newText = prompt('Редактировать сообщение:', oldText);
    if (newText && newText !== oldText) {
        const formData = new FormData();
        formData.append('edit_id', msgId);
        formData.append('text', newText);
        const response = await fetch(window.location.href, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: formData
        });
        const data = await response.json();
        if (data.success) {
            msgDiv.querySelector('.message-text').innerHTML = escapeHtml(newText);
        }
    }
}

async function handleDeleteClick(btn) {
    if (!confirm('Удалить сообщение?')) return;
    const msgId = btn.dataset.id;
    const msgDiv = btn.closest('.message');
    const formData = new FormData();
    formData.append('delete_id', msgId);
    const response = await fetch(window.location.href, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData
    });
    const data = await response.json();
    if (data.success) {
        msgDiv.remove();
    }
}

function bindEditDeleteEvents() {
    document.querySelectorAll('.edit-msg').forEach(btn => {
        if (btn.dataset.bound === 'true') return;
        btn.dataset.bound = 'true';
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            handleEditClick(this);
        });
    });

    document.querySelectorAll('.delete-msg').forEach(btn => {
        if (btn.dataset.bound === 'true') return;
        btn.dataset.bound = 'true';
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            handleDeleteClick(this);
        });
    });
}

function initMessageContextMenu() {
    document.addEventListener('contextmenu', function(e) {
        const messageDiv = e.target.closest('.message');
        if (!messageDiv) return;
        
        e.preventDefault();
        
        const existingMenu = document.querySelector('.message-context-menu');
        if (existingMenu) existingMenu.remove();
        
        const menu = document.createElement('div');
        menu.className = 'message-context-menu';
        const isSent = messageDiv.classList.contains('sent');
        
        let menuHtml = `
            <div class="context-item" data-action="copy">Копировать текст</div>
            <div class="context-item" data-action="reply">Ответить</div>
            <div class="context-item" data-action="forward">Переслать</div>
        `;
        
        if (isSent) {
            menuHtml += `
                <hr>
                <div class="context-item" data-action="edit">Редактировать</div>
                <div class="context-item delete" data-action="delete">Удалить</div>
            `;
        }
        
        menu.innerHTML = menuHtml;
        menu.style.left = `${e.pageX}px`;
        menu.style.top = `${e.pageY}px`;
        document.body.appendChild(menu);
        
        menu.addEventListener('click', function(event) {
            const action = event.target.dataset.action;
            const msgId = messageDiv.dataset.id;
            const msgText = messageDiv.querySelector('.message-text').innerText;
            
            switch(action) {
                case 'copy':
                    navigator.clipboard.writeText(msgText);
                    break;
                case 'reply':
                    const msgInput = document.getElementById('messageInput');
                    if (msgInput) {
                        msgInput.value = `> ${msgText}\n\n`;
                        msgInput.focus();
                    }
                    break;
                case 'forward':
                    alert('Функция пересылки в разработке');
                    break;
                case 'edit':
                    const editBtn = messageDiv.querySelector('.edit-msg');
                    if (editBtn) handleEditClick(editBtn);
                    break;
                case 'delete':
                    const deleteBtn = messageDiv.querySelector('.delete-msg');
                    if (deleteBtn) handleDeleteClick(deleteBtn);
                    break;
            }
            menu.remove();
        });
        
        const closeMenu = (e) => {
            if (!menu.contains(e.target)) {
                menu.remove();
                document.removeEventListener('click', closeMenu);
            }
        };
        setTimeout(() => document.addEventListener('click', closeMenu), 100);
    });
}

function initDeleteChat() {
    const deleteForMe = document.getElementById('deleteForMeBtn');
    const deleteForBoth = document.getElementById('deleteForBothBtn');
    if (!deleteForMe && !deleteForBoth) return;

    const chatId = document.getElementById('chatMessages')?.dataset.chatId;
    if (!chatId) return;

    if (deleteForMe) {
        deleteForMe.addEventListener('click', async () => {
            if (!confirm('Удалить чат только для себя?')) return;
            await fetch(`/api/chat/delete-for-me/${chatId}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            });
            window.location.href = '/chats/';
        });
    }

    if (deleteForBoth) {
        deleteForBoth.addEventListener('click', async () => {
            if (!confirm('Удалить чат для обоих участников? Это действие необратимо.')) return;
            await fetch(`/api/chat/delete-for-both/${chatId}/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            });
            window.location.href = '/chats/';
        });
    }
}

function initDragAndDrop() {
    const container = document.getElementById('chatsList');
    if (!container) return;
    new Sortable(container, {
        animation: 150,
        handle: '.chat-item',
        onEnd: async function() {
            const order = [];
            document.querySelectorAll('.chat-item').forEach((item) => {
                order.push(item.getAttribute('data-chat-id'));
            });
            await fetch('/api/chat/order/', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
                body: JSON.stringify({ order: order })
            });
        }
    });
}

function initEmojiPicker() {
    const emojiBtn = document.getElementById('emojiBtn');
    const messageInput = document.getElementById('messageInput');
    const inputField = document.querySelector('.input-field');
    if (!emojiBtn || !messageInput || !inputField) return;

    emojiBtn.addEventListener('click', async (e) => {
        e.stopPropagation();

        if (emojiPickerWrapper && emojiPickerWrapper.isConnected) {
            emojiPickerWrapper.remove();
            emojiPickerWrapper = null;
            return;
        }

        const module = await import('https://cdn.jsdelivr.net/npm/emoji-picker-element@1.21.0/index.js');
        const Picker = module.Picker;
        const picker = new Picker();

        emojiPickerWrapper = document.createElement('div');
        emojiPickerWrapper.className = 'emoji-picker-wrapper';
        emojiPickerWrapper.style.position = 'absolute';
        emojiPickerWrapper.style.bottom = '100%';
        emojiPickerWrapper.style.left = '0';
        emojiPickerWrapper.style.marginBottom = '10px';
        emojiPickerWrapper.style.zIndex = '1000';
        emojiPickerWrapper.appendChild(picker);

        inputField.style.position = 'relative';
        inputField.appendChild(emojiPickerWrapper);

        picker.addEventListener('emoji-click', event => {
            messageInput.value += event.detail.unicode;
            messageInput.focus();
            messageInput.dispatchEvent(new Event('input'));
        });

        const closePicker = (event) => {
            if (emojiPickerWrapper && !emojiPickerWrapper.contains(event.target) && event.target !== emojiBtn) {
                emojiPickerWrapper.remove();
                emojiPickerWrapper = null;
                document.removeEventListener('click', closePicker);
            }
        };
        setTimeout(() => document.addEventListener('click', closePicker), 100);
    });
}

function initChatMenu() {
    const menuBtn = document.getElementById('chatMenuBtn');
    const dropdown = document.getElementById('chatMenuDropdown');
    if (!menuBtn || !dropdown) return;

    menuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isVisible = dropdown.style.display === 'block';
        dropdown.style.display = isVisible ? 'none' : 'block';
    });

    document.addEventListener('click', (e) => {
        if (!menuBtn.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}

function initProfileSidebar() {
    const chatUserInfo = document.getElementById('chatUserInfo');
    const sidebar = document.getElementById('profileSidebar');
    const closeBtn = document.getElementById('closeSidebarBtn');
    const profileContent = document.getElementById('profileContent');

    if (!chatUserInfo || !sidebar || !closeBtn || !profileContent) return;

    function openProfile(userId) {
        fetch(`/api/user-profile/${userId}/`)
            .then(res => res.json())
            .then(data => {
                let avatarHtml = '';
                if (data.avatar) {
                    avatarHtml = `<div class="profile-avatar"><img src="${data.avatar}" class="profile-avatar-img"></div>`;
                } else {
                    avatarHtml = `<div class="profile-avatar"><div class="avatar-lg" style="width:100px;height:100px;font-size:40px;">${data.full_name.charAt(0).toUpperCase()}</div></div>`;
                }
                let html = avatarHtml;
                html += `<div class="profile-field"><strong>Имя</strong><span>${escapeHtml(data.full_name)}</span></div>`;
                if (data.birth_date) html += `<div class="profile-field"><strong>Дата рождения</strong><span>${data.birth_date}</span></div>`;
                if (data.gender) html += `<div class="profile-field"><strong>Пол</strong><span>${data.gender}</span></div>`;
                if (data.phone) html += `<div class="profile-field"><strong>Телефон</strong><span>${data.phone}</span></div>`;
                if (data.city) html += `<div class="profile-field"><strong>Город</strong><span>${escapeHtml(data.city)}</span></div>`;
                if (data.interests) html += `<div class="profile-field"><strong>Интересы</strong><span>${escapeHtml(data.interests)}</span></div>`;
                if (data.about) html += `<div class="profile-field"><strong>О себе</strong><span>${escapeHtml(data.about)}</span></div>`;
                if (data.student_info) {
                    if (data.student_info.group) html += `<div class="profile-field"><strong>Группа</strong><span>${data.student_info.group}</span></div>`;
                    if (data.student_info.course) html += `<div class="profile-field"><strong>Курс</strong><span>${data.student_info.course}</span></div>`;
                    if (data.student_info.direction) html += `<div class="profile-field"><strong>Направление</strong><span>${escapeHtml(data.student_info.direction)}</span></div>`;
                }
                if (data.is_self) {
                    html += `<div class="profile-edit-link"><a href="/profile/settings/">Редактировать профиль</a></div>`;
                }
                profileContent.innerHTML = html;
                sidebar.classList.add('open');
            });
    }

    chatUserInfo.addEventListener('click', () => {
        const chatId = document.getElementById('chatMessages')?.dataset.chatId;
        if (chatId) {
            fetch(`/api/chat/participant/${chatId}/`)
                .then(res => res.json())
                .then(data => {
                    if (data.user_id) openProfile(data.user_id);
                });
        }
    });

    closeBtn.addEventListener('click', () => sidebar.classList.remove('open'));
    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !chatUserInfo.contains(e.target) && sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
        }
    });
}

function initMoreSubmenu() {
    const darkModeBtn = document.getElementById('darkModeBtn');
    const disableAnimationsBtn = document.getElementById('disableAnimationsBtn');
    const switchVersionBtn = document.getElementById('switchVersionBtn');
    const telegramFeaturesBtn = document.getElementById('telegramFeaturesBtn');
    const reportBugBtn = document.getElementById('reportBugBtn');
    const installAppBtn = document.getElementById('installAppBtn');

    if (darkModeBtn) {
        darkModeBtn.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }

    if (disableAnimationsBtn) {
        disableAnimationsBtn.addEventListener('click', () => {
            document.body.classList.toggle('no-animations');
            localStorage.setItem('noAnimations', document.body.classList.contains('no-animations'));
        });
        if (localStorage.getItem('noAnimations') === 'true') {
            document.body.classList.add('no-animations');
        }
    }

    if (switchVersionBtn) {
        switchVersionBtn.addEventListener('click', () => {
            alert('Переключение на другую версию (демо)');
        });
    }

    if (telegramFeaturesBtn) {
        telegramFeaturesBtn.addEventListener('click', () => {
            alert('Открыть страницу с функциями Telegram');
        });
    }

    if (reportBugBtn) {
        reportBugBtn.addEventListener('click', () => {
            window.location.href = '/complaint/';
        });
    }

    if (installAppBtn) {
        installAppBtn.addEventListener('click', () => {
            alert('Установка приложения (PWA)');
        });
    }
}

function startPolling(intervalMs) {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;
    currentChatId = messagesContainer.dataset.chatId;
    currentUserId = messagesContainer.dataset.userId;
    if (!currentChatId) return;
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = setInterval(checkNewMessages, intervalMs);
}

async function checkNewMessages() {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;
    const lastMsg = messagesContainer.querySelector('.message:last-child');
    const lastId = lastMsg ? lastMsg.dataset.id : '0';
    try {
        const response = await fetch(`/api/chat/messages/${currentChatId}/?last_id=${lastId}`);
        const data = await response.json();
        if (data.messages && data.messages.length) {
            updateMessages(data.messages);
        }
    } catch(e) { console.warn('Polling error', e); }
}

function updateMessages(messages) {
    const container = document.getElementById('chatMessages');
    const lastMessageBeforeUpdate = container.querySelector('.message:last-child');
    
    messages.forEach(msg => {
        const existingMsg = container.querySelector(`.message[data-id="${msg.id}"]`);
        const isSent = msg.sender_id == currentUserId;
        
        if (existingMsg) {
            existingMsg.querySelector('.message-text').innerHTML = escapeHtml(msg.text);
            const fileDiv = existingMsg.querySelector('.message-file');
            if (msg.file && msg.filename) {
                if (fileDiv) {
                    fileDiv.innerHTML = `<a href="${msg.file}" target="_blank">📎 ${escapeHtml(msg.filename)}</a>`;
                } else {
                    const newFileDiv = document.createElement('div');
                    newFileDiv.className = 'message-file';
                    newFileDiv.innerHTML = `<a href="${msg.file}" target="_blank">📎 ${escapeHtml(msg.filename)}</a>`;
                    existingMsg.querySelector('.message-bubble').appendChild(newFileDiv);
                }
            } else if (fileDiv) {
                fileDiv.remove();
            }
            
            const timeDiv = existingMsg.querySelector('.message-time');
            if (timeDiv && isSent) {
                const existingStatus = timeDiv.querySelector('.message-status');
                if (msg.is_read) {
                    if (existingStatus) {
                        existingStatus.className = 'fa-solid fa-check-double message-status read';
                    } else {
                        timeDiv.innerHTML = `${msg.time} <i class="fa-solid fa-check-double message-status read"></i>`;
                    }
                } else if (msg.is_delivered) {
                    if (existingStatus) {
                        existingStatus.className = 'fa-solid fa-check-double message-status delivered';
                    } else {
                        timeDiv.innerHTML = `${msg.time} <i class="fa-solid fa-check-double message-status delivered"></i>`;
                    }
                } else {
                    if (existingStatus) {
                        existingStatus.className = 'fa-solid fa-check message-status sent';
                    } else {
                        timeDiv.innerHTML = `${msg.time} <i class="fa-solid fa-check message-status sent"></i>`;
                    }
                }
            }
        } else {
            const div = document.createElement('div');
            div.className = `message ${isSent ? 'sent' : 'received'}`;
            div.setAttribute('data-id', msg.id);
            div.innerHTML = `
                <div class="message-bubble">
                    <div class="message-text">${escapeHtml(msg.text)}</div>
                    ${msg.file && msg.filename ? `<div class="message-file"><a href="${msg.file}" target="_blank">📎 ${escapeHtml(msg.filename)}</a></div>` : ''}
                    <div class="message-time">
                        ${msg.time}
                        ${isSent ? `
                            ${msg.is_read ? '<i class="fa-solid fa-check-double message-status read"></i>' : (msg.is_delivered ? '<i class="fa-solid fa-check-double message-status delivered"></i>' : '<i class="fa-solid fa-check message-status sent"></i>')}
                        ` : ''}
                    </div>
                    ${isSent ? `
                    <div class="message-actions">
                        <button class="edit-msg" data-id="${msg.id}">✏️</button>
                        <button class="delete-msg" data-id="${msg.id}">🗑️</button>
                    </div>` : ''}
                </div>
            `;
            container.appendChild(div);
        }
    });
    
    bindEditDeleteEvents();
    
    const lastMessageAfterUpdate = container.querySelector('.message:last-child');
    if (lastMessageBeforeUpdate !== lastMessageAfterUpdate) {
        scrollToBottom();
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

function scrollToBottom() {
    const container = document.getElementById('chatMessages');
    if (container) {
        container.scrollTo({
            top: container.scrollHeight,
            behavior: 'smooth'
        });
    }
}

function getCookie(name) {
    let value = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            const [key, val] = cookie.trim().split('=');
            if (key === name) value = decodeURIComponent(val);
        });
    }
    return value;
}