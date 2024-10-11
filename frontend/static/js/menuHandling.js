DataDialogue.toggleMenu = () => {
    DataDialogue.elements.menuContainer.classList.toggle('active');
};

DataDialogue.handleOutsideClick = (event) => {
    const { menuContainer, menuIcon } = DataDialogue.elements;
    if (menuContainer && !menuContainer.contains(event.target) && !menuIcon.contains(event.target)) {
        menuContainer.classList.remove('active');
    }
};