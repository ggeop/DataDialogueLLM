DataDialogue.initializeModelSelections = async (formPrefix = '') => {
    try {
        const response = await fetch('http://localhost:8000/api/v1/models/list');
        if (!response.ok) throw new Error('Failed to fetch model configurations');
        const modelConfigs = await response.json();
        
        // Store model configs for later use
        DataDialogue.modelConfigs = modelConfigs;

        // Initialize custom select with dynamic model sources
        const selectId = `${formPrefix}ModelSource`;
        const originalSelect = document.getElementById(selectId);
        if (!originalSelect) return;

        // Ensure the original select has the options too
        originalSelect.innerHTML = `
            <option value="">Select source...</option>
            ${modelConfigs.map(config => 
                `<option value="${config.source_id}">${config.display_name}</option>`
            ).join('')}
        `;

        // Create and setup custom select UI
        await DataDialogue.initializeCustomSelect(formPrefix);

        // Initialize model source icons
        DataDialogue.initializeModelSourceIcons(formPrefix);

        // Add change handler for model source
        originalSelect.addEventListener('change', () => {
            const selectedConfig = DataDialogue.modelConfigs?.find(c => c.source_id === originalSelect.value);
            if (!selectedConfig) return;

            // Handle token visibility
            const tokenGroup = document.getElementById(`${formPrefix}tokenGroup`) || document.getElementById('tokenGroup');
            if (tokenGroup) {
                if (selectedConfig.has_token) {
                    tokenGroup.classList.remove('initially-hidden');
                    tokenGroup.style.display = 'block';
                } else {
                    tokenGroup.style.display = 'none';
                    tokenGroup.classList.add('initially-hidden');
                }
            }

            // Update model options
            DataDialogue.updateModelOptions(formPrefix, selectedConfig);
        });

    } catch (error) {
        console.error('Error initializing model selections:', error);
        DataDialogue.showMessage('Failed to load model configurations');
    }
};

DataDialogue.updateModelOptions = (formPrefix, selectedConfig) => {
    const containerID = formPrefix === 'demo' ? 'demoModelSelectContainer' : 'modelSelectContainer';
    const modelSelectContainer = document.getElementById(containerID);
    
    if (!modelSelectContainer) {
        console.error('Could not find model select container:', containerID);
        return;
    }
    
    // Clear existing content and ensure the container is visible
    modelSelectContainer.innerHTML = '';
    modelSelectContainer.classList.remove('initially-hidden');
    
    // Remove the style property completely and set it fresh
    modelSelectContainer.removeAttribute('style');
    Object.assign(modelSelectContainer.style, {
        display: 'block',
        visibility: 'visible',
        height: 'auto',
        opacity: '1',
        overflow: 'visible',
        margin: '1rem 0'
    });

    // Set IDs based on form prefix
    const repoSelectId = formPrefix === 'demo' ? 'demoRepoSelect' : `${formPrefix}repoSelect`;
    const variantSelectId = formPrefix === 'demo' ? 'demoVariantSelect' : `${formPrefix}variantSelect`;
    const modelSelectId = formPrefix === 'demo' ? 'demoModelSelect' : `${formPrefix}modelSelect`;
    const customModelInputId = formPrefix === 'demo' ? 'demoCustomModel' : `${formPrefix}customModel`;
    
    if (selectedConfig.options.some(opt => opt.repo_id)) {
        // Create repo and variant selects for Hugging Face style models
        const repoGroup = document.createElement('div');
        repoGroup.className = 'form-group';
        repoGroup.style.display = 'block';
        repoGroup.innerHTML = `
            <label style="display: block; margin-bottom: 0.5rem;">Repository ID:</label>
            <select id="${repoSelectId}" class="form-control">
                <option value="">Select repository...</option>
                ${selectedConfig.options.map(opt => opt.repo_id ? 
                    `<option value="${opt.repo_id}">${opt.label}</option>` : 
                    '').join('')}
            </select>
        `;

        const variantGroup = document.createElement('div');
        variantGroup.className = 'form-group initially-hidden';
        variantGroup.id = `${formPrefix}variantGroup`;
        variantGroup.innerHTML = `
            <label style="display: block; margin-bottom: 0.5rem;">Model Variant:</label>
            <select id="${variantSelectId}" class="form-control">
                <option value="">Select variant...</option>
            </select>
            <div id="${customModelInputId}Container" style="display: none; margin-top: 0.5rem;">
                <input type="text" id="${customModelInputId}" class="form-control" placeholder="Enter custom model name">
            </div>
        `;

        modelSelectContainer.appendChild(repoGroup);
        modelSelectContainer.appendChild(variantGroup);

        // Add repo select change handler
        const repoSelect = document.getElementById(repoSelectId);
        if (repoSelect) {
            repoSelect.addEventListener('change', function() {
                const selectedRepo = selectedConfig.options.find(opt => opt.repo_id === this.value);
                const variantGroup = document.getElementById(`${formPrefix}variantGroup`);
                const variantSelect = document.getElementById(variantSelectId);

                if (selectedRepo?.variants) {
                    variantSelect.innerHTML = `
                        <option value="">Select variant...</option>
                        ${selectedRepo.variants.map(variant => 
                            `<option value="${variant.value}">${variant.label}${variant.size ? ` (${variant.size})` : ''}</option>`
                        ).join('')}
                        <option value="custom">Custom Model...</option>
                    `;
                    variantGroup.classList.remove('initially-hidden');
                    variantGroup.style.display = 'block';

                    // Add change handler for variant select
                    variantSelect.addEventListener('change', function() {
                        const customInputContainer = document.getElementById(`${customModelInputId}Container`);
                        const customInput = document.getElementById(customModelInputId);
                        
                        if (this.value === 'custom') {
                            customInputContainer.style.display = 'block';
                            customInput.value = '';
                        } else {
                            customInputContainer.style.display = 'none';
                            customInput.value = this.value;
                        }
                    });
                }
            });
        }
    } else {
        // Create simple model select for other sources
        const modelGroup = document.createElement('div');
        modelGroup.className = 'form-group';
        modelGroup.style.display = 'block';
        modelGroup.innerHTML = `
            <label style="display: block; margin-bottom: 0.5rem;">Model:</label>
            <div>
                <select id="${modelSelectId}" class="form-control">
                    <option value="">Select model...</option>
                    ${selectedConfig.options.map(opt => 
                        `<option value="${opt.value}">${opt.label}${opt.suggested ? ' (Suggested)' : ''}</option>`
                    ).join('')}
                    <option value="custom">Custom Model...</option>
                </select>
                <div id="${customModelInputId}Container" style="display: none; margin-top: 0.5rem;">
                    <input type="text" id="${customModelInputId}" class="form-control" placeholder="Enter custom model name">
                </div>
            </div>
        `;

        modelSelectContainer.appendChild(modelGroup);

        // Add change handler for model select
        const modelSelect = document.getElementById(modelSelectId);
        if (modelSelect) {
            modelSelect.addEventListener('change', function() {
                const customInputContainer = document.getElementById(`${customModelInputId}Container`);
                const customInput = document.getElementById(customModelInputId);
                
                if (this.value === 'custom') {
                    customInputContainer.style.display = 'block';
                    customInput.value = '';
                } else {
                    customInputContainer.style.display = 'none';
                    customInput.value = this.value;
                }
            });
        }
    }

    // Force a reflow to ensure styles are applied
    modelSelectContainer.offsetHeight;
};


