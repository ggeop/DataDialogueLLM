
///////////////////////////////////////////
// Common
///////////////////////////////////////////
DataDialogue.showFormLoadingAnimation = (sourceType) => {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        const loadingMessage = loadingOverlay.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.innerHTML = `Connecting to ${sourceType}.<br>Adding database schema in SQLAgent context`;
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



///////////////////////////////////////////
// Demo Form
///////////////////////////////////////////
DataDialogue.handleTryDemo = () => {
    DataDialogue.openDemoForm();
};

DataDialogue.openDemoForm = () => {
    const { demoFormOverlay, demoFormContainer, menuIcon, tryDemoContainer } = DataDialogue.elements;

    if (demoFormOverlay && demoFormContainer) {
        demoFormOverlay.style.display = 'block';
        demoFormContainer.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Hide menu icon and try demo button
        if (menuIcon) menuIcon.style.display = 'none';
        if (tryDemoContainer) tryDemoContainer.style.display = 'none';
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

DataDialogue.submitDemoForm = async () => {
    const formData = {
        // General
        modelType: document.getElementById('demoModelType').value,
        // Source
        sourceType: document.getElementById('demoSourceType').value,
        dbname: document.getElementById('demoDbname').value,
        username: document.getElementById('demoUsername').value,
        password: document.getElementById('demoPassword').value,
        host: document.getElementById('demoHost').value,
        port: document.getElementById('demoPort').value,
        // LLM Model
        modelSource: "huggingface",
        repoID : document.getElementById('demoRepoId').value,
        modelFormat: "gguf",
        modelName: document.getElementById('demoModelName').value,
        token: document.getElementById('demoToken').value
    };

    DataDialogue.showFormLoadingAnimation(formData.sourceType);

    try {
        const response = await fetch('http://localhost:8000/api/v1/agents/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const result = await response.json();
        console.log('Demo form submitted successfully:', result);

        DataDialogue.hideFormLoadingAnimation();
        DataDialogue.closeDemoForm();
        DataDialogue.showExampleSection();  // Add this line to show examples after successful submission
    } catch (error) {
        console.error('Error submitting demo form:', error);
        const loadingMessage = document.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.textContent = "Error connecting to demo database. Please try again.";
        }
        setTimeout(DataDialogue.hideFormLoadingAnimation, 2000);
    }
};



///////////////////////////////////////////
// Register Form
///////////////////////////////////////////
DataDialogue.openRegisterForm = () => {
    const { formContainer, pageOverlay, menuIcon, tryDemoContainer } = DataDialogue.elements;
    
    if (formContainer && pageOverlay) {
        formContainer.classList.add('show');
        pageOverlay.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // Hide menu icon and try demo button
        if (menuIcon) menuIcon.style.display = 'none';
        if (tryDemoContainer) tryDemoContainer.style.display = 'none';
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
    const formData = {
        // General
        modelType: document.getElementById('modelType').value,
        // Source
        sourceType: document.getElementById('sourceType').value,
        dbname: document.getElementById('dbname').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        host: document.getElementById('host').value,
        port: document.getElementById('port').value,
        // LLM Model
        modelSource: "huggingface",
        repoID: document.getElementById('repoId').value,
        modelFormat: "gguf",
        modelName: document.getElementById('modelName').value,
        token: document.getElementById('token').value
    };

    DataDialogue.showFormLoadingAnimation(formData.sourceType);

    try {
        const response = await fetch('http://localhost:8000/api/v1/agents/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const result = await response.json();
        console.log('Form submitted successfully:', result);

        DataDialogue.hideFormLoadingAnimation();
        DataDialogue.toggleForm();
    } catch (error) {
        console.error('Error submitting form:', error);
        const loadingMessage = document.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.textContent = "Error connecting to database. Please try again.";
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
