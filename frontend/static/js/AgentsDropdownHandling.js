

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
        DataDialogue.elements.dropdownButton.textContent = 'Error loading agents';
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
        DataDialogue.elements.dropdownButton.textContent = event.target.textContent;
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
        DataDialogue.elements.dropdownButton.textContent = 'Error loading agents';
    }
};

DataDialogue.populateAgentList = (agents) => {
    const { dropdownList, dropdownButton } = DataDialogue.elements;
    dropdownList.innerHTML = ''; // Clear existing options

    agents.forEach(agent => {
        const option = document.createElement('li');
        option.textContent = agent;
        dropdownList.appendChild(option);
    });

    if (agents.length > 0) {
        dropdownButton.textContent = agents[0]; // Select the first option by default
    }
};