DataDialogue.handleTryDemo = () => {
    DataDialogue.openDemoForm();
};

DataDialogue.openDemoForm = () => {
    const demoFormOverlay = document.getElementById('demoFormOverlay');
    const demoFormContainer = document.getElementById('demoFormContainer');

    demoFormOverlay.style.display = 'block';
    demoFormContainer.classList.add('show');
    document.body.style.overflow = 'hidden';
};

DataDialogue.closeDemoForm = () => {
    const demoFormOverlay = document.getElementById('demoFormOverlay');
    const demoFormContainer = document.getElementById('demoFormContainer');

    demoFormOverlay.style.display = 'none';
    demoFormContainer.classList.remove('show');
    document.body.style.overflow = 'auto';
};

DataDialogue.submitDemoForm = async () => {
    const formData = {
        sourceType: document.getElementById('demoSourceType').value,
        dbname: document.getElementById('demoDbname').value,
        username: document.getElementById('demoUsername').value,
        password: document.getElementById('demoPassword').value,
        host: document.getElementById('demoHost').value,
        port: document.getElementById('demoPort').value
    };

    DataDialogue.showFormLoadingAnimation(formData.sourceType);

    try {
        const response = await fetch('http://localhost:8000/agents/register', {
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

DataDialogue.toggleForm = () => {
    const { formContainer, pageOverlay, menuIcon } = DataDialogue.elements;
    
    if (formContainer && pageOverlay && menuIcon) {
        const isFormShown = formContainer.classList.toggle('show');
        pageOverlay.style.display = isFormShown ? 'block' : 'none';
        document.body.style.overflow = isFormShown ? 'hidden' : 'auto';
        
        // Hide menu container
        DataDialogue.elements.menuContainer.classList.remove('active');

        // Hide menu icon when form is shown, show it when form is hidden
        menuIcon.style.display = isFormShown ? 'none' : 'block';

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

DataDialogue.submitForm = async () => {
    const formData = {
        sourceType: document.getElementById('sourceType').value,
        dbname: document.getElementById('dbname').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        host: document.getElementById('host').value,
        port: document.getElementById('port').value
    };

    DataDialogue.showFormLoadingAnimation(formData.sourceType);

    try {
        const response = await fetch('http://localhost:8000/agents/register', {
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

DataDialogue.handleOverlayClick = function(event) {
    if (event.target === DataDialogue.elements.pageOverlay) {
        DataDialogue.toggleForm();
    }
};



