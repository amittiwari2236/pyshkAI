// Follow-up chip sets per topic — shown after AI responds
const FOLLOW_UP_CHIPS = {
    courses:       [{ label: '💰 Fees', query: 'What are the fees?' }, { label: '📝 Admissions', query: 'Tell me about the admission process' }, { label: '🗓️ Schedule', query: 'What are the class schedules?' }],
    admissions:    [{ label: '📋 Eligibility', query: 'What is the eligibility criteria?' }, { label: '📄 Documents', query: 'What documents are required?' }, { label: '💰 Fees', query: 'What are the fees?' }],
    fees:          [{ label: '📚 Courses', query: 'What courses does PYSHK offer?' }, { label: '🏦 Installments', query: 'Are there installment options?' }, { label: '🎓 Scholarships', query: 'Are scholarships available?' }],
    teachers:      [{ label: '📚 Courses', query: 'What courses does PYSHK offer?' }, { label: '🗓️ Schedule', query: 'What are the class schedules?' }],
    schedules:     [{ label: '📚 Courses', query: 'What courses does PYSHK offer?' }, { label: '👨‍🏫 Teachers', query: 'Tell me about the teachers' }],
    yoga:          [{ label: '💰 Yoga Fees', query: 'What are the fees for yoga?' }, { label: '📝 Enroll', query: 'How do I enroll in yoga?' }],
    certifications:[{ label: '📝 Admissions', query: 'Tell me about the admission process' }, { label: '💰 Fees', query: 'What are the fees?' }],
    faqs:          [{ label: '📚 Courses', query: 'What courses does PYSHK offer?' }, { label: '📝 Admissions', query: 'Tell me about the admission process' }],
    contact:       [{ label: '📚 Courses', query: 'What courses does PYSHK offer?' }, { label: '📝 Admissions', query: 'Tell me about the admission process' }],
};

const TOPIC_KEYWORDS = {
    courses:       ['course', 'program', 'offer', 'available', 'study'],
    admissions:    ['admission', 'enroll', 'register', 'join', 'apply', 'process', 'document', 'eligibility'],
    fees:          ['fee', 'fees', 'cost', 'price', 'charge', 'installment', 'scholarship', 'discount'],
    teachers:      ['teacher', 'faculty', 'instructor', 'staff', 'trainer'],
    schedules:     ['schedule', 'timetable', 'batch', 'timing', 'class'],
    yoga:          ['yoga', 'meditation', 'wellness'],
    certifications:['certif', 'certificate'],
    faqs:          ['faq', 'question', 'help'],
    contact:       ['contact', 'phone', 'email', 'support', 'reach'],
};

function detectTopic(text) {
    const lower = text.toLowerCase();
    for (const [topic, keywords] of Object.entries(TOPIC_KEYWORDS)) {
        if (keywords.some(k => lower.includes(k))) return topic;
    }
    return 'courses'; // default fallback
}

class ChatUI {
    constructor() {
        this.chatBody = document.getElementById('chat-body');
        this.chatInput = document.getElementById('chat-input');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.sendBtn = document.getElementById('send-btn');
        this.isGenerating = false;
        this.lastQuery = '';
    }

    appendMessage(content, sender, isHtml = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender === 'User' ? 'user-message' : 'ai-message'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (isHtml) {
            contentDiv.innerHTML = content;
        } else {
            if (typeof marked !== 'undefined') {
                contentDiv.innerHTML = marked.parse(content);
            } else {
                contentDiv.textContent = content;
            }
        }
        
        msgDiv.appendChild(contentDiv);
        
        // Insert before typing indicator
        this.chatBody.insertBefore(msgDiv, this.typingIndicator);
        this.scrollToBottom();
    }

    appendFollowUpChips(query) {
        // Remove any previous follow-up chip rows
        const existing = this.chatBody.querySelectorAll('.followup-chips');
        existing.forEach(el => el.remove());

        const topic = detectTopic(query);
        const chips = FOLLOW_UP_CHIPS[topic];
        if (!chips || chips.length === 0) return;

        const chipRow = document.createElement('div');
        chipRow.className = 'suggestions-container followup-chips';
        chipRow.style.marginTop = '6px';

        chips.forEach(({ label, query: chipQuery }) => {
            const btn = document.createElement('button');
            btn.className = 'suggestion-chip';
            btn.textContent = label;
            btn.setAttribute('data-query', chipQuery);
            chipRow.appendChild(btn);
        });

        // Insert before typing indicator
        this.chatBody.insertBefore(chipRow, this.typingIndicator);
        this.scrollToBottom();

        // Bind click handlers if bindChips is available
        if (typeof window.bindChips === 'function') {
            window.bindChips(chipRow);
        }
    }

    showTyping() {
        this.typingIndicator.classList.remove('hidden');
        this.scrollToBottom();
    }

    hideTyping() {
        this.typingIndicator.classList.add('hidden');
    }

    scrollToBottom() {
        this.chatBody.scrollTop = this.chatBody.scrollHeight;
    }

    setLoadingState(isLoading) {
        this.isGenerating = isLoading;
        this.chatInput.disabled = isLoading;
        if (this.sendBtn) {
            this.sendBtn.disabled = isLoading;
        }
        
        if (isLoading) {
            this.showTyping();
        } else {
            this.hideTyping();
            this.chatInput.focus();
        }
    }

    async handleSend() {
        if (this.isGenerating) return;
        
        const text = this.chatInput.value.trim();
        if (!text) return;

        this.lastQuery = text;

        // Clear input and show user msg
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';
        this.appendMessage(text, 'User');
        
        // Hide the initial suggestion chips once user starts chatting
        const initialChips = document.getElementById('suggestions-container');
        if (initialChips) initialChips.style.display = 'none';

        // Show AI typing and disable inputs
        this.setLoadingState(true);

        // Send to backend
        const response = await api.sendMessage(text);
        
        // Hide AI typing and re-enable inputs
        this.setLoadingState(false);
        
        if (response && response.ai_response) {
            this.appendMessage(response.ai_response.content, 'AI');
            // Show smart follow-up chips based on the topic
            this.appendFollowUpChips(text);
        } else {
            this.appendMessage("Sorry, I am having trouble connecting to the server.", 'AI');
        }
    }
}

const chatUI = new ChatUI();
