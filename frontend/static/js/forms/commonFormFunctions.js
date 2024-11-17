DataDialogue.initializeCustomSelect = (formPrefix = '') => {
    const selectId = `${formPrefix}ModelSource`;
    const originalSelect = document.getElementById(selectId);
    if (!originalSelect) return;

    // Create custom select HTML
    const customSelect = document.createElement('div');
    customSelect.className = 'custom-select-container';
    customSelect.innerHTML = `
        <div class="custom-select-trigger">
            <div class="selected-option">Select source...</div>
            <span class="dropdown-arrow"></span>
        </div>
        <div class="custom-select-options">
            <div class="custom-select-option" data-value="google">
                <img src="/static/images/google-logo.png" alt="Google Logo">
                Google Cloud AI (Suggested)
            </div>
            <div class="custom-select-option" data-value="huggingface">
                <img src="/static/images/hf-logo.png" alt="Hugging Face Logo">
                Hugging Face
            </div>
        </div>
    `;

    // Insert custom select before original
    originalSelect.parentNode.insertBefore(customSelect, originalSelect);
    originalSelect.style.display = 'none';

    const trigger = customSelect.querySelector('.custom-select-trigger');
    const options = customSelect.querySelector('.custom-select-options');
    const optionElements = customSelect.querySelectorAll('.custom-select-option');

    // Toggle dropdown
    trigger.addEventListener('click', () => {
        options.classList.toggle('show');
        trigger.classList.toggle('open');
    });

    // Handle option selection
    optionElements.forEach(option => {
        option.addEventListener('click', () => {
            const value = option.dataset.value;
            const content = option.innerHTML;
            
            // Update trigger content
            trigger.querySelector('.selected-option').innerHTML = content;
            
            // Update original select
            originalSelect.value = value;
            
            // Trigger change event on original select
            const event = new Event('change', { bubbles: true });
            originalSelect.dispatchEvent(event);
            
            // Close dropdown
            options.classList.remove('show');
            trigger.classList.remove('open');
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!customSelect.contains(e.target)) {
            options.classList.remove('show');
            trigger.classList.remove('open');
        }
    });
};

DataDialogue.initializeModelSourceIcons = (formPrefix = '') => {
    const modelSource = document.getElementById(`${formPrefix}ModelSource`);
    if (!modelSource) return;

    // Function to update icon visibility
    const updateIcon = (value) => {
        // Find the icon container within the same select-with-icon container
        const iconContainer = modelSource.closest('.select-with-icon').querySelector('.model-icon');
        if (!iconContainer) return;

        const icons = iconContainer.querySelectorAll('.source-icon');
        
        // Hide all icons first
        icons.forEach(icon => {
            icon.style.display = 'none';
        });

        // Show selected icon if there's a value
        if (value) {
            const selectedIcon = iconContainer.querySelector(`.source-icon[data-source="${value}"]`);
            if (selectedIcon) {
                selectedIcon.style.display = 'block';
            }
        }
    };

    // Initial state
    updateIcon(modelSource.value);

    // Remove any existing change listeners to prevent duplicates
    const newListener = (e) => updateIcon(e.target.value);
    modelSource.removeEventListener('change', newListener);
    modelSource.addEventListener('change', newListener);
};

DataDialogue.showFormLoadingAnimation = (agentType, modelName) => {
    // Look for loading overlay inside the currently active form
    const activeForm = document.querySelector('.form-container.show, #demoFormContainer.show');
    const loadingOverlay = activeForm?.querySelector(':scope > .loading-overlay');
    console.log('Loading overlay found:', loadingOverlay); // Add this for debugging
    
    if (loadingOverlay) {
        const loadingMessage = loadingOverlay.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.innerHTML = `Creating new ${agentType} Agent.<br>⚠️ This might take a few minutes as we download and set up the ${modelName} model`;
        }
        loadingOverlay.classList.add('show');
    }
};

DataDialogue.hideFormLoadingAnimation = () => {
    // Look for loading overlay inside the currently active form
    const activeForm = document.querySelector('.form-container.show, #demoFormContainer.show');
    const loadingOverlay = activeForm?.querySelector(':scope > .loading-overlay');
    
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

