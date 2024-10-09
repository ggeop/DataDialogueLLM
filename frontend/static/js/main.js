// Create a global object to store our app's functions and variables
window.DataDialogue = window.DataDialogue || {};

// Main initialization function
DataDialogue.init = () => {
    console.log('Initializing Data Dialogue');
    DataDialogue.cacheElements();
    DataDialogue.attachEventListeners();
    DataDialogue.renderExampleSection();
    console.log('Data Dialogue initialized successfully');
};

// Cache DOM elements
DataDialogue.cacheElements = () => {
    DataDialogue.elements = {
        queryInput: document.getElementById('queryInput'),
        askButton: document.getElementById('askButton'),
        modelSelect: document.getElementById('modelSelect'),
        conversationsDiv: document.getElementById('conversations'),
        loadingIndicator: document.getElementById('loadingIndicator'),
        menuIcon: document.querySelector('.menu-icon'),
        menuContainer: document.querySelector('.menu-container'),
        cancelCloseBtn: document.querySelector('.cancel-close-btn'),
        pageOverlay: document.getElementById('pageOverlay'),
        formContainer: document.getElementById('formContainer')
    };
};

// Attach event listeners
DataDialogue.attachEventListeners = () => {
    const { askButton, queryInput, menuIcon, cancelCloseBtn, pageOverlay } = DataDialogue.elements;

    if (askButton) askButton.addEventListener('click', DataDialogue.handleSubmit);
    if (queryInput) queryInput.addEventListener('keypress', DataDialogue.handleEnterKey);
    if (menuIcon) menuIcon.addEventListener('click', DataDialogue.toggleMenu);
    if (cancelCloseBtn) cancelCloseBtn.addEventListener('click', DataDialogue.toggleForm);
    if (pageOverlay) pageOverlay.addEventListener('click', DataDialogue.handleOverlayClick);

    document.addEventListener('click', DataDialogue.handleOutsideClick);
};

// Event handler functions
DataDialogue.handleSubmit = () => {
    const query = DataDialogue.elements.queryInput.value.trim();
    const model = DataDialogue.elements.modelSelect.value;
    if (query === '') return;

    DataDialogue.addMessageToConversation('user-message', query);
    DataDialogue.elements.queryInput.value = '';
    DataDialogue.showLoadingAnimation();
    DataDialogue.submitQuery(query, model);
};

DataDialogue.handleEnterKey = (e) => {
    if (e.key === 'Enter') DataDialogue.handleSubmit();
};

DataDialogue.toggleMenu = () => {
    DataDialogue.elements.menuContainer.classList.toggle('active');
};

DataDialogue.handleOutsideClick = (event) => {
    const { menuContainer, menuIcon } = DataDialogue.elements;
    if (menuContainer && !menuContainer.contains(event.target) && !menuIcon.contains(event.target)) {
        menuContainer.classList.remove('active');
    }
};

DataDialogue.handleOverlayClick = function(event) {
    if (event.target === DataDialogue.elements.pageOverlay) {
        DataDialogue.toggleForm();
    }
};

// Form handling functions
DataDialogue.toggleForm = () => {
    const { formContainer, pageOverlay } = DataDialogue.elements;
    
    if (formContainer && pageOverlay) {
        formContainer.classList.toggle('show');
        pageOverlay.style.display = formContainer.classList.contains('show') ? 'block' : 'none';
        document.body.style.overflow = formContainer.classList.contains('show') ? 'hidden' : 'auto';
        
        DataDialogue.elements.menuContainer.classList.remove('active');

        if (!formContainer.classList.contains('show')) {
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

// Loading animation functions
DataDialogue.showLoadingAnimation = (sourceType) => {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        const loadingMessage = loadingOverlay.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.innerHTML = `Connecting to ${sourceType}.<br>Embedding database schema`;
        }
        loadingOverlay.classList.add('show');
    }
};

DataDialogue.hideLoadingAnimation = () => {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('show');
    }
};

// Form submission function
DataDialogue.submitForm = async () => {
    const formData = {
        sourceType: document.getElementById('sourceType').value,
        dbname: document.getElementById('dbname').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        host: document.getElementById('host').value,
        port: document.getElementById('port').value
    };

    DataDialogue.showLoadingAnimation(formData.sourceType);

    try {
        const response = await fetch('http://localhost:8000/agents/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const result = await response.json();
        console.log('Form submitted successfully:', result);

        DataDialogue.hideLoadingAnimation();
        DataDialogue.toggleForm();
    } catch (error) {
        console.error('Error submitting form:', error);
        const loadingMessage = document.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.textContent = "Error connecting to database. Please try again.";
        }
        setTimeout(DataDialogue.hideLoadingAnimation, 2000);
    }
};

// Initialize when components are ready
function initializeWhenReady() {
    console.log('Main.js: Checking if components are loaded');
    if (window.DataDialogue.componentsLoaded) {
        console.log('Main.js: Components are loaded, initializing');
        DataDialogue.init();
    } else {
        console.log('Main.js: Components not loaded yet, waiting');
        window.addEventListener('componentsLoaded', () => {
            console.log('Main.js: Received componentsLoaded event, initializing');
            DataDialogue.init();
        }, { once: true });
    }
}

// Attach the initializer to DOMContentLoaded event
document.addEventListener('DOMContentLoaded', initializeWhenReady);

// Make necessary functions globally accessible
window.DataDialogue = DataDialogue;
window.toggleForm = DataDialogue.toggleForm;
window.submitForm = DataDialogue.submitForm;