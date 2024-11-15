DataDialogue.showFormLoadingAnimation = (agentType, modelName) => {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        const loadingMessage = loadingOverlay.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.innerHTML = `Creating new ${agentType} Agent.<br>⚠️ This might take a few minutes as we download and set up the ${modelName} model`;
        }
        loadingOverlay.classList.add('show');
    }
};

DataDialogue.hideFormLoadingAnimation = () => {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('show');
    }
};

DataDialogue.initializeMessageSystem = () => {
    // Create message overlay element if it doesn't exist
    if (!document.querySelector('.message-overlay')) {
        const messageHTML = `
            <div class="message-overlay">
                <div class="message-content">
                    <span class="message-text"></span>
                    <button class="message-close">×</button>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', messageHTML);

        // Add click handler for close button
        const closeBtn = document.querySelector('.message-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', DataDialogue.hideMessage);
        }
    }
};

DataDialogue.showMessage = (message, duration = 5000) => {
    const messageOverlay = document.querySelector('.message-overlay');
    const messageText = document.querySelector('.message-text');
    
    if (messageOverlay && messageText) {
        messageText.textContent = message;
        messageOverlay.classList.add('show');
        
        // Auto-hide after duration
        setTimeout(DataDialogue.hideMessage, duration);
    }
};

DataDialogue.hideMessage = () => {
    const messageOverlay = document.querySelector('.message-overlay');
    if (messageOverlay) {
        messageOverlay.classList.remove('show');
    }
};

