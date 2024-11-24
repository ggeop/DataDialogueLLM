
DataDialogue.toggleDropdown = async (event) => {
    event.stopPropagation();
    if (!DataDialogue.isDropdownOpen) {
        await DataDialogue.openDropdown();
    } else {
        DataDialogue.closeDropdown();
    }
};

DataDialogue.openDropdown = async () => {
    if (DataDialogue.isFetching) return;
    
    DataDialogue.isFetching = true;
    DataDialogue.elements.dropdownButton.textContent = 'Loading...';
    DataDialogue.elements.customDropdown.classList.add('open');
    
    try {
        await DataDialogue.fetchAgentList();
        DataDialogue.elements.dropdownList.classList.add('show');
        DataDialogue.isDropdownOpen = true;
    } catch (error) {
        console.error('Error fetching agent list:', error);
        DataDialogue.elements.dropdownButton.textContent = 'Select an agent';
        DataDialogue.populateAgentList([]);
    } finally {
        DataDialogue.isFetching = false;
    }
};

DataDialogue.closeDropdown = () => {
    DataDialogue.elements.dropdownList.classList.remove('show');
    DataDialogue.elements.customDropdown.classList.remove('open');
    DataDialogue.isDropdownOpen = false;
};

DataDialogue.handleOptionClick = (event) => {
    if (event.target.tagName === 'LI') {
        const optionText = event.target.textContent;
        
        if (optionText === '+ Register Agent') {
            DataDialogue.closeDropdown();
            DataDialogue.openRegisterForm();
            return;
        }
        
        DataDialogue.elements.dropdownButton.textContent = optionText;
        DataDialogue.elements.dropdownList.querySelectorAll('li').forEach(li => li.classList.remove('selected'));
        event.target.classList.add('selected');
        DataDialogue.closeDropdown();
    }
};

DataDialogue.closeDropdownOutside = (event) => {
    if (DataDialogue.isDropdownOpen && !DataDialogue.elements.customDropdown.contains(event.target)) {
        DataDialogue.closeDropdown();
    }
};

DataDialogue.fetchAgentList = async () => {
    try {
        const response = await fetch('http://localhost:8000/api/v1/agents/list');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // Extract the agents array from the nested response
        // If data.data.agents exists, use it; otherwise fallback to empty array
        const agents = data?.data?.agents || [];
        DataDialogue.populateAgentList(agents);
    } catch (error) {
        console.error('Error fetching agent list:', error);
        DataDialogue.populateAgentList([]);
    }
};

DataDialogue.initConfirmDialog = () => {
    const confirmHtml = `
        <div class="confirm-dialog">
            <div class="confirm-dialog-title">Confirm Delete</div>
            <div class="confirm-dialog-message"></div>
            <div class="confirm-dialog-buttons">
                <button class="confirm-dialog-button confirm-dialog-cancel">Cancel</button>
                <button class="confirm-dialog-button confirm-dialog-confirm">Delete</button>
            </div>
        </div>
    `;
    
    const overlay = document.createElement('div');
    overlay.className = 'confirm-dialog-overlay';
    overlay.style.display = 'none';
    overlay.innerHTML = confirmHtml;
    document.body.appendChild(overlay);
    
    // Cache the elements
    DataDialogue.elements.confirmDialog = overlay;
    DataDialogue.elements.confirmMessage = overlay.querySelector('.confirm-dialog-message');
    DataDialogue.elements.confirmCancelBtn = overlay.querySelector('.confirm-dialog-cancel');
    DataDialogue.elements.confirmConfirmBtn = overlay.querySelector('.confirm-dialog-confirm');
};

DataDialogue.createConfirmDialog = (message) => {
    return new Promise((resolve) => {
        const { confirmDialog, confirmMessage, confirmCancelBtn, confirmConfirmBtn } = DataDialogue.elements;
        
        // Update message
        confirmMessage.textContent = message;
        
        // Show dialog
        confirmDialog.style.display = 'flex';
        // Use the same animation class pattern you use elsewhere
        confirmDialog.classList.add('fade-in-up');
        
        const closeDialog = (result) => {
            confirmDialog.classList.remove('fade-in-up');
            confirmDialog.style.display = 'none';
            resolve(result);
        };
        
        // Setup one-time event listeners
        const cancelHandler = () => {
            confirmCancelBtn.removeEventListener('click', cancelHandler);
            confirmConfirmBtn.removeEventListener('click', confirmHandler);
            closeDialog(false);
        };
        
        const confirmHandler = () => {
            confirmCancelBtn.removeEventListener('click', cancelHandler);
            confirmConfirmBtn.removeEventListener('click', confirmHandler);
            closeDialog(true);
        };
        
        confirmCancelBtn.addEventListener('click', cancelHandler);
        confirmConfirmBtn.addEventListener('click', confirmHandler);
    });
};

DataDialogue.populateAgentList = (agents) => {
    const { dropdownList, dropdownButton } = DataDialogue.elements;
    dropdownList.innerHTML = ''; // Clear existing options

    // Always add the "Add Agent" option
    const addAgentOption = document.createElement('li');
    addAgentOption.textContent = '+ Register Agent';
    addAgentOption.classList.add('add-agent-option');
    dropdownList.appendChild(addAgentOption);

    if (agents.length > 0) {
        // Add a separator after "Add Agent" option
        const separator = document.createElement('li');
        separator.classList.add('dropdown-separator');
        dropdownList.appendChild(separator);

        // Add the rest of the agents
        agents.forEach(agent => {
            const option = document.createElement('li');
            
            // Create span for agent name
            const nameSpan = document.createElement('span');
            nameSpan.textContent = agent;
            nameSpan.classList.add('agent-name-text');
            
            // Create delete button
            const deleteBtn = document.createElement('button');
            deleteBtn.classList.add('agent-delete-btn');
            deleteBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 18L18 6M6 6l12 12"/>
            </svg>`;
            
            // Add delete functionality
            deleteBtn.addEventListener('click', async (e) => {
                e.stopPropagation(); // Prevent dropdown item selection
                
                const confirmed = await DataDialogue.createConfirmDialog(
                    `Are you sure you want to delete agent "${agent}"?`
                );
                
                if (confirmed) {
                    try {
                        const encodedAgent = encodeURIComponent(encodeURIComponent(agent));
                        const response = await fetch(`http://localhost:8000/api/v1/agents/${encodedAgent}`, {
                            method: 'DELETE'
                        });
                        
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        
                        // Refresh the agent list
                        await DataDialogue.fetchAgentList();
                    } catch (error) {
                        console.error('Error deleting agent:', error);
                        alert('Failed to delete agent. Please try again.');
                    }
                }
            });
            
            option.appendChild(nameSpan);
            option.appendChild(deleteBtn);
            dropdownList.appendChild(option);
        });

        dropdownButton.textContent = agents[0]; // Select the first agent by default
    } else {
        dropdownButton.textContent = 'Select an agent';
    }
};


DataDialogue.handleOptionClick = (event) => {
    const listItem = event.target.closest('li');
    if (!listItem) return;
    
    if (listItem.classList.contains('add-agent-option')) {
        DataDialogue.closeDropdown();
        DataDialogue.openRegisterForm();
        return;
    }
    
    // Only update selection if clicking on the name text, not the delete button
    if (event.target.classList.contains('agent-name-text')) {
        const optionText = event.target.textContent;
        DataDialogue.elements.dropdownButton.textContent = optionText;
        DataDialogue.elements.dropdownList.querySelectorAll('li').forEach(li => li.classList.remove('selected'));
        listItem.classList.add('selected');
        DataDialogue.closeDropdown();
    }
};
