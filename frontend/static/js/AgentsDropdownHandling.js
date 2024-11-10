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
        const agents = await response.json();
        DataDialogue.populateAgentList(agents);
    } catch (error) {
        console.error('Error fetching agent list:', error);
        DataDialogue.populateAgentList([]);
    }
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
            option.textContent = agent;
            dropdownList.appendChild(option);
        });

        dropdownButton.textContent = agents[0]; // Select the first agent by default
    } else {
        dropdownButton.textContent = 'Select an agent';
    }
};