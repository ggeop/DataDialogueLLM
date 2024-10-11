// Create a global object to store our app's functions and variables
window.DataDialogue = window.DataDialogue || {};

// Main initialization function
DataDialogue.init = () => {
    console.log('Initializing Data Dialogue');
    DataDialogue.cacheElements();
    DataDialogue.attachEventListeners();
    DataDialogue.renderExampleSection();
    DataDialogue.fetchAgentList();
    DataDialogue.hideExampleSection();
    console.log('Data Dialogue initialized successfully');
};

// Cache DOM elements
DataDialogue.cacheElements = () => {
    DataDialogue.elements = {
        queryInput: document.getElementById('queryInput'),
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
        messageBox: document.getElementById('messageBox')
    };
};

DataDialogue.isFetching = false;
DataDialogue.isDropdownOpen = false;

// Attach event listeners
DataDialogue.attachEventListeners = () => {
    const { askButton, queryInput, menuIcon, cancelCloseBtn, pageOverlay, dropdownButton, dropdownList, tryDemoButton } = DataDialogue.elements;

    if (askButton) askButton.addEventListener('click', DataDialogue.handleSubmit);
    if (queryInput) queryInput.addEventListener('keypress', DataDialogue.handleEnterKey);
    if (menuIcon) menuIcon.addEventListener('click', DataDialogue.toggleMenu);
    if (cancelCloseBtn) cancelCloseBtn.addEventListener('click', DataDialogue.toggleForm);
    if (pageOverlay) pageOverlay.addEventListener('click', DataDialogue.handleOverlayClick);
    if (dropdownButton) dropdownButton.addEventListener('click', DataDialogue.toggleDropdown);
    if (dropdownList) dropdownList.addEventListener('click', DataDialogue.handleOptionClick);
    if (tryDemoButton) tryDemoButton.addEventListener('click', DataDialogue.handleTryDemo);

    document.addEventListener('click', DataDialogue.closeDropdownOutside);
};


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

    DataDialogue.showLoadingAnimation(formData.sourceType);

    try {
        const response = await fetch('http://localhost:8000/agents/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const result = await response.json();
        console.log('Demo form submitted successfully:', result);

        DataDialogue.hideLoadingAnimation();
        DataDialogue.closeDemoForm();
        DataDialogue.showExampleSection();  // Add this line to show examples after successful submission
    } catch (error) {
        console.error('Error submitting demo form:', error);
        const loadingMessage = document.querySelector('.loading-message');
        if (loadingMessage) {
            loadingMessage.textContent = "Error connecting to demo database. Please try again.";
        }
        setTimeout(DataDialogue.hideLoadingAnimation, 2000);
    }
};


DataDialogue.toggleDropdown = async (event) => {
    event.stopPropagation();
    if (!DataDialogue.isDropdownOpen) {
        await DataDialogue.openDropdown();
    } else {
        DataDialogue.closeDropdown();
    }
};

DataDialogue.openDropdown = async () => {
    if (DataDialogue.isFetching) return;
    
    DataDialogue.isFetching = true;
    DataDialogue.elements.dropdownButton.textContent = 'Loading...';
    DataDialogue.elements.customDropdown.classList.add('open');
    
    try {
        await DataDialogue.fetchAgentList();
        DataDialogue.elements.dropdownList.classList.add('show');
        DataDialogue.isDropdownOpen = true;
    } catch (error) {
        console.error('Error fetching agent list:', error);
        DataDialogue.elements.dropdownButton.textContent = 'Error loading agents';
    } finally {
        DataDialogue.isFetching = false;
    }
};

DataDialogue.closeDropdown = () => {
    DataDialogue.elements.dropdownList.classList.remove('show');
    DataDialogue.elements.customDropdown.classList.remove('open');
    DataDialogue.isDropdownOpen = false;
};

DataDialogue.handleOptionClick = (event) => {
    if (event.target.tagName === 'LI') {
        DataDialogue.elements.dropdownButton.textContent = event.target.textContent;
        DataDialogue.elements.dropdownList.querySelectorAll('li').forEach(li => li.classList.remove('selected'));
        event.target.classList.add('selected');
        DataDialogue.closeDropdown();
    }
};

DataDialogue.closeDropdownOutside = (event) => {
    if (DataDialogue.isDropdownOpen && !DataDialogue.elements.customDropdown.contains(event.target)) {
        DataDialogue.closeDropdown();
    }
};

DataDialogue.fetchAgentList = async () => {
    try {
        const response = await fetch('http://localhost:8000/agents/list');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const agents = await response.json();
        DataDialogue.populateAgentList(agents);
    } catch (error) {
        console.error('Error fetching agent list:', error);
        DataDialogue.elements.dropdownButton.textContent = 'Error loading agents';
    }
};

DataDialogue.populateAgentList = (agents) => {
    const { dropdownList, dropdownButton } = DataDialogue.elements;
    dropdownList.innerHTML = ''; // Clear existing options

    agents.forEach(agent => {
        const option = document.createElement('li');
        option.textContent = agent;
        dropdownList.appendChild(option);
    });

    if (agents.length > 0) {
        dropdownButton.textContent = agents[0]; // Select the first option by default
    }
};


// Event handler functions
DataDialogue.handleSubmit = () => {
    const query = DataDialogue.elements.queryInput.value.trim();
    const model = DataDialogue.elements.dropdownButton.textContent.trim();
    if (query === '' || model === 'Select an agent') return;

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
            loadingMessage.innerHTML = `Connecting to ${sourceType}.<br>Adding database schema in SQLAgent context`;
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