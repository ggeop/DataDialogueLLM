DataDialogue.handleTryDemo = () => {
    DataDialogue.openDemoForm();
};

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
        
        // Hide all conditional elements using your CSS class
        const elementsToHide = [
            'googleModels',
            'huggingfaceModels',
            'googleCustomDiv',
            'huggingfaceCustomDiv',
            'tokenGroup'
        ];
        
        elementsToHide.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.classList.add('initially-hidden');
            }
        });

        DataDialogue.initializeCustomSelect('demo');

        // Show the form
        demoFormOverlay.style.display = 'block';
        demoFormContainer.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Hide menu icon and try demo button
        if (menuIcon) menuIcon.style.display = 'none';
        if (tryDemoContainer) tryDemoContainer.style.display = 'none';

        // Set up event listeners
        setupFormListeners();
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

function setupFormListeners() {
    // Model source change handler
    const demoModelSource = document.getElementById('demoModelSource');
    if (demoModelSource) {
        demoModelSource.addEventListener('change', function() {
            const googleModels = document.getElementById('googleModels');
            const huggingfaceModels = document.getElementById('huggingfaceModels');
            const repoIdGroup = document.getElementById('demoRepoIdGroup');
            const tokenGroup = document.getElementById('tokenGroup');
            
            // Reset and hide all model sections
            [googleModels, huggingfaceModels, repoIdGroup].forEach(el => {
                if (el) el.classList.add('initially-hidden');
            });
            
            // Reset custom inputs
            document.getElementById('googleCustomDiv')?.classList.add('initially-hidden');
            document.getElementById('huggingfaceCustomDiv')?.classList.add('initially-hidden');

            // Show relevant sections
            if (this.value === 'google') {
                googleModels?.classList.remove('initially-hidden');
                tokenGroup?.classList.remove('initially-hidden');
            } else if (this.value === 'huggingface') {
                huggingfaceModels?.classList.remove('initially-hidden');
                repoIdGroup?.classList.remove('initially-hidden');
                tokenGroup?.classList.remove('initially-hidden');
            }
        });
    }

    // Google model change handler
    document.getElementById('googleModelName').addEventListener('change', function() {
        const customDiv = document.getElementById('googleCustomDiv');
        if (this.value === 'custom') {
            customDiv?.classList.remove('initially-hidden');
        } else {
            customDiv?.classList.add('initially-hidden');
        }
    });

    // Hugging Face model change handler
    document.getElementById('huggingfaceModelName').addEventListener('change', function() {
        const customDiv = document.getElementById('huggingfaceCustomDiv');
        if (this.value === 'custom') {
            customDiv?.classList.remove('initially-hidden');
        } else {
            customDiv?.classList.add('initially-hidden');
        }
    });
}

DataDialogue.submitDemoForm = async () => {
    const modelSource = document.getElementById('demoModelSource').value;
    if (!modelSource) {
        DataDialogue.showMessage('Please select a model source');
        return;
    }

    let modelName = '';
    let repoID = '';
    if (modelSource === 'google') {
        const googleModel = document.getElementById('googleModelName').value;
        modelName = googleModel === 'custom' ? 
            document.getElementById('googleCustomModel').value : 
            googleModel;
    } else {
        const huggingfaceModel = document.getElementById('huggingfaceModelName').value;
        modelName = huggingfaceModel === 'custom' ? 
            document.getElementById('huggingfaceCustomModel').value : 
            huggingfaceModel;
        repoID = document.getElementById('demoRepoId').value;
        
        if (!repoID) {
            DataDialogue.showMessage('Please enter a repository ID');
            return;
        }
    }

    if (!modelName) {
        DataDialogue.showMessage('Please select or enter a model name');
        return;
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
    // Reset model source and related fields
    const modelFields = {
        'demoModelSource': '',
        'demoRepoId': '',
        'demoToken': '',
        'googleModelName': '',
        'huggingfaceModelName': '',
        'googleCustomModel': '',
        'huggingfaceCustomModel': ''
    };

    Object.entries(modelFields).forEach(([id, defaultValue]) => {
        const element = document.getElementById(id);
        if (element) {
            element.value = defaultValue;
        }
    });

    // Hide conditional sections
    const sectionsToHide = [
        'googleModels',
        'huggingfaceModels',
        'googleCustomDiv',
        'huggingfaceCustomDiv',
        'demoRepoIdGroup',
        'tokenGroup'
    ];

    sectionsToHide.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.add('initially-hidden');
        }
    });
};
