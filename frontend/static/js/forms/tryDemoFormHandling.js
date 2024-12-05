DataDialogue.openDemoForm = () => {
    const { demoFormOverlay, demoFormContainer, menuIcon, tryDemoContainer } = DataDialogue.elements;

    if (demoFormOverlay && demoFormContainer) {
        // Reset form elements
        document.getElementById('demoModelSource').value = '';
        
        // Clear any existing custom select before reinitializing
        const existingCustomSelect = document.querySelector('.custom-select-container');
        if (existingCustomSelect) {
            existingCustomSelect.remove();
        }
        
        // Hide conditional elements
        const modelSelectContainer = document.getElementById('modelSelectContainer');
        const tokenGroup = document.getElementById('tokenGroup');
        
        if (modelSelectContainer) modelSelectContainer.classList.add('initially-hidden');
        if (tokenGroup) tokenGroup.classList.add('initially-hidden');
        
        // Initialize model selections - this now handles all the select creation logic
        DataDialogue.initializeModelSelections('demo');

        // Show the form
        demoFormOverlay.style.display = 'block';
        demoFormContainer.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Hide menu icon and try demo button
        if (menuIcon) menuIcon.style.display = 'none';
        if (tryDemoContainer) tryDemoContainer.style.display = 'none';
    }
};

DataDialogue.submitDemoForm = async () => {
    const modelSource = document.getElementById('demoModelSource').value;
    if (!modelSource) {
        DataDialogue.showMessage('Please select a model source');
        return;
    }

    const selectedConfig = DataDialogue.modelConfigs?.find(c => c.source_id === modelSource);
    let modelName = '';
    let repoID = '';
    
    if (selectedConfig?.options.some(opt => opt.repo_id)) {
        repoID = document.getElementById('demoRepoSelect')?.value;
        const variantSelect = document.getElementById('demoVariantSelect');
        const customInput = document.getElementById('demoCustomModel');
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
        const modelSelect = document.getElementById('demoModelSelect');
        const customInput = document.getElementById('demoCustomModel');
        modelName = modelSelect?.value === 'custom' ? customInput?.value : modelSelect?.value;
        
        if (!modelName) {
            DataDialogue.showMessage('Please select a model or enter a custom model name');
            return;
        }
    }

    const formData = {
        agentType: 'SQL',
        sourceType: 'postgresql',
        dbname: 'dvdrental',
        username: 'demo',
        password: '123456',
        host: 'localhost',
        port: '5432',
        modelSource: modelSource,
        modelName: modelName,
        repoID: repoID,
        token: document.getElementById('demoToken')?.value || '',
        modelFormat: modelSource === 'huggingface' ? 'gguf' : ''
    };

    DataDialogue.showFormLoadingAnimation(formData.agentType, formData.modelName);

    try {
        const response = await fetch('http://localhost:8000/api/v1/agents/register', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Demo form submitted successfully:', result);

        const agentName = `(${formData.agentType}) ${formData.modelName}`;
        DataDialogue.elements.dropdownButton.textContent = agentName;

        DataDialogue.hideFormLoadingAnimation();
        DataDialogue.resetDemoForm();
        DataDialogue.closeDemoForm();
        DataDialogue.showExampleSection();
    } catch (error) {
        console.error('Error submitting form:', error);
        DataDialogue.hideFormLoadingAnimation();
        DataDialogue.showMessage(`Error registering Demo Agent: ${error.message}`);
    }
};

DataDialogue.resetDemoForm = () => {
    // Reset model source
    const demoModelSource = document.getElementById('demoModelSource');
    if (demoModelSource) {
        demoModelSource.value = '';
    }

    // Reset token
    const tokenInput = document.getElementById('demoToken');
    if (tokenInput) {
        tokenInput.value = '';
    }

    // Reset model select container and its contents
    const modelSelectContainer = document.getElementById('demoModelSelectContainer');
    if (modelSelectContainer) {
        modelSelectContainer.innerHTML = ''; // Clear all dynamic content
        modelSelectContainer.classList.add('initially-hidden');
    }

    // Explicitly reset all possible model-related fields
    const fieldsToReset = [
        'demoModelSelect',
        'demoRepoSelect',
        'demoVariantSelect',
        'demoCustomModel'
    ];

    fieldsToReset.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = '';
        }
    });

    // Reset custom model container if it exists
    const customModelContainer = document.getElementById('demoCustomModelContainer');
    if (customModelContainer) {
        customModelContainer.style.display = 'none';
    }

    // Hide tokenGroup
    const tokenGroup = document.getElementById('tokenGroup');
    if (tokenGroup) {
        tokenGroup.classList.add('initially-hidden');
    }

    // Reset custom select display
    const customSelectTrigger = document.querySelector('.custom-select-trigger .selected-option');
    if (customSelectTrigger) {
        customSelectTrigger.innerHTML = 'Select source...';
    }

    // Clear model icon
    const modelIcon = document.querySelector('.model-icon');
    if (modelIcon) {
        modelIcon.innerHTML = '';
    }

    // Force a reflow to ensure all changes take effect
    if (modelSelectContainer) {
        modelSelectContainer.offsetHeight;
    }
};

DataDialogue.closeDemoForm = () => {
    const { demoFormContainer, demoFormOverlay, menuIcon, tryDemoContainer } = DataDialogue.elements;
    if (demoFormContainer) demoFormContainer.classList.remove('show');
    if (demoFormOverlay) demoFormOverlay.style.display = 'none';
    document.body.style.overflow = 'auto';
    
    // Show menu icon and try demo button
    if (menuIcon) menuIcon.style.display = 'block';
    if (tryDemoContainer) tryDemoContainer.style.display = 'block';
};
