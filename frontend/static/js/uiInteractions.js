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