DataDialogue.initializeCustomSelect = async (formPrefix = '') => {
    try {
        // Fetch model configurations
        const response = await fetch('http://localhost:8000/api/v1/models/list');
        if (!response.ok) throw new Error('Failed to fetch model configurations');
        const modelConfigs = await response.json();
        
        // Store model configs for later use
        DataDialogue.modelConfigs = modelConfigs;

        const selectId = `${formPrefix}ModelSource`;
        const originalSelect = document.getElementById(selectId);
        if (!originalSelect) return;

        // Create custom select HTML
        const customSelect = document.createElement('div');
        customSelect.className = 'custom-select-container';
        
        // Generate options HTML dynamically from model configs
        const optionsHTML = modelConfigs.map(config => `
            <div class="custom-select-option" data-value="${config.source_id}">
                <img src="${config.logo_path}" alt="${config.display_name} Logo">
                ${config.display_name} ${config.suggested ? '(Suggested)' : ''}
            </div>
        `).join('');

        customSelect.innerHTML = `
            <div class="custom-select-trigger">
                <div class="selected-option">Select source...</div>
                <span class="dropdown-arrow"></span>
            </div>
            <div class="custom-select-options">
                ${optionsHTML}
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
                
                // Update icon immediately
                DataDialogue.initializeModelSourceIcons(formPrefix);
                
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

        // Initialize model source icons
        DataDialogue.initializeModelSourceIcons(formPrefix);

    } catch (error) {
        console.error('Error initializing custom select:', error);
        DataDialogue.showMessage('Failed to load model configurations');
    }
};

DataDialogue.initializeModelSourceIcons = (formPrefix = '') => {
    const modelSource = document.getElementById(`${formPrefix}ModelSource`);
    if (!modelSource) return;

    // Function to update icon visibility
    const updateIcon = (value) => {
        // Find the icon container within the same select-with-icon container
        const selectWithIcon = modelSource.closest('.select-with-icon');
        if (!selectWithIcon) return;
        
        const iconContainer = selectWithIcon.querySelector('.model-icon');
        if (!iconContainer) return;

        // Clear existing icons
        iconContainer.innerHTML = '';

        // Find selected config
        const selectedConfig = DataDialogue.modelConfigs?.find(c => c.source_id === value);
        if (selectedConfig) {
            const icon = document.createElement('img');
            icon.src = selectedConfig.logo_path;
            icon.alt = `${selectedConfig.display_name} Logo`;
            icon.className = 'source-icon';
            icon.dataset.source = value;
            iconContainer.appendChild(icon);
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
