DataDialogue.openRegisterForm = () => {
    const { formContainer, pageOverlay, menuIcon, tryDemoContainer } = DataDialogue.elements;
    
    if (formContainer && pageOverlay) {
        // Reset the form when opening
        const agentTypeSelect = document.getElementById('agentType');
        
        if (agentTypeSelect) {
            agentTypeSelect.value = '';
            DataDialogue.handleAgentTypeChange(); // This will hide the sections
        }
        
        // Clear any existing custom select before reinitializing
        const existingCustomSelect = document.querySelector('.custom-select-container');
        if (existingCustomSelect) {
            existingCustomSelect.remove();
        }
        
        // Initialize model selections with empty prefix for register form
        DataDialogue.initializeModelSelections('');

        formContainer.classList.add('show');
        pageOverlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // Hide menu icon and try demo button
        if (menuIcon) menuIcon.style.display = 'none';
        if (tryDemoContainer) tryDemoContainer.style.display = 'none';
        
        // Add event listener for agent type changes
        if (agentTypeSelect) {
            // Remove existing listener to prevent duplicates
            agentTypeSelect.removeEventListener('change', DataDialogue.handleAgentTypeChange);
            // Add new listener
            agentTypeSelect.addEventListener('change', DataDialogue.handleAgentTypeChange);
        }
    }
};

DataDialogue.handleAgentTypeChange = () => {
    const agentType = document.getElementById('agentType').value;
    const sourceConfigSection = document.getElementById('sourceConfigSection');
    const llmConfigSection = document.getElementById('llmConfigSection');
    
    // First hide both sections
    sourceConfigSection.classList.add('initially-hidden');
    llmConfigSection.classList.add('initially-hidden');
    
    // Then show appropriate sections based on selection
    if (agentType === 'SQL') {
        sourceConfigSection.classList.remove('initially-hidden');
        llmConfigSection.classList.remove('initially-hidden');
    } else if (agentType === 'General') {
        llmConfigSection.classList.remove('initially-hidden');
    }
};

DataDialogue.submitForm = async () => {
    const agentType = document.getElementById('agentType')?.value;
    const modelProvider = document.getElementById('ModelProvider')?.value;
    
    if (!agentType) {
        DataDialogue.showMessage('Please select an agent type');
        return;
    }

    if (!modelProvider) {
        DataDialogue.showMessage('Please select a Model Provider');
        return;
    }

    // Get the selected config to determine how to get the model name
    const selectedConfig = DataDialogue.modelConfigs?.find(c => c.source_id === modelProvider);
    if (!selectedConfig) {
        DataDialogue.showMessage('Invalid Model Provider');
        return;
    }

    // Get model name and repo ID based on the model structure
    let modelName = '';
    let repoID = '';

    if (selectedConfig.options.some(opt => opt.repo_id)) {
        // For models with repository (like Hugging Face)
        repoID = document.getElementById('repoSelect')?.value;
        const variantSelect = document.getElementById('variantSelect');
        const customInput = document.getElementById('customModel');
        modelName = variantSelect?.value === 'custom' ? customInput?.value : variantSelect?.value;
        
        if (!repoID) {
            DataDialogue.showMessage('Please select a repository');
            return;
        }
        if (!modelName) {
            DataDialogue.showMessage('Please select a model variant or enter a custom model name');
            return;
        }
    } else {
        // For simple model selection (like Google, OpenAI)
        const modelSelect = document.getElementById('modelSelect');
        const customInput = document.getElementById('customModel');
        modelName = modelSelect?.value === 'custom' ? customInput?.value : modelSelect?.value;
        
        if (!modelName) {
            DataDialogue.showMessage('Please select a model or enter a custom model name');
            return;
        }
    }

    const formData = {
        // General
        agentType: agentType,
        // Source
        sourceType: document.getElementById('sourceType')?.value || 'postgresql',
        dbname: document.getElementById('dbname')?.value || '',
        username: document.getElementById('username')?.value || '',
        password: document.getElementById('password')?.value || '',
        host: document.getElementById('host')?.value || '',
        port: document.getElementById('port')?.value || '',
        // LLM Model
        modelProvider: modelProvider,
        repoID: repoID,
        modelFormat: modelProvider === 'huggingface' ? 'gguf' : '',
        modelName: modelName,
        token: document.getElementById('token')?.value || ''
    };

    // Validate required fields based on agent type
    if (agentType === 'SQL') {
        if (!formData.dbname || !formData.username || !formData.host || !formData.port) {
            DataDialogue.showMessage('Please fill in all required database fields');
            return;
        }
    }

    if (!modelName) {
        DataDialogue.showMessage('Please select or enter a model name');
        return;
    }

    if (modelProvider === 'huggingface' && !formData.repoID) {
        DataDialogue.showMessage('Please enter a repository ID');
        return;
    }

    DataDialogue.showFormLoadingAnimation(formData.agentType, formData.modelName);

    try {
        const response = await fetch('http://localhost:8000/api/v1/agents/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Form submitted successfully:', result);

        const agentName = `(${formData.agentType}) ${formData.modelName}`;
        DataDialogue.elements.dropdownButton.textContent = agentName;

        DataDialogue.hideFormLoadingAnimation();
        DataDialogue.resetRegisterForm();
        DataDialogue.closeRegisterForm();
    } catch (error) {
        console.error('Error submitting form:', error);
        DataDialogue.hideFormLoadingAnimation();
        DataDialogue.showMessage(`Error registering new Agent: ${error.message}`);
    }
};


