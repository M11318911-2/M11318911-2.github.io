// ChatBot Class
class ChatBot {
    constructor() {
        // ⚠️ Important: Replace with your n8n webhook URL
        // ****************************************************************
        this.webhookUrl = 'https://a3g.app.n8n.cloud/webhook/chat_webhook';
        // ****************************************************************        
        // Initialize session ID
        this.sessionId = this.getOrCreateSessionId();
        
        // Create ChatBot UI
        this.createChatBotUI();
        
        // DOM elements
        this.chatbotToggle = document.getElementById('chatbotToggle');
        this.chatbotPanel = document.getElementById('chatbotPanel');
        this.chatbotClose = document.getElementById('chatbotClose');
        this.messagesContainer = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.notificationBadge = document.getElementById('notificationBadge');
        
        // Bind events
        this.bindEvents();
        
        // Load chat history
        this.loadChatHistory();
        
        console.log('ChatBot initialized successfully, Session ID:', this.sessionId);
    }
    
    createChatBotUI() {
        // Create CSS styles
        const style = document.createElement('style');
        style.textContent = `
            .chatbot-widget {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1000;
            }

            .chatbot-toggle {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
                border: none;
                border-radius: 50%;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(255, 107, 157, 0.4);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                color: white;
                font-size: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                animation: float 3s ease-in-out infinite;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-8px); }
            }

            .chatbot-toggle:hover {
                transform: scale(1.1) translateY(-2px);
                box-shadow: 0 8px 30px rgba(255, 107, 157, 0.5);
                background: linear-gradient(135deg, #ff7bb0 0%, #d15587 100%);
            }

            .chatbot-toggle:active {
                transform: scale(0.95);
            }

            .chatbot-panel {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(255, 107, 157, 0.2);
                display: none;
                flex-direction: column;
                overflow: hidden;
                border: 2px solid rgba(255, 107, 157, 0.1);
                backdrop-filter: blur(10px);
            }

            .chatbot-panel.active {
                display: flex;
                animation: slideInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }

            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px) scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            .chatbot-header {
                background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
                color: white;
                padding: 18px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: relative;
                overflow: hidden;
            }

            .chatbot-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                animation: shimmer 3s infinite;
            }

            @keyframes shimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }

            .chatbot-title {
                font-size: 16px;
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .title-icon {
                animation: bounce 2s infinite;
            }

            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-4px); }
            }

            .chatbot-close {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
            }

            .chatbot-close:hover {
                background: rgba(255,255,255,0.2);
                transform: rotate(90deg);
            }

            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 12px;
                background: linear-gradient(135deg, #ffeef4 0%, #ffe0eb 100%);
                position: relative;
            }

            .chat-messages::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    radial-gradient(circle at 20% 20%, rgba(255, 107, 157, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(196, 69, 105, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 60%, rgba(255, 182, 193, 0.1) 0%, transparent 50%);
                pointer-events: none;
            }

            .message {
                max-width: 80%;
                padding: 12px 16px;
                border-radius: 20px;
                line-height: 1.4;
                word-wrap: break-word;
                font-size: 14px;
                animation: messageSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                z-index: 1;
            }

            @keyframes messageSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(20px) scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            .message.user {
                background: linear-gradient(135deg, #ff6b9d, #c44569);
                color: white;
                align-self: flex-end;
                border-bottom-right-radius: 6px;
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
            }

            .message.user::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
                border-radius: inherit;
            }

            .message.ai {
                background: white;
                color: #333;
                align-self: flex-start;
                border-bottom-left-radius: 6px;
                border: 2px solid #ffcce0;
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.1);
                animation: messageSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1), glow 2s ease-in-out;
            }

            @keyframes glow {
                0%, 100% { box-shadow: 0 4px 15px rgba(255, 107, 157, 0.1); }
                50% { box-shadow: 0 4px 20px rgba(255, 107, 157, 0.3); }
            }

            .message.system {
                background: linear-gradient(135deg, #ff9ac1, #e91e63);
                color: white;
                align-self: center;
                font-size: 12px;
                max-width: 90%;
                text-align: center;
                animation: messageSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1), pulse 2s infinite;
            }

            .message.error-message {
                background: linear-gradient(135deg, #ff4757, #c44569);
                color: white;
                align-self: center;
                font-size: 12px;
                max-width: 90%;
                text-align: center;
                animation: shake 0.5s ease-in-out;
            }

            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-4px); }
                75% { transform: translateX(4px); }
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.02); }
            }

            .typing-indicator {
                display: none;
                align-self: flex-start;
                padding: 12px 16px;
                background: white;
                border-radius: 20px;
                border-bottom-left-radius: 6px;
                border: 2px solid #ffcce0;
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.1);
                animation: typingPulse 1s infinite;
            }

            @keyframes typingPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }

            .typing-dots {
                display: flex;
                gap: 4px;
            }

            .typing-dot {
                width: 8px;
                height: 8px;
                background: linear-gradient(135deg, #ff6b9d, #c44569);
                border-radius: 50%;
                animation: typingAnimation 1.4s infinite ease-in-out;
            }

            .typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }

            .typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }

            @keyframes typingAnimation {
                0%, 60%, 100% {
                    transform: scale(0.8);
                    opacity: 0.5;
                }
                30% {
                    transform: scale(1.2);
                    opacity: 1;
                }
            }

            .chat-input {
                padding: 15px;
                border-top: 2px solid #ffcce0;
                display: flex;
                gap: 10px;
                background: white;
                position: relative;
            }

            .chat-input::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, #ff6b9d, #c44569, #ff6b9d);
                background-size: 200% 100%;
                animation: gradientMove 3s linear infinite;
            }

            @keyframes gradientMove {
                0% { background-position: 200% 0; }
                100% { background-position: -200% 0; }
            }

            .input-field {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #ffcce0;
                border-radius: 25px;
                outline: none;
                font-size: 14px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                background: linear-gradient(135deg, #fff 0%, #fef7fa 100%);
            }

            .input-field:focus {
                border-color: #ff6b9d;
                box-shadow: 0 0 20px rgba(255, 107, 157, 0.2);
                transform: translateY(-2px);
            }

            .send-button {
                padding: 12px 18px;
                background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }

            .send-button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }

            .send-button:hover:not(:disabled) {
                transform: translateY(-2px) scale(1.05);
                box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
            }

            .send-button:hover:not(:disabled)::before {
                left: 100%;
            }

            .send-button:active:not(:disabled) {
                transform: translateY(0) scale(0.98);
            }

            .send-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }

            .notification-badge {
                position: absolute;
                top: -8px;
                right: -8px;
                width: 24px;
                height: 24px;
                background: linear-gradient(135deg, #ff4757, #c44569);
                color: white;
                border-radius: 50%;
                font-size: 12px;
                display: none;
                align-items: center;
                justify-content: center;
                animation: notificationPulse 1.5s infinite, bounce 2s infinite;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
            }

            @keyframes notificationPulse {
                0% { 
                    transform: scale(1); 
                    box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
                }
                50% { 
                    transform: scale(1.1); 
                    box-shadow: 0 6px 20px rgba(255, 71, 87, 0.6);
                }
                100% { 
                    transform: scale(1); 
                    box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
                }
            }

            /* Responsive Design */
            @media (max-width: 768px) {
                .chatbot-panel {
                    width: 320px;
                    height: 450px;
                    bottom: 70px;
                }
            }

            @media (max-width: 480px) {
                .chatbot-widget {
                    bottom: 15px;
                    right: 15px;
                }
                
                .chatbot-toggle {
                    width: 50px;
                    height: 50px;
                    font-size: 20px;
                }
                
                .chatbot-panel {
                    width: calc(100vw - 30px);
                    height: 70vh;
                    bottom: 75px;
                    right: -15px;
                }
            }

            /* Custom Scrollbar */
            .chat-messages::-webkit-scrollbar {
                width: 6px;
            }

            .chat-messages::-webkit-scrollbar-track {
                background: #ffcce0;
                border-radius: 3px;
            }

            .chat-messages::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #ff6b9d, #c44569);
                border-radius: 3px;
            }

            .chat-messages::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #ff7bb0, #d15587);
            }
        `;
        document.head.appendChild(style);
        
        // Create ChatBot HTML
        const chatbotHTML = `
            <div class="chatbot-widget" id="chatbotWidget">
                <button class="chatbot-toggle" id="chatbotToggle">
                    <i class="fas fa-comments"></i>
                    <div class="notification-badge" id="notificationBadge">!</div>
                </button>
                
                <div class="chatbot-panel" id="chatbotPanel">
                    <div class="chatbot-header">
                        <div class="chatbot-title">
                            <span class="title-icon">🤖</span>
                            Prof Luarn's AI Assistant v6
                        </div>
                        <button class="chatbot-close" id="chatbotClose">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="chat-messages" id="chatMessages">
                        <div class="message system">
                            Welcome! I can answer any questions for you.
                        </div>
                    </div>
                    
                    <div class="typing-indicator" id="typingIndicator">
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                    
                    <div class="chat-input">
                        <input 
                            type="text" 
                            class="input-field" 
                            id="messageInput" 
                            placeholder="Type your question..."
                            maxlength="500"
                        >
                        <button class="send-button" id="sendButton" disabled>Send</button>
                    </div>
                </div>
            </div>
        `;
        
        // Insert at end of body
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }
    
