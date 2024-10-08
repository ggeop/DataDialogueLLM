function toggleForm() {
    const formContainer = document.getElementById('formContainer');
    const pageOverlay = document.getElementById('pageOverlay');
    
    formContainer.classList.toggle('show');
    pageOverlay.style.display = formContainer.classList.contains('show') ? 'block' : 'none';
    
    // Toggle body scroll
    document.body.style.overflow = formContainer.classList.contains('show') ? 'hidden' : 'auto';
    
    // Close the menu when the form is toggled
    const menuContainer = document.querySelector('.menu-container');
    menuContainer.classList.remove('active');

    // Clear form fields when closing
    if (!formContainer.classList.contains('show')) {
        document.getElementById('sourceType').value = 'postgresql';
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
    }
}

function showLoadingAnimation(sourceType) {
    const loadingOverlay = document.querySelector('.loading-overlay');
    const loadingMessage = loadingOverlay.querySelector('.loading-message');
    loadingMessage.innerHTML = `Connecting to ${sourceType}.<br>Embedding database schema`;
    loadingOverlay.classList.add('show');
}

function hideLoadingAnimation() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    loadingOverlay.classList.remove('show');
}

async function submitForm() {
    const sourceType = document.getElementById('sourceType').value;
    const dbname = document.getElementById('dbname').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const host = document.getElementById('host').value;
    const port = document.getElementById('port').value;

    const formData = {
        sourceType,
        dbname,
        username,
        password,
        host,
        port
    };

    showLoadingAnimation(sourceType);

    try {
        const response = await fetch('http://localhost:8000/agents/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Form submitted successfully:', result);

        // Hide loading animation and close form immediately on success
        hideLoadingAnimation();
        toggleForm();
    } catch (error) {
        console.error('Error submitting form:', error);
        const loadingMessage = document.querySelector('.loading-message');
        loadingMessage.textContent = "Error connecting to database. Please try again.";
        setTimeout(() => {
            hideLoadingAnimation();
        }, 2000);
    }
}

// Add event listener for overlay click to close the form
document.getElementById('pageOverlay').addEventListener('click', function(event) {
    if (event.target === this) {
        toggleForm();
    }
});