// Ensure DataDialogue object exists
window.DataDialogue = window.DataDialogue || {};

document.addEventListener('DOMContentLoaded', function() {
    const componentPromises = [
        loadComponent('header-component', 'header'),
        loadComponent('register-form-component', 'register_form'),
        loadComponent('question-input-component', 'question_input'),
        loadComponent('loading-indicator-component', 'loading_indicator'),
        loadComponent('conversations-component', 'conversations'),
        loadComponent('example-section-component', 'example_section')
    ];

    Promise.all(componentPromises)
        .then(() => {
            // Initialize the application after all components are loaded
            DataDialogue.init();
        })
        .catch(error => console.error('Error loading components:', error));
});

function loadComponent(elementId, componentName) {
    return fetch(`/component/${componentName}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById(elementId).innerHTML = data;
        });
}

// Make loadComponent available globally if needed
window.loadComponent = loadComponent;