    getOrCreateSessionId() {
        let sessionId = localStorage.getItem('chatbot_session_id');
        if (!sessionId) {
            sessionId = 'web_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('chatbot_session_id', sessionId);
        }
        return sessionId;
    }
    
    bindEvents() {
        // Chatbot toggle
        this.chatbotToggle.addEventListener('click', () => {
            this.toggleChatbot();
        });
        
        this.chatbotClose.addEventListener('click', () => {
            this.closeChatbot();
        });
        
        // Send button click event
        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Input field key press event
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Input field input event
        this.messageInput.addEventListener('input', () => {
            this.sendButton.disabled = this.messageInput.value.trim() === '';
        });
        
        // Click outside to close chatbot
        document.addEventListener('click', (e) => {
            if (!this.chatbotToggle.contains(e.target) && 
                !this.chatbotPanel.contains(e.target) && 
                this.chatbotPanel.classList.contains('active')) {
                this.closeChatbot();
            }
        });
    }
    
    toggleChatbot() {
        if (this.chatbotPanel.classList.contains('active')) {
            this.closeChatbot();
        } else {
            this.openChatbot();
        }
    }
    
    openChatbot() {
        this.chatbotPanel.classList.add('active');
        this.messageInput.focus();
        this.hideNotification();
        this.scrollToBottom();
    }
    
