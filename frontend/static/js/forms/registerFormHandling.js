DataDialogue.handleModelSourceChange = (formPrefix = '') => {
    const modelSource = document.getElementById(`${formPrefix}ModelSource`);
    if (!modelSource) return;

    const repoIdGroup = document.getElementById('repoIdGroup');
    const tokenGroup = document.getElementById('tokenGroup');
    const googleModels = document.getElementById('googleModels');
    const openaiModels = document.getElementById('openaiModels');
    const huggingfaceModels = document.getElementById('huggingfaceModels');
    
    // First hide all model-related fields
    [repoIdGroup, tokenGroup, googleModels, openaiModels, huggingfaceModels].forEach(el => {
        if (el) el.classList.add('initially-hidden');
    });
    
    // Show appropriate fields based on model source
    if (modelSource.value === 'google') {
        googleModels?.classList.remove('initially-hidden');
        tokenGroup?.classList.remove('initially-hidden');
    } else if (modelSource.value === 'openai') {
        openaiModels?.classList.remove('initially-hidden');
        tokenGroup?.classList.remove('initially-hidden');
    } else if (modelSource.value === 'huggingface') {
        huggingfaceModels?.classList.remove('initially-hidden');
        repoIdGroup?.classList.remove('initially-hidden');
        tokenGroup?.classList.remove('initially-hidden');
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
        
        // Initialize model source icons and custom select
        DataDialogue.initializeCustomSelect('');
        
        // Add model selection change handlers
        document.getElementById('googleModelName')?.addEventListener('change', function() {
            const customDiv = document.getElementById('googleCustomDiv');
            if (this.value === 'custom') {
                customDiv?.classList.remove('initially-hidden');
            } else {
                customDiv?.classList.add('initially-hidden');
            }
        });
        
        document.getElementById('openaiModelName')?.addEventListener('change', function() {
            const customDiv = document.getElementById('openaiCustomDiv');
            if (this.value === 'custom') {
                customDiv?.classList.remove('initially-hidden');
            } else {
                customDiv?.classList.add('initially-hidden');
            }
        });
        
        document.getElementById('huggingfaceModelName')?.addEventListener('change', function() {
            const customDiv = document.getElementById('huggingfaceCustomDiv');
            if (this.value === 'custom') {
                customDiv?.classList.remove('initially-hidden');
            } else {
                customDiv?.classList.add('initially-hidden');
            }
        });

        // Add event listener for model source changes
        const modelSource = document.getElementById('ModelSource');
        if (modelSource) {
            modelSource.addEventListener('change', () => DataDialogue.handleModelSourceChange(''));
        }
        
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

DataDialogue.resetRegisterForm = () => {
    // Reset all form fields
    const fieldsToReset = {
        'agentType': '',
        'ModelSource': '',
        'googleModelName': '',
        'openaiModelName': '',
        'huggingfaceModelName': '',
        'googleCustomModel': '',
        'openaiCustomModel': '',
        'huggingfaceCustomModel': '',
        'repoId': '',
        'token': '',
        'sourceType': 'postgresql',
        'dbname': '',
        'username': '',
        'password': '',
        'host': '',
        'port': ''
    };

    Object.entries(fieldsToReset).forEach(([id, defaultValue]) => {
        const element = document.getElementById(id);
        if (element) {
            element.value = defaultValue;
        }
    });

    // Hide conditional sections
    const sectionsToHide = [
        'sourceConfigSection',
        'llmConfigSection',
        'googleModels',
        'openaiModels',
        'huggingfaceModels',
        'googleCustomDiv',
        'openaiCustomDiv',
        'huggingfaceCustomDiv',
        'repoIdGroup',
        'tokenGroup'
    ];

    sectionsToHide.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.add('initially-hidden');
        }
    });

    // Reset the custom select if it exists
    const customSelect = document.querySelector('.custom-select-container');
    if (customSelect) {
        const selectedOption = customSelect.querySelector('.selected-option');
        if (selectedOption) {
            selectedOption.innerHTML = 'Select source...';
        }
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


DataDialogue.submitForm = async () => {
    const agentType = document.getElementById('agentType')?.value;
    const modelSource = document.getElementById('ModelSource')?.value;
    
    if (!agentType) {
        DataDialogue.showMessage('Please select an agent type');
        return;
    }

    if (!modelSource) {
        DataDialogue.showMessage('Please select a model source');
        return;
    }

    // Get the selected model name based on the model source
    let modelName = '';
    let repoID = '';
    
    if (modelSource === 'google') {
        const googleModel = document.getElementById('googleModelName')?.value;
        modelName = googleModel === 'custom' ? 
            document.getElementById('googleCustomModel')?.value : 
            googleModel;
    } else if (modelSource === 'openai') {
        const openaiModel = document.getElementById('openaiModelName')?.value;
        modelName = openaiModel === 'custom' ? 
            document.getElementById('openaiCustomModel')?.value : 
            openaiModel;
    } else if (modelSource === 'huggingface') {
        const huggingfaceModel = document.getElementById('huggingfaceModelName')?.value;
        modelName = huggingfaceModel === 'custom' ? 
            document.getElementById('huggingfaceCustomModel')?.value : 
            huggingfaceModel;
        repoID = document.getElementById('repoId')?.value || '';
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
        modelSource: modelSource,
        repoID: repoID,
        modelFormat: modelSource === 'huggingface' ? 'gguf' : '',
        modelName: modelName,
        token: document.getElementById('token')?.value || ''
    };

    // Validate required fields based on agent type and model source
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

    if (modelSource === 'huggingface' && !formData.repoID) {
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


DataDialogue.toggleForm = () => {
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
