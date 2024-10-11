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

DataDialogue.showLoadingAnimation = () => {
    DataDialogue.elements.loadingIndicator.style.display = 'flex';
    DataDialogue.elements.askButton.disabled = true;
};

DataDialogue.hideLoadingAnimation = () => {
    DataDialogue.elements.loadingIndicator.style.display = 'none';
    DataDialogue.elements.askButton.disabled = false;
};