    closeChatbot() {
        this.chatbotPanel.classList.remove('active');
    }
    
    showNotification() {
        this.notificationBadge.style.display = 'flex';
    }
    
    hideNotification() {
        this.notificationBadge.style.display = 'none';
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Show user message
        this.addMessage(message, 'user');
        
        // Clear input and disable send button
        this.messageInput.value = '';
        this.sendButton.disabled = true;
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send request to n8n webhook
            const response = await fetch(this.webhookUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    sessionId: this.sessionId,
                    timestamp: new Date().toISOString()
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success && data.message) {
                this.addMessage(data.message, 'ai');
                
                // Save conversation to local storage
                this.saveChatToLocal(message, data.message);
                
                // Show notification if chatbot is closed
                if (!this.chatbotPanel.classList.contains('active')) {
                    this.showNotification();
                }
            } else {
                throw new Error('Invalid response format');
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('Sorry, an error occurred. Please check your network connection or try again later.', 'error-message');
        } finally {
            // Hide typing indicator
            this.hideTypingIndicator();
        }
    }
    
    addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = content;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'block';
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }
    
    saveChatToLocal(userMessage, aiMessage) {
        const chatHistory = JSON.parse(localStorage.getItem('chatbot_history') || '[]');
        
        chatHistory.push({
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId,
            userMessage: userMessage,
            aiMessage: aiMessage
        });
        
        // Limit history records (keep max 100 entries)
        if (chatHistory.length > 100) {
            chatHistory.splice(0, chatHistory.length - 100);
        }
        
        localStorage.setItem('chatbot_history', JSON.stringify(chatHistory));
    }
    
    loadChatHistory() {
        const chatHistory = JSON.parse(localStorage.getItem('chatbot_history') || '[]');
        const currentSessionHistory = chatHistory.filter(chat => chat.sessionId === this.sessionId);
        
        // Only load the latest 10 conversations
        const recentHistory = currentSessionHistory.slice(-10);
        
        recentHistory.forEach(chat => {
            this.addMessage(chat.userMessage, 'user');
            this.addMessage(chat.aiMessage, 'ai');
        });
        
        if (recentHistory.length === 0) {
            // If no history, show welcome message
            setTimeout(() => {
                this.addMessage('Hello! I\'m Prof Luarn\'s AI Assistant. Do you have any questions?', 'ai');
            }, 1000);
        }
    }
    
    // Method to clear chat history (can be called in console)
    clearHistory() {
        localStorage.removeItem('chatbot_history');
        localStorage.removeItem('chatbot_session_id');
        location.reload();
    }
}

// Initialize ChatBot
document.addEventListener('DOMContentLoaded', function() {
    // Wait one second to ensure page is fully loaded
    setTimeout(() => {
        window.chatBot = new ChatBot();
        
        // Provide method to clear history in console
        window.clearChatHistory = () => {
            if (confirm('Are you sure you want to clear all chat history?')) {
                window.chatBot.clearHistory();
            }
        };
        
        console.log('ChatBot loaded successfully!');
        console.log('To clear chat history, run in console: clearChatHistory()');
    }, 1000);
});
