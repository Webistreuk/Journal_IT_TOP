document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.getElementById('menuIcon');
    const sidebarMenu = document.getElementById('sidebarMenu');
    const darkModeBtn = document.getElementById('darkModeBtn');
    const disableAnimationsBtn = document.getElementById('disableAnimationsBtn');
    const switchVersionBtn = document.getElementById('switchVersionBtn');
    const telegramFeaturesBtn = document.getElementById('telegramFeaturesBtn');
    const reportBugBtn = document.getElementById('reportBugBtn');
    const installAppBtn = document.getElementById('installAppBtn');
    const addAccountBtn = document.getElementById('addAccountBtn');
    const savedMessagesBtn = document.getElementById('savedMessagesBtn');
    const archivedChatsBtn = document.getElementById('archivedChatsBtn');
    const myStoriesBtn = document.getElementById('myStoriesBtn');
    const contactsBtn = document.getElementById('contactsBtn');
    const walletBtn = document.getElementById('walletBtn');
    const settingsBtn = document.getElementById('settingsBtn');
    const addContactBtn = document.querySelector('.add-contact-btn');
    const contactSearch = document.getElementById('contactSearch');
    const messageBtns = document.querySelectorAll('.message-contact-btn');

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
            alert('Switch to A version (demo)');
        });
    }

    if (telegramFeaturesBtn) {
        telegramFeaturesBtn.addEventListener('click', () => {
            alert('Telegram Features');
        });
    }

    if (reportBugBtn) {
        reportBugBtn.addEventListener('click', () => {
            window.location.href = '/complaint/';
        });
    }

    if (installAppBtn) {
        installAppBtn.addEventListener('click', () => {
            alert('Install App (PWA)');
        });
    }

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

    if (addContactBtn) {
        addContactBtn.addEventListener('click', function() {
            alert('Add contact feature coming soon');
        });
    }

    if (contactSearch) {
        contactSearch.addEventListener('input', function() {
            const term = this.value.toLowerCase();
            const contactItems = document.querySelectorAll('.contact-item');
            contactItems.forEach(item => {
                const name = item.querySelector('.contact-name').innerText.toLowerCase();
                item.style.display = name.includes(term) ? 'flex' : 'none';
            });
        });
    }

    messageBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const userId = this.dataset.userId;
            window.location.href = `/chats/create/${userId}/`;
        });
    });
});