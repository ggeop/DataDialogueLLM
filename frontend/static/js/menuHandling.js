DataDialogue.toggleMenu = () => {
    const { menuContainer, pageOverlay, tryDemoContainer } = DataDialogue.elements;
    const isMenuActive = menuContainer.classList.toggle('active');
    
    if (pageOverlay) {
        pageOverlay.style.display = isMenuActive ? 'block' : 'none';
        document.body.style.overflow = isMenuActive ? 'hidden' : 'auto';
    }

    // Hide try demo button when menu is open
    if (tryDemoContainer) {
        tryDemoContainer.style.display = isMenuActive ? 'none' : 'block';
    }
};

DataDialogue.closeMenu = () => {
    const { menuContainer, pageOverlay, tryDemoContainer } = DataDialogue.elements;
    if (menuContainer) menuContainer.classList.remove('active');
    if (pageOverlay) pageOverlay.style.display = 'none';
    document.body.style.overflow = 'auto';
    
    // Show try demo button when menu is closed
    if (tryDemoContainer) tryDemoContainer.style.display = 'block';
};

DataDialogue.toggleElementsVisibility = (hideElements) => {
    const elementsToToggle = [
        DataDialogue.elements.tryDemoContainer,
        DataDialogue.elements.conversationsDiv,
        DataDialogue.elements.queryInput,
        DataDialogue.elements.askButton,
    ];

    elementsToToggle.forEach(element => {
        if (element) {
            element.style.display = hideElements ? 'none' : '';
        }
    });
};