// Create a global object to store our app's functions and variables
window.DataDialogue = window.DataDialogue || {};

// Main initialization function
DataDialogue.init = () => {
    console.log('Initializing Data Dialogue');
    DataDialogue.cacheElements();
    DataDialogue.initConfirmDialog();
    DataDialogue.attachEventListeners();
    DataDialogue.renderExampleSection();
    DataDialogue.fetchAgentList();
    DataDialogue.hideExampleSection();
    DataDialogue.initializeMessageSystem();
    console.log('Data Dialogue initialized successfully');
};

// Cache DOM elements
DataDialogue.cacheElements = () => {
    DataDialogue.elements = {
        queryInput: document.getElementById('queryInput'),
        visibleInput: document.getElementById('visibleInput'),
        askButton: document.getElementById('askButton'),
        modelSelect: document.getElementById('modelSelect'),
        customDropdown: document.getElementById('customDropdown'),
        dropdownButton: document.getElementById('dropdownButton'),
        dropdownList: document.getElementById('dropdownList'),
        conversationsDiv: document.getElementById('conversations'),
        loadingIndicator: document.getElementById('loadingIndicator'),
        menuIcon: document.querySelector('.menu-icon'),
        menuContainer: document.querySelector('.menu-container'),
        cancelCloseBtn: document.querySelector('.cancel-close-btn'),
        pageOverlay: document.getElementById('pageOverlay'),
        formContainer: document.getElementById('formContainer'),
        tryDemoButton: document.getElementById('tryDemoButton'),
        tryDemoContainer: document.getElementById('try-demo-container'),
        messageBox: document.getElementById('messageBox'),
        demoFormOverlay: document.getElementById('demoFormOverlay'),
        demoFormContainer: document.getElementById('demoFormContainer')
    };
};

DataDialogue.isFetching = false;
DataDialogue.isDropdownOpen = false;

// Attach event listeners
DataDialogue.attachEventListeners = () => {
    const { askButton, queryInput, menuIcon, cancelCloseBtn, pageOverlay, dropdownButton, dropdownList, tryDemoButton } = DataDialogue.elements;

    if (askButton) askButton.addEventListener('click', DataDialogue.handleSubmit);
    if (queryInput) queryInput.addEventListener('keypress', DataDialogue.handleEnterKey);
    if (visibleInput) {
        visibleInput.addEventListener('input', DataDialogue.syncInputs);
        visibleInput.addEventListener('keypress', DataDialogue.handleEnterKey);
    }
    if (menuIcon) menuIcon.addEventListener('click', DataDialogue.toggleMenu);
    if (cancelCloseBtn) cancelCloseBtn.addEventListener('click', DataDialogue.toggleForm);
    if (pageOverlay) pageOverlay.addEventListener('click', DataDialogue.handleOverlayClick);
    if (dropdownButton) dropdownButton.addEventListener('click', DataDialogue.toggleDropdown);
    if (dropdownList) dropdownList.addEventListener('click', DataDialogue.handleOptionClick);
    if (tryDemoButton) tryDemoButton.addEventListener('click', DataDialogue.handleTryDemo);

    // Global event handlers
    document.addEventListener('click', DataDialogue.handleOutsideClick);
    document.addEventListener('click', DataDialogue.closeDropdownOutside);
};

DataDialogue.handleEnterKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Prevent default to avoid newline in textarea
        DataDialogue.handleSubmit();
    }
};

// Add this new function
DataDialogue.syncInputs = () => {
    const { queryInput, visibleInput } = DataDialogue.elements;
    queryInput.value = visibleInput.value;
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