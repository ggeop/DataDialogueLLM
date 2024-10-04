// Create a global object to store our app's functions and variables
window.DataDialogue = window.DataDialogue || {};

document.addEventListener('DOMContentLoaded', () => {
    // Initialize the application
    DataDialogue.init();
});

DataDialogue.init = () => {
    const queryInput = document.getElementById('queryInput');
    const askButton = document.getElementById('askButton');
    const conversationsDiv = document.getElementById('conversations');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const menuIcon = document.querySelector('.menu-icon');
    const menuContainer = document.querySelector('.menu-container');

    // Store these elements in the DataDialogue object so they're accessible in other files
    DataDialogue.elements = {
        queryInput,
        askButton,
        conversationsDiv,
        loadingIndicator,
        menuIcon,
        menuContainer
    };

    // Set up event listeners
    askButton.addEventListener('click', DataDialogue.handleSubmit);
    queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            DataDialogue.handleSubmit();
        }
    });

    menuIcon.addEventListener('click', toggleMenu);

    document.addEventListener('click', (event) => {
        if (!menuContainer.contains(event.target) && !menuIcon.contains(event.target)) {
            closeMenu();
        }
    });

    // Render the ExampleSection component
    DataDialogue.renderExampleSection();

    console.log('Data Dialogue initialized successfully');
};

DataDialogue.handleSubmit = () => {
    const query = DataDialogue.elements.queryInput.value.trim();
    if (query === '') return;

    DataDialogue.addMessageToConversation('user-message', query);
    DataDialogue.elements.queryInput.value = '';
    DataDialogue.showLoadingAnimation();
    DataDialogue.submitQuery(query);
};

function toggleMenu() {
    const menuContainer = document.querySelector('.menu-container');
    menuContainer.classList.toggle('active');
}

function closeMenu() {
    const menuContainer = document.querySelector('.menu-container');
    menuContainer.classList.remove('active');
}

// Make sure copyToClipboard is available globally
window.copyToClipboard = DataDialogue.copyToClipboard;