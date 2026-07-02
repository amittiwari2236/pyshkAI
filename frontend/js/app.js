document.addEventListener('DOMContentLoaded', async () => {
    // Elements
    const chatFab = document.getElementById('chat-fab');
    const chatWindow = document.getElementById('chat-window');
    const closeBtn = document.getElementById('close-chat');
    const themeToggle = document.getElementById('theme-toggle');
    const fullscreenToggle = document.getElementById('fullscreen-toggle');
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const voiceBtn = document.getElementById('voice-btn');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');

    // Initialize session
    await api.initSession();

    // Toggle Chat Window
    chatFab.addEventListener('click', () => {
        chatWindow.classList.remove('hidden');
        chatFab.style.transform = 'scale(0)';
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.classList.add('hidden');
        chatFab.style.transform = 'scale(1)';
    });

    // Theme Toggle
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.body.getAttribute('data-theme');
        if (currentTheme === 'dark') {
            document.body.removeAttribute('data-theme');
            themeToggle.innerHTML = '<i class="fa-solid fa-moon"></i>';
        } else {
            document.body.setAttribute('data-theme', 'dark');
            themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
        }
    });

    // Fullscreen Toggle
    fullscreenToggle.addEventListener('click', () => {
        chatWindow.classList.toggle('fullscreen');
        if(chatWindow.classList.contains('fullscreen')){
            fullscreenToggle.innerHTML = '<i class="fa-solid fa-compress"></i>';
        } else {
            fullscreenToggle.innerHTML = '<i class="fa-solid fa-expand"></i>';
        }
    });

    // Input Handling
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatUI.handleSend();
        }
    });
    
    // Auto resize textarea
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    sendBtn.addEventListener('click', () => {
        chatUI.handleSend();
    });

    // Suggestions click — use data-query attribute for precise intent
    function bindChips(container) {
        container.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                const query = chip.getAttribute('data-query') || chip.textContent.trim();
                chatInput.value = query;
                chatUI.handleSend();
            });
        });
    }

    // Bind initial chips
    bindChips(document.getElementById('suggestions-container'));

    // Expose bindChips so chat.js can use it for dynamic follow-up chips
    window.bindChips = bindChips;

    // Voice button stub
    voiceBtn.addEventListener('click', () => {
        alert("Voice recognition activated. (This is a stub, Web Speech API integration goes here)");
    });
});
