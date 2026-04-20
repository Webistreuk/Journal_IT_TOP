let pollingInterval = null;
let currentUserId = null;
let currentChatId = null;
let emojiPickerWrapper = null;
let selectedFile = null;
let typingTimeout = null;
let isTyping = false;
let replyToId = null;
let replyToText = null;
let currentForwardMessageId = null;

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
    initContextMenu();
    startPolling(1000);
    scrollToBottom();
    initTypingIndicator();
    startUnreadPolling();
    initForwardBadgeClick();
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

    if (addAccountBtn) addAccountBtn.addEventListener('click', () => window.location.href = '/profile/settings/');
    if (savedMessagesBtn) savedMessagesBtn.addEventListener('click', () => window.location.href = '/saved-messages/');
    if (archivedChatsBtn) archivedChatsBtn.addEventListener('click', () => window.location.href = '/archived-chats/');
    if (myStoriesBtn) myStoriesBtn.addEventListener('click', () => window.location.href = '/my-stories/');
    if (contactsBtn) contactsBtn.addEventListener('click', () => window.location.href = '/contacts/');
    if (walletBtn) walletBtn.addEventListener('click', () => window.location.href = '/wallet/');
    if (settingsBtn) settingsBtn.addEventListener('click', () => window.location.href = '/settings/');
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
        preview.innerHTML = `<span>📎 ${selectedFile.name}</span><button type="button" class="remove-file-btn">✖</button>`;
        preview.querySelector('.remove-file-btn').onclick = function() {
            selectedFile = null;
            document.getElementById('fileInput').value = '';
            preview.remove();
        };
        inputField.appendChild(preview);
    }
}

function showReplyPreview() {
    const bar = document.getElementById('replyPreviewBar');
    if (replyToId && replyToText) {
        bar.style.display = 'block';
        bar.querySelector('.reply-preview-text').innerHTML = `Ответ на: ${escapeHtml(replyToText.substring(0, 80))}`;
    } else {
        bar.style.display = 'none';
    }
}

