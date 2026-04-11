// Communication with VS Code extension
const vscode = acquireVsCodeApi();

// DOM elements
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

// Track typing indicator
let typingIndicator = null;

// Send message handler
function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;

    vscode.postMessage({
        command: 'sendMessage',
        text: text
    });

    messageInput.value = '';
    messageInput.style.height = 'auto';
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-resize textarea
messageInput.addEventListener('input', () => {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
});

// Handle messages from extension
window.addEventListener('message', (event) => {
    const message = event.data;

    switch (message.command) {
        case 'addMessage':
            addMessageToUI(message.role, message.content, message.isTyping);
            break;
        case 'updateTyping':
            updateTypingMessage(message.content);
            break;
        case 'removeTyping':
            removeTypingIndicator();
            break;
        case 'clearChat':
            clearChatUI();
            break;
    }
});

// Add message to UI
function addMessageToUI(role, content, isTyping = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}${isTyping ? ' typing' : ''}`;
    
    // Convert markdown-like text to HTML
    messageDiv.innerHTML = formatMessage(content);
    
    messagesContainer.appendChild(messageDiv);
    scrollToBottom();

    if (isTyping) {
        typingIndicator = messageDiv;
    }
}

// Remove typing indicator
function removeTypingIndicator() {
    if (typingIndicator && typingIndicator.parentNode) {
        typingIndicator.parentNode.removeChild(typingIndicator);
        typingIndicator = null;
    }
}

// Update the text of the current typing indicator
function updateTypingMessage(text) {
    if (typingIndicator) {
        typingIndicator.innerHTML = formatMessage(text);
        scrollToBottom();
    }
}

// Clear chat UI
function clearChatUI() {
    messagesContainer.innerHTML = '';
}

// Format message text (basic markdown support)
function formatMessage(text) {
    // Escape HTML
    let formatted = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    // Bold
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Code blocks
    formatted = formatted.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    
    // Inline code
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Lists
    formatted = formatted.replace(/^- (.+)$/gm, '<li>$1</li>');
    formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    // Numbered lists
    formatted = formatted.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

    return formatted;
}

// Scroll to bottom
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
