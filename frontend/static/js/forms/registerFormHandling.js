DataDialogue.handleModelSourceChange = (formPrefix = '') => {
    const modelSource = document.getElementById(`${formPrefix}ModelSource`).value;
    const repoIdGroup = document.getElementById(`${formPrefix}RepoIdGroup`);
    const modelNameGroup = document.getElementById(`${formPrefix}ModelNameGroup`);
    const tokenGroup = document.getElementById(`${formPrefix}TokenGroup`);
    
    // First hide all model-related fields
    repoIdGroup?.classList.add('initially-hidden');
    modelNameGroup?.classList.add('initially-hidden');
    tokenGroup?.classList.add('initially-hidden');
    
    // Show appropriate fields based on model source
    if (modelSource === 'huggingface') {
        repoIdGroup?.classList.remove('initially-hidden');
        modelNameGroup?.classList.remove('initially-hidden');
        tokenGroup?.classList.remove('initially-hidden');
    } else if (modelSource === 'google') {
        modelNameGroup?.classList.remove('initially-hidden');
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
        const modelSource = document.getElementById('modelSource');
        
        if (agentTypeSelect) {
            agentTypeSelect.value = '';
            DataDialogue.handleAgentTypeChange(); // This will hide the sections
        }
        
        // Add handler for model source changes
        if (modelSource) {
            // Remove existing listener to prevent duplicates
            modelSource.removeEventListener('change', DataDialogue.handleModelSourceChange);
            // Add new listener
            modelSource.addEventListener('change', () => {
                const modelSource = document.getElementById('modelSource').value;
                const repoIdGroup = document.getElementById('repoIdGroup');
                const modelNameGroup = document.getElementById('modelNameGroup');
                const tokenGroup = document.getElementById('tokenGroup');
                
                // First hide all model-related fields
                repoIdGroup.classList.add('initially-hidden');
                modelNameGroup.classList.add('initially-hidden');
                tokenGroup.classList.add('initially-hidden');
                
                // Show appropriate fields based on model source
                if (modelSource === 'huggingface') {
                    repoIdGroup.classList.remove('initially-hidden');
                    modelNameGroup.classList.remove('initially-hidden');
                    tokenGroup.classList.remove('initially-hidden');
                } else if (modelSource === 'google') {
                    modelNameGroup.classList.remove('initially-hidden');
                    tokenGroup.classList.remove('initially-hidden');
                }
            });
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
    const agentType = document.getElementById('agentType').value;
    const modelSource = document.getElementById('modelSource').value;
    
    if (!agentType) {
        alert('Please select an agent type');
        return;
    }

    if (!modelSource) {
        alert('Please select a model source');
        return;
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
        repoID: document.getElementById('repoId')?.value || '',
        modelFormat: document.getElementById('ModelFormat')?.value || '', // e.g gguf
        modelName: document.getElementById('modelName')?.value || '',
        token: document.getElementById('token')?.value || ''
    };

    // Validate required fields based on agent type and model source
    if (agentType === 'SQL') {
        if (!formData.dbname || !formData.username || !formData.host || !formData.port) {
            alert('Please fill in all required database fields');
            return;
        }
    }
    
    if (!formData.modelName) {
        alert('Please enter a model name');
        return;
    }

    if (modelSource === 'huggingface' && !formData.repoID) {
        alert('Please enter a repository ID');
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

        // Update dropdown with new agent
        // NOTE: The naming convention should be consistent with backend
        const agentName = `(${formData.agentType}) ${formData.modelName}`;
        DataDialogue.elements.dropdownButton.textContent = agentName;

        DataDialogue.hideFormLoadingAnimation();
        DataDialogue.resetRegisterForm();
        DataDialogue.closeRegisterForm();
    } catch (error) {
        console.error('Error submitting form:', error);
        const loadingMessage = document.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.textContent = `Error registering new Agent: ${error.message}`;
        }
        setTimeout(DataDialogue.hideFormLoadingAnimation, 2000);
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