document.getElementById('cancelReplyBtn')?.addEventListener('click', () => {
    replyToId = null;
    replyToText = null;
    showReplyPreview();
});

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
        if (text) formData.append('text', text);
        if (file) formData.append('file', file);
        if (replyToId) formData.append('reply_to', replyToId);

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
            replyToId = null;
            replyToText = null;
            showReplyPreview();
            const preview = document.querySelector('.file-preview');
            if (preview) preview.remove();
            stopTyping();
            loadMessages();
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
    if (attachBtn && fileInput) attachBtn.addEventListener('click', () => fileInput.click());
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
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify({ chat_id: chatId, is_typing: typing })
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
            typingIndicator.style.display = data.is_typing ? 'flex' : 'none';
        }
    };
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
            await fetch(`/api/chat/delete-for-me/${chatId}/`, { method: 'POST', headers: { 'X-CSRFToken': getCookie('csrftoken') } });
            window.location.href = '/chats/';
        });
    }
    if (deleteForBoth) {
        deleteForBoth.addEventListener('click', async () => {
            if (!confirm('Удалить чат для обоих участников? Это действие необратимо.')) return;
            await fetch(`/api/chat/delete-for-both/${chatId}/`, { method: 'POST', headers: { 'X-CSRFToken': getCookie('csrftoken') } });
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
        dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
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
                if (data.is_self) html += `<div class="profile-edit-link"><a href="/profile/settings/">Редактировать профиль</a></div>`;
                profileContent.innerHTML = html;
                sidebar.classList.add('open');
            });
    }
    chatUserInfo.addEventListener('click', () => {
        const chatId = document.getElementById('chatMessages')?.dataset.chatId;
        if (chatId) {
            fetch(`/api/chat/participant/${chatId}/`)
                .then(res => res.json())
                .then(data => { if (data.user_id) openProfile(data.user_id); });
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
        if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark-mode');
    }
    if (disableAnimationsBtn) {
        disableAnimationsBtn.addEventListener('click', () => {
            document.body.classList.toggle('no-animations');
            localStorage.setItem('noAnimations', document.body.classList.contains('no-animations'));
        });
        if (localStorage.getItem('noAnimations') === 'true') document.body.classList.add('no-animations');
    }
    if (switchVersionBtn) switchVersionBtn.addEventListener('click', () => alert('Переключение на другую версию (демо)'));
    if (telegramFeaturesBtn) telegramFeaturesBtn.addEventListener('click', () => alert('Открыть страницу с функциями Telegram'));
    if (reportBugBtn) reportBugBtn.addEventListener('click', () => window.location.href = '/complaint/');
    if (installAppBtn) installAppBtn.addEventListener('click', () => alert('Установка приложения (PWA)'));
}

function initContextMenu() {
    const contextMenu = document.createElement('div');
    contextMenu.className = 'message-context-menu';
    contextMenu.style.display = 'none';
    document.body.appendChild(contextMenu);

    document.addEventListener('contextmenu', function(e) {
        const msgDiv = e.target.closest('.message');
        if (!msgDiv) return;
        e.preventDefault();
        
        const msgId = msgDiv.dataset.id;
        const msgText = msgDiv.querySelector('.message-text').innerText;
        const isSent = msgDiv.classList.contains('sent');
        
        let menuHtml = '';
        
        if (isSent) {
            menuHtml = `
                <div class="context-item" data-action="edit">Редактировать</div>
                <div class="context-item" data-action="delete">Удалить</div>
                <hr>
                <div class="context-item" data-action="copy">Копировать текст</div>
                <div class="context-item" data-action="reply">Ответить</div>
                <div class="context-item" data-action="forward">Переслать</div>
                <div class="context-item" data-action="react">Отреагировать</div>
            `;
        } else {
            menuHtml = `
                <div class="context-item" data-action="copy">Копировать текст</div>
                <div class="context-item" data-action="reply">Ответить</div>
                <div class="context-item" data-action="forward">Переслать</div>
                <div class="context-item" data-action="react">Отреагировать</div>
            `;
        }
        
        contextMenu.innerHTML = menuHtml;
        contextMenu.style.left = e.pageX + 'px';
        contextMenu.style.top = e.pageY + 'px';
        contextMenu.style.display = 'block';
        contextMenu.dataset.messageId = msgId;
        contextMenu.dataset.messageText = msgText;
        
        const closeMenu = (e) => {
            if (!contextMenu.contains(e.target)) {
                contextMenu.style.display = 'none';
                document.removeEventListener('click', closeMenu);
            }
        };
        setTimeout(() => document.addEventListener('click', closeMenu), 100);
    });
    
    contextMenu.addEventListener('click', async (e) => {
        const action = e.target.closest('.context-item')?.dataset.action;
        const msgId = contextMenu.dataset.messageId;
        let msgText = contextMenu.dataset.messageText;
        
        msgText = msgText.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
        
        if (action === 'copy') {
            await navigator.clipboard.writeText(msgText);
            showToast('Скопировано');
            contextMenu.style.display = 'none';
        }
        else if (action === 'reply') {
            replyToId = msgId;
            replyToText = msgText;
            showReplyPreview();
            document.getElementById('messageInput').focus();
            contextMenu.style.display = 'none';
        }
        else if (action === 'forward') {
            contextMenu.style.display = 'none';
            currentForwardMessageId = msgId;
            showForwardModal();
        }
        else if (action === 'react') {
            contextMenu.style.display = 'none';
            showReactionPicker(msgId);
        }
        else if (action === 'edit') {
            const newText = prompt('Редактировать сообщение:', msgText);
            if (newText && newText !== msgText) {
                const formData = new FormData();
                formData.append('edit_id', msgId);
                formData.append('text', newText);
                await fetch(window.location.href, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                    body: formData
                });
                loadMessages();
            }
            contextMenu.style.display = 'none';
        }
        else if (action === 'delete') {
            if (!confirm('Удалить сообщение?')) return;
            const formData = new FormData();
            formData.append('delete_id', msgId);
            await fetch(window.location.href, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: formData
            });
            loadMessages();
            contextMenu.style.display = 'none';
        }
    });
}

