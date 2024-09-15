let controller;
let chatHistory = [];


document.addEventListener('DOMContentLoaded', (event) => {
    const submitButton = document.getElementById('submitButton');
    const userInput = document.getElementById('userInput');

    submitButton.addEventListener('click', handleSubmitClick);
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmitClick();
        }
    });

    userInput.addEventListener('input', function() {
        if (submitButton.textContent === 'Send') {
            submitButton.disabled = this.value.trim().length === 0;
        }
    });

    submitButton.disabled = true;
});

function handleSubmitClick() {
    const submitButton = document.getElementById('submitButton');
    if (submitButton.textContent === 'Send' && !submitButton.disabled) {
        submitQuery();
    } else if (submitButton.textContent === 'Cancel') {
        cancelRequest();
    }
}

function formatTimestamp(date) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

function addMessageToHistory(message, isUser) {
    const messageContainer = document.createElement('div');
    messageContainer.className = `message-container ${isUser ? 'user' : 'assistant'}`;

    const timestampDiv = document.createElement('div');
    timestampDiv.className = 'timestamp';
    timestampDiv.textContent = formatTimestamp(new Date());
    messageContainer.appendChild(timestampDiv);

    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user-message' : 'assistant-message'}`;
    
    if (!isUser) {
        messageDiv.innerHTML = formatMessage(message);
    } else {
        messageDiv.textContent = message;
    }
    
    messageContainer.appendChild(messageDiv);

    document.getElementById('chatHistory').appendChild(messageContainer);
    chatHistory.push({ message, isUser, timestamp: new Date() });
    
    const chatHistoryDiv = document.getElementById('chatHistory');
    chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight;

    if (!isUser) {
        addCopyButtonsToCodeBlocks();
    }
}

function formatMessage(message) {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    return message.replace(codeBlockRegex, (match, language, code) => {
        language = language || 'plaintext';
        // Replace newlines with <br> tags and preserve spaces
        const formattedCode = code.trim()
            .replace(/\n/g, '<br>')
            .replace(/ /g, '&nbsp;');
        return `
            <div class="code-block-wrapper">
                <pre><code class="language-${language}">${formattedCode}</code></pre>
                <button class="copy-button">Copy</button>
            </div>
        `;
    });
}

function formatCodeBlocks(message) {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    return message.replace(codeBlockRegex, (match, language, code) => {
        language = language || 'plaintext';
        return `<div class="code-block-wrapper"><pre><code class="language-${language}">${escapeHtml(code.trim())}</code></pre></div>`;
    });
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function addCopyButtonsToCodeBlocks() {
    document.querySelectorAll('.code-block-wrapper').forEach(wrapper => {
        const copyButton = wrapper.querySelector('.copy-button');
        const codeElement = wrapper.querySelector('code');
        
        copyButton.addEventListener('click', () => {
            // Get the original text (without HTML entities)
            const code = codeElement.innerText;
            navigator.clipboard.writeText(code).then(() => {
                copyButton.textContent = 'Copied!';
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        });
    });
}
function copyCodeToClipboard(block, button) {
    const code = block.querySelector('code');
    const text = code.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = 'Copy';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

function formatCodeBlocks(message) {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    return message.replace(codeBlockRegex, (match, language, code) => {
        language = language || 'plaintext';
        return `<pre><code class="language-${language}">${escapeHtml(code.trim())}</code></pre>`;
    });
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function addTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'typing-indicator';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';
    document.getElementById('chatHistory').appendChild(typingDiv);
    const chatHistoryDiv = document.getElementById('chatHistory');
    chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight;
    return typingDiv;
}

function removeTypingIndicator(typingDiv) {
    if (typingDiv && typingDiv.parentNode) {
        typingDiv.parentNode.removeChild(typingDiv);
    }
}

function submitQuery() {
    const userInput = document.getElementById('userInput');
    const submitButton = document.getElementById('submitButton');
    const message = userInput.value.trim();
    
    if (!message) return;

    addMessageToHistory(message, true);
    userInput.value = '';

    submitButton.textContent = 'Cancel';
    submitButton.classList.add('cancel');
    submitButton.disabled = false;

    const typingIndicator = addTypingIndicator();

    controller = new AbortController();
    const signal = controller.signal;

    axios.post('/', { user_input: message, chat_history: chatHistory }, {
        headers: {
            'Content-Type': 'application/json'
        },
        signal: signal
    })
    .then(function (response) {
        removeTypingIndicator(typingIndicator);
        addMessageToHistory(response.data.response, false);
    })
    .catch(function (error) {
        removeTypingIndicator(typingIndicator);
        if (error.name === 'CanceledError') {
            addMessageToHistory('Sorry, request was cancelled.', false);
        } else {
            addMessageToHistory('Error: ' + error.message, false);
        }
    })
    .finally(function () {
        resetSubmitButton();
    });
}

function cancelRequest() {
    if (controller) {
        controller.abort();
        controller = null;
    }
}

function resetSubmitButton() {
    const submitButton = document.getElementById('submitButton');
    const userInput = document.getElementById('userInput');
    submitButton.textContent = 'Send';
    submitButton.classList.remove('cancel');
    submitButton.disabled = userInput.value.trim().length === 0;
}