DataDialogue.resetRegisterForm = () => {
    // Reset agent type and show/hide sections
    const agentType = document.getElementById('agentType');
    if (agentType) {
        agentType.value = '';
    }

    // Reset source configuration fields
    const sourceConfigFields = {
        'sourceType': 'postgresql', // default value
        'dbname': '',
        'username': '',
        'password': '',
        'host': '',
        'port': ''
    };

    Object.entries(sourceConfigFields).forEach(([id, defaultValue]) => {
        const element = document.getElementById(id);
        if (element) {
            element.value = defaultValue;
        }
    });

    // Reset model selections
    const modelFields = ['ModelProvider', 'modelSelect', 'repoSelect', 'variantSelect', 'token'];
    modelFields.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.value = '';
        }
    });

    // Reset custom model fields
    const customModelInput = document.getElementById('customModel');
    if (customModelInput) {
        customModelInput.value = '';
    }
    const customModelContainer = document.getElementById('customModelContainer');
    if (customModelContainer) {
        customModelContainer.style.display = 'none';
    }

    // Reset custom select display
    const customSelectTrigger = document.querySelector('.custom-select-trigger .selected-option');
    if (customSelectTrigger) {
        customSelectTrigger.innerHTML = 'Select provider...';
    }

    // Clear model icon
    const modelIcon = document.querySelector('.model-icon');
    if (modelIcon) {
        modelIcon.innerHTML = '';
    }

    // Hide sections that should be hidden initially
    const sectionsToHide = [
        'sourceConfigSection',
        'llmConfigSection',
        'modelSelectContainer',
        'tokenGroup'
    ];

    sectionsToHide.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.add('initially-hidden');
        }
    });

    // Clear any existing custom select
    const existingCustomSelect = document.querySelector('.custom-select-container');
    if (existingCustomSelect) {
        existingCustomSelect.remove();
    }
};

DataDialogue.closeRegisterForm = () => {
    const { formContainer, pageOverlay, menuIcon, tryDemoContainer } = DataDialogue.elements;
    if (formContainer) formContainer.classList.remove('show');
    if (pageOverlay) pageOverlay.style.display = 'none';
    document.body.style.overflow = 'auto';

    // Show menu icon and try demo button
    if (menuIcon) menuIcon.style.display = 'block';
    if (tryDemoContainer) tryDemoContainer.style.display = 'block';
};

DataDialogue.closeForm = () => {
    const { formContainer, pageOverlay, menuIcon, tryDemoContainer } = DataDialogue.elements;
    
    if (formContainer && pageOverlay) {
        const isFormShown = formContainer.classList.toggle('show');
        pageOverlay.style.display = isFormShown ? 'block' : 'none';
        document.body.style.overflow = isFormShown ? 'hidden' : 'auto';
        
        // Hide menu container
        DataDialogue.elements.menuContainer.classList.remove('active');

        // Hide or show menu icon and try demo button
        if (menuIcon) menuIcon.style.display = isFormShown ? 'none' : 'block';
        if (tryDemoContainer) tryDemoContainer.style.display = isFormShown ? 'none' : 'block';

        if (!isFormShown) {
            DataDialogue.clearFormFields();
        }
    }
};

DataDialogue.clearFormFields = () => {
    const sourceType = document.getElementById('sourceType');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    
    if (sourceType) sourceType.value = 'postgresql';
    if (username) username.value = '';
    if (password) password.value = '';
};