function showForwardModal() {
    const modal = document.getElementById('forwardChatModal');
    const chatsList = document.getElementById('forwardChatsList');
    chatsList.innerHTML = '';
    
    const selectedChats = new Set();
    
    document.querySelectorAll('.chat-item').forEach(item => {
        const chatId = item.dataset.chatId;
        if (chatId == currentChatId) return;
        const chatName = item.querySelector('.chat-name').innerText;
        const chatDiv = document.createElement('div');
        chatDiv.className = 'forward-chat-item';
        chatDiv.innerHTML = `<input type="checkbox" value="${chatId}" class="forward-checkbox"> <span>${chatName}</span>`;
        const checkbox = chatDiv.querySelector('.forward-checkbox');
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                selectedChats.add(chatId);
            } else {
                selectedChats.delete(chatId);
            }
            const sendBtn = document.getElementById('sendForwardBtn');
            if (sendBtn) {
                sendBtn.textContent = `Отправить (${selectedChats.size})`;
            }
        });
        chatsList.appendChild(chatDiv);
    });
    
    const existingButtons = modal.querySelector('.forward-buttons');
    if (existingButtons) existingButtons.remove();
    
    const buttonsDiv = document.createElement('div');
    buttonsDiv.className = 'forward-buttons';
    buttonsDiv.innerHTML = `
        <button id="sendForwardBtn" class="send-forward-btn">Отправить (0)</button>
        <button id="cancelForwardBtn" class="cancel-forward-btn">Отмена</button>
    `;
    modal.querySelector('.modal-content').appendChild(buttonsDiv);
    
    document.getElementById('sendForwardBtn').onclick = async () => {
        const checkboxes = document.querySelectorAll('.forward-checkbox:checked');
        if (checkboxes.length === 0) {
            showToast('Выберите хотя бы один чат');
            return;
        }
        
        let successCount = 0;
        for (const checkbox of checkboxes) {
            const targetChatId = checkbox.value;
            try {
                const response = await fetch('/api/forward-message/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message_id: currentForwardMessageId, chat_id: targetChatId })
                });
                const data = await response.json();
                if (data.success) successCount++;
            } catch (error) {
                console.error('Forward error:', error);
            }
        }
        
        modal.style.display = 'none';
        showToast(`Сообщение переслано в ${successCount} чатов`);
        currentForwardMessageId = null;
        
        if (successCount > 0) {
            setTimeout(() => location.reload(), 500);
        }
    };
    
    document.getElementById('cancelForwardBtn').onclick = () => {
        modal.style.display = 'none';
        currentForwardMessageId = null;
    };
    
    modal.style.display = 'flex';
}

