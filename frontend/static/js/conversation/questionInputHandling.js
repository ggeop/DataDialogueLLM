DataDialogue.handleSubmit = () => {
    const query = DataDialogue.elements.visibleInput.value.trim();
    const agent = DataDialogue.elements.dropdownButton.textContent.trim();
    
    // Check for empty query
    if (query === '') return;

    // Check for agent selection
    if (agent === 'Select an agent') {
        DataDialogue.addMessageToConversation('app-response error-response', `
            <div class="warning-message">
                <h3>Agent Selection Required</h3>
                <p>Please select an agent from the dropdown menu before submitting your query.</p>
            </div>
        `);
        return;
    }

    DataDialogue.addMessageToConversation('user-message', query);
    DataDialogue.elements.visibleInput.value = '';
    DataDialogue.elements.queryInput.value = '';
    DataDialogue.showLoadingAnimation();
    DataDialogue.submitQuery(query, agent);
};

DataDialogue.submitQuery = async (query, agent) => {
    try {
        DataDialogue.showLoadingAnimation();

        const response = await fetch('http://localhost:8000/api/v1/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: query, agent: agent }),
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
        
        // Create remove button
        const removeButton = document.createElement('button');
        removeButton.className = 'remove-conversation';
        removeButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        `;
        removeButton.addEventListener('click', (e) => {
            e.stopPropagation();
            conversationDiv.remove();
        });
        
        conversationDiv.appendChild(removeButton);
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