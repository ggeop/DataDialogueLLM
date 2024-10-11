DataDialogue.handleSubmit = () => {
    const query = DataDialogue.elements.queryInput.value.trim();
    const model = DataDialogue.elements.dropdownButton.textContent.trim();
    if (query === '' || model === 'Select an agent') return;

    DataDialogue.addMessageToConversation('user-message', query);
    DataDialogue.elements.queryInput.value = '';
    DataDialogue.showLoadingAnimation();
    DataDialogue.submitQuery(query, model);
};

DataDialogue.submitQuery = async (query, model) => {
    try {
        DataDialogue.showLoadingAnimation();

        const response = await fetch('http://localhost:8000/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: query, model: model }),
        });

        if (!response.ok) {
            const errorBody = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, body: ${errorBody}`);
        }

        const data = await response.json();
        DataDialogue.displayResponse(data);
    } catch (error) {
        console.error('Error details:', error);
        let errorMessage = 'An unexpected error occurred.';

        if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
            errorMessage = 'Network error: Unable to connect to the server. Please check your internet connection and try again.';
        } else if (error.message.includes('HTTP error!')) {
            errorMessage = `Server error: ${error.message}`;
        } else {
            errorMessage = `Error: ${error.message}`;
        }

        DataDialogue.addMessageToConversation('app-response error-response', `
            <div class="error-message">
                <h3>Error Occurred</h3>
                <p>${errorMessage}</p>
                <details>
                    <summary>Technical Details</summary>
                    <pre>${error.stack || 'No stack trace available'}</pre>
                </details>
            </div>
        `);
    } finally {
        DataDialogue.hideLoadingAnimation();
    }
};

DataDialogue.addMessageToConversation = (className, content) => {
    let conversationDiv;
    const lastConversation = DataDialogue.elements.conversationsDiv.lastElementChild;
    
    if (className.includes('user-message') || !lastConversation || !lastConversation.classList.contains('conversation')) {
        conversationDiv = document.createElement('div');
        conversationDiv.className = 'conversation';
        DataDialogue.elements.conversationsDiv.appendChild(conversationDiv);
    } else {
        conversationDiv = lastConversation;
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = className;
    if (className.includes('user-message')) {
        content = `
            <svg class="user-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
            ${content}
        `;
    }
    messageDiv.innerHTML = content;
    conversationDiv.appendChild(messageDiv);
    DataDialogue.elements.conversationsDiv.scrollTop = DataDialogue.elements.conversationsDiv.scrollHeight;
};


DataDialogue.showLoadingAnimation = () => {
    DataDialogue.elements.loadingIndicator.style.display = 'flex';
    DataDialogue.elements.askButton.disabled = true;
};

DataDialogue.hideLoadingAnimation = () => {
    DataDialogue.elements.loadingIndicator.style.display = 'none';
    DataDialogue.elements.askButton.disabled = false;
};