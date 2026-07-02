let API_BASE_URL = 'https://pyshk-backend.onrender.com/api'; // Replace with your actual Render URL later if it's different
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:') {
    API_BASE_URL = 'http://127.0.0.1:8000/api';
}

class ApiService {
    constructor() {
        this.sessionToken = localStorage.getItem('chat_session_token');
    }

    async initSession() {
        if (!this.sessionToken) {
            try {
                const response = await fetch(`${API_BASE_URL}/chat/init_session/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ language: 'en' })
                });
                const data = await response.json();
                this.sessionToken = data.session_token;
                localStorage.setItem('chat_session_token', this.sessionToken);
            } catch (error) {
                console.error("Failed to initialize session", error);
            }
        }
        return this.sessionToken;
    }

    async sendMessage(content) {
        if (!this.sessionToken) await this.initSession();
        
        try {
            const response = await fetch(`${API_BASE_URL}/chat/send_message/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_token: this.sessionToken,
                    content: content
                })
            });

            // If session expired/invalid (server restarted), auto-recover
            if (response.status === 404) {
                localStorage.removeItem('chat_session_token');
                this.sessionToken = null;
                await this.initSession();
                // Retry once with the fresh session
                const retryResponse = await fetch(`${API_BASE_URL}/chat/send_message/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_token: this.sessionToken,
                        content: content
                    })
                });
                return await retryResponse.json();
            }

            return await response.json();
        } catch (error) {
            console.error("Message send failed", error);
            return null;
        }
    }
}

const api = new ApiService();
