DataDialogue.initRegisterSource = () => {
    const cancelCloseBtn = document.querySelector('.cancel-close-btn');
    cancelCloseBtn.addEventListener('click', DataDialogue.toggleForm);
};

DataDialogue.toggleForm = () => {
    const formContainer = document.getElementById('formContainer');
    formContainer.classList.toggle('show');
    
    // Close the menu when the form is toggled
    DataDialogue.elements.menuContainer.classList.remove('active');

    // Clear form fields when closing
    if (!formContainer.classList.contains('show')) {
        document.getElementById('sourceType').value = 'postgresql';
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
    }
};

DataDialogue.submitForm = async () => {
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

    try {
        const response = await fetch('http://localhost:8000/api/register', {
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
        alert('Form submitted successfully!');

        // Hide the form after successful submission
        DataDialogue.toggleForm();
    } catch (error) {
        console.error('Error submitting form:', error);
        alert('Error submitting form. Please try again.');
    }
};


DataDialogue.initRegisterSource();