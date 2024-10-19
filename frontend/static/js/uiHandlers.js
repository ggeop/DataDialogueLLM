DataDialogue.handleOutsideClick = (event) => {
    const { 
        menuContainer, 
        menuIcon, 
        pageOverlay, 
        demoFormOverlay
    } = DataDialogue.elements;

    // Check if click is outside menu
    if (menuContainer && !menuContainer.contains(event.target) && !menuIcon.contains(event.target)) {
        DataDialogue.closeMenu();
    }

    // Check if click is on main overlay (for register form)
    if (event.target === pageOverlay) {
        DataDialogue.closeRegisterForm();
    }

    // Check if click is on demo form overlay
    if (event.target === demoFormOverlay) {
        DataDialogue.closeDemoForm();
    }
};