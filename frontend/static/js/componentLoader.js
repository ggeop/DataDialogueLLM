// Ensure DataDialogue object exists
window.DataDialogue = window.DataDialogue || {};

document.addEventListener('DOMContentLoaded', function() {
    console.log('ComponentLoader: DOMContentLoaded event fired');
    const componentPromises = [
        loadComponent('header-component', 'header'),
        loadComponent('loading-indicator-component', 'loading_indicator'),
        loadComponent('example-section-component', 'demo_examples'),
        loadComponent('question-input-component', 'question_input', 'conversation'),
        loadComponent('conversations-component', 'conversations', 'conversation'),
        loadComponent('register-form-component', 'register_form', 'forms'),
        loadComponent('demo-form-component', 'demo_form', 'forms')
    ];

    Promise.all(componentPromises)
        .then(() => {
            console.log('ComponentLoader: All components loaded');
            window.DataDialogue.componentsLoaded = true;
            window.dispatchEvent(new Event('componentsLoaded'));
        })
        .catch(error => console.error('Error loading components:', error));
});

function loadComponent(elementId, componentName, subFolder) {
    const path = subFolder ? `${subFolder}/${componentName}` : componentName;
    return fetch(`/component/${path}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById(elementId).innerHTML = data;
        });
}

// Make loadComponent available globally if needed
window.loadComponent = loadComponent;