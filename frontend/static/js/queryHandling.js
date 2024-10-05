DataDialogue.submitQuery = async (query, model) => {
    try {
        const response = await fetch('http://localhost:8000/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: query, model: model }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        DataDialogue.displayResponse(data);
    } catch (error) {
        console.error('Error details:', error);
        DataDialogue.addMessageToConversation('app-response error-response', `<div class="error-message">Error: ${error.message}</div>`);
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