function showReactionPicker(msgId) {
    const existingPicker = document.querySelector('.reaction-picker');
    if (existingPicker) existingPicker.remove();
    
    const picker = document.createElement('div');
    picker.className = 'reaction-picker';
    picker.innerHTML = `
        <div class="reaction-picker-title">Выберите реакцию</div>
        <div class="reaction-picker-grid">
            <div class="reaction-option" data-emoji="👍">👍</div>
            <div class="reaction-option" data-emoji="❤️">❤️</div>
            <div class="reaction-option" data-emoji="😮">😮</div>
            <div class="reaction-option" data-emoji="😂">😂</div>
            <div class="reaction-option" data-emoji="😢">😢</div>
            <div class="reaction-option" data-emoji="😡">😡</div>
            <div class="reaction-option" data-emoji="🎉">🎉</div>
            <div class="reaction-option" data-emoji="🔥">🔥</div>
            <div class="reaction-option" data-emoji="👏">👏</div>
            <div class="reaction-option" data-emoji="💯">💯</div>
            <div class="reaction-option" data-emoji="🤔">🤔</div>
            <div class="reaction-option" data-emoji="😎">😎</div>
        </div>
    `;
    
    const rect = document.activeElement.getBoundingClientRect();
    picker.style.position = 'fixed';
    picker.style.bottom = '80px';
    picker.style.right = '20px';
    picker.style.zIndex = '1000';
    document.body.appendChild(picker);
    
    const options = picker.querySelectorAll('.reaction-option');
    options.forEach(option => {
        option.addEventListener('click', async (e) => {
            e.stopPropagation();
            const emoji = option.getAttribute('data-emoji');
            if (emoji) {
                try {
                    const response = await fetch(`/api/message/${msgId}/react/`, {
                        method: 'POST',
                        headers: { 
                            'X-CSRFToken': getCookie('csrftoken'), 
                            'Content-Type': 'application/json' 
                        },
                        body: JSON.stringify({ emoji: emoji })
                    });
                    const data = await response.json();
                    if (data.success) {
                        loadMessages();
                        showToast(`Реакция ${emoji} добавлена`);
                    } else {
                        showToast('Ошибка при добавлении реакции');
                    }
                } catch (error) {
                    console.error('Reaction error:', error);
                    showToast('Ошибка сервера');
                }
            }
            picker.remove();
        });
    });
    
    const closePicker = (e) => {
        if (!picker.contains(e.target)) {
            picker.remove();
            document.removeEventListener('click', closePicker);
        }
    };
    setTimeout(() => document.addEventListener('click', closePicker), 100);
}

function initForwardBadgeClick() {
    document.addEventListener('click', async function(e) {
        const forwardBadge = e.target.closest('.forward-badge');
        if (forwardBadge) {
            const messageDiv = forwardBadge.closest('.message');
            const msgId = messageDiv.dataset.id;
            
            const response = await fetch(`/api/message/${msgId}/`);
            const data = await response.json();
            
            if (data.forwarded_from_user_id) {
                openProfileModal(data.forwarded_from_user_id);
            }
        }
    });
}

