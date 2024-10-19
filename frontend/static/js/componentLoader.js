// Ensure DataDialogue object exists
window.DataDialogue = window.DataDialogue || {};

document.addEventListener('DOMContentLoaded', function() {
    console.log('ComponentLoader: DOMContentLoaded event fired');
    const componentPromises = [
        loadComponent('header-component', 'header'),
        loadComponent('register-form-component', 'register_form'),
        loadComponent('demo-form-component', 'demo_form'),
        loadComponent('question-input-component', 'question_input'),
        loadComponent('loading-indicator-component', 'loading_indicator'),
        loadComponent('conversations-component', 'conversations'),
        loadComponent('example-section-component', 'demo_examples')
    ];

    Promise.all(componentPromises)
        .then(() => {
            console.log('ComponentLoader: All components loaded');
            window.DataDialogue.componentsLoaded = true;
            window.dispatchEvent(new Event('componentsLoaded'));
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