function openProfileModal(userId) {
    fetch(`/api/user-profile/${userId}/`)
        .then(res => res.json())
        .then(data => {
            const modal = document.createElement('div');
            modal.className = 'profile-modal';
            
            let roleText = '';
            if (data.role === 'student') roleText = 'Студент';
            else if (data.role === 'professor') roleText = 'Преподаватель';
            else if (data.role === 'staff') roleText = 'Учебная часть';
            else roleText = 'Пользователь';
            
            modal.innerHTML = `
                <div class="profile-modal-content">
                    <div class="profile-modal-header">
                        <h3>Информация о пользователе</h3>
                        <button class="close-profile-modal">&times;</button>
                    </div>
                    <div class="profile-modal-body">
                        ${data.avatar ? `<img src="${data.avatar}" class="profile-modal-avatar">` : `<div class="profile-modal-avatar placeholder">${data.full_name.charAt(0).toUpperCase()}</div>`}
                        <div class="profile-modal-name">${escapeHtml(data.full_name)}</div>
                        <div class="profile-modal-role">${roleText}</div>
                        ${data.student_info ? `<div class="profile-modal-info">🎓 ${data.student_info.group}</div>` : ''}
                        ${data.student_info ? `<div class="profile-modal-info">📚 ${data.student_info.course} курс</div>` : ''}
                        ${data.city ? `<div class="profile-modal-info">📍 ${escapeHtml(data.city)}</div>` : ''}
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            modal.querySelector('.close-profile-modal').onclick = () => modal.remove();
            modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
        });
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
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

function loadMessages() {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return;
    fetch(`/api/chat/messages/${currentChatId}/?last_id=0`)
        .then(response => response.json())
        .then(data => {
            if (data.messages && data.messages.length) {
                messagesContainer.innerHTML = '';
                updateMessages(data.messages);
            }
        });
}

function updateMessages(messages) {
    const container = document.getElementById('chatMessages');
    if (!container) return;
    let lastDate = null;
    messages.forEach(msg => {
        if (!msg.text && !msg.file) return;
        let msgDate;
        try {
            const date = new Date(msg.created_at);
            msgDate = date.toLocaleDateString();
        } catch(e) {
            msgDate = new Date().toLocaleDateString();
        }
        if (lastDate !== msgDate) {
            const divider = document.createElement('div');
            divider.className = 'date-divider';
            let dateText = '';
            const today = new Date().toLocaleDateString();
            const yesterday = new Date(Date.now() - 86400000).toLocaleDateString();
            if (msgDate === today) {
                dateText = 'Сегодня';
            } else if (msgDate === yesterday) {
                dateText = 'Вчера';
            } else {
                dateText = new Date(msgDate).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
            }
            divider.innerHTML = `<span>${dateText}</span>`;
            container.appendChild(divider);
            lastDate = msgDate;
        }
        const existingMsg = container.querySelector(`.message[data-id="${msg.id}"]`);
        const isSent = msg.sender_id == currentUserId;
        if (existingMsg) {
            existingMsg.querySelector('.message-text').innerHTML = escapeHtml(msg.text);
            const fileDiv = existingMsg.querySelector('.message-file');
            if (msg.file && msg.filename) {
                if (fileDiv) {
                    fileDiv.innerHTML = `<a href="${msg.file}" target="_blank">📎 ${msg.filename}</a>`;
                } else {
                    const newFileDiv = document.createElement('div');
                    newFileDiv.className = 'message-file';
                    newFileDiv.innerHTML = `<a href="${msg.file}" target="_blank">📎 ${msg.filename}</a>`;
                    existingMsg.querySelector('.message-bubble').appendChild(newFileDiv);
                }
            } else if (fileDiv) {
                fileDiv.remove();
            }
            const statusSpan = existingMsg.querySelector('.message-status');
            if (statusSpan && isSent) {
                if (msg.is_read) {
                    statusSpan.className = 'fa-solid fa-check-double message-status read';
                } else if (msg.is_delivered) {
                    statusSpan.className = 'fa-solid fa-check-double message-status delivered';
                } else {
                    statusSpan.className = 'fa-solid fa-check message-status sent';
                }
            }
            const reactionsDiv = existingMsg.querySelector('.message-reactions');
            if (reactionsDiv && msg.reactions) {
                reactionsDiv.innerHTML = '';
                for (const [emoji, users] of Object.entries(msg.reactions)) {
                    const badge = document.createElement('span');
                    badge.className = 'reaction-badge';
                    badge.setAttribute('data-emoji', emoji);
                    badge.setAttribute('data-message-id', msg.id);
                    badge.innerHTML = `${emoji} ${users.length}`;
                    badge.onclick = async (e) => {
                        e.stopPropagation();
                        await fetch(`/api/message/${msg.id}/react/`, {
                            method: 'POST',
                            headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
                            body: JSON.stringify({ emoji: emoji })
                        });
                        loadMessages();
                    };
                    reactionsDiv.appendChild(badge);
                }
            }
        } else {
            const div = document.createElement('div');
            div.className = `message ${isSent ? 'sent' : 'received'}`;
            div.setAttribute('data-id', msg.id);
            div.setAttribute('data-text', msg.text || '');
            div.setAttribute('data-sender-id', msg.sender_id);
            let replyHtml = '';
            if (msg.reply_to) {
                replyHtml = `<div class="reply-preview-inline"><div class="reply-sender">${escapeHtml(msg.reply_to.sender_name || 'Пользователь')}</div><div class="reply-text">${escapeHtml(msg.reply_to.text || 'Файл')}</div></div>`;
            }
            let forwardHtml = '';
            if (msg.forwarded_from) {
                forwardHtml = `<div class="forward-badge" data-forward-user-id="${msg.forwarded_from.sender_id}">📎 Переслано от ${escapeHtml(msg.forwarded_from.sender_name || 'Пользователя')}</div>`;
            }
            let reactionsHtml = '<div class="message-reactions">';
            if (msg.reactions) {
                for (const [emoji, users] of Object.entries(msg.reactions)) {
                    reactionsHtml += `<span class="reaction-badge" data-emoji="${emoji}" data-message-id="${msg.id}">${emoji} ${users.length}</span>`;
                }
            }
            reactionsHtml += '</div>';
            div.innerHTML = `
                <div class="message-bubble">
                    ${forwardHtml}
                    ${replyHtml}
                    <div class="message-text">${escapeHtml(msg.text || '')}</div>
                    ${msg.file && msg.filename ? `<div class="message-file"><a href="${msg.file}" target="_blank">📎 ${escapeHtml(msg.filename)}</a></div>` : ''}
                    <div class="message-time">
                        ${msg.time}
                        ${isSent ? (msg.is_read ? '<i class="fa-solid fa-check-double message-status read"></i>' : (msg.is_delivered ? '<i class="fa-solid fa-check-double message-status delivered"></i>' : '<i class="fa-solid fa-check message-status sent"></i>')) : ''}
                    </div>
                    ${reactionsHtml}
                </div>
            `;
            container.appendChild(div);
            const forwardBadgeDiv = div.querySelector('.forward-badge');
            if (forwardBadgeDiv) {
                forwardBadgeDiv.style.cursor = 'pointer';
                forwardBadgeDiv.style.textDecoration = 'underline';
                forwardBadgeDiv.onclick = async (e) => {
                    e.stopPropagation();
                    const userId = forwardBadgeDiv.getAttribute('data-forward-user-id');
                    if (userId) openProfileModal(userId);
                };
            }
            const reactionBadges = div.querySelectorAll('.reaction-badge');
            reactionBadges.forEach(badge => {
                badge.onclick = async (e) => {
                    e.stopPropagation();
                    const emoji = badge.getAttribute('data-emoji');
                    const messageId = badge.getAttribute('data-message-id');
                    await fetch(`/api/message/${messageId}/react/`, {
                        method: 'POST',
                        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
                        body: JSON.stringify({ emoji: emoji })
                    });
                    loadMessages();
                };
            });
        }
    });
    scrollToBottom();
    updateUnreadCounts();
}

function startUnreadPolling() {
    setInterval(updateUnreadCounts, 3000);
}

async function updateUnreadCounts() {
    try {
        const response = await fetch('/api/unread_counts/');
        const counts = await response.json();
        for (const [chatId, count] of Object.entries(counts)) {
            const badge = document.querySelector(`.unread-badge[data-chat-id="${chatId}"]`);
            if (badge) {
                if (count > 0) {
                    badge.style.display = 'inline-block';
                    badge.textContent = count;
                    let level = 1;
                    if (count >= 16) level = 6;
                    else if (count >= 13) level = 5;
                    else if (count >= 10) level = 4;
                    else if (count >= 6) level = 3;
                    else if (count >= 3) level = 2;
                    badge.className = `unread-badge level-${level}`;
                    if (count >= 16) {
                        let speed = 1;
                        if (count >= 80) speed = 0.2;
                        else if (count >= 70) speed = 0.25;
                        else if (count >= 60) speed = 0.3;
                        else if (count >= 50) speed = 0.35;
                        else if (count >= 40) speed = 0.4;
                        else if (count >= 30) speed = 0.5;
                        else if (count >= 20) speed = 0.7;
                        badge.style.animation = `pulse ${speed}s infinite`;
                    } else {
                        badge.style.animation = '';
                    }
                } else {
                    badge.style.display = 'none';
                }
            }
        }
    } catch(e) { console.warn('Unread polling error', e); }
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
        container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
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