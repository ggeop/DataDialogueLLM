DataDialogue.ExampleSection = () => {
    const [isVisible, setIsVisible] = React.useState(true);
    const examples = [
        "Give me a list of 10 movies",
        "Give me the the top 3 actors names with the most movies"
        ];

    const handleExampleClick = (example) => {
        const visibleInput = document.getElementById('visibleInput');
        if (visibleInput) {
            visibleInput.value = example;
            visibleInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
        const queryInput = document.getElementById('queryInput');
        if (queryInput) {
            queryInput.value = example;
            queryInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    };

    const toggleVisibility = () => {
        setIsVisible(!isVisible);
    };

    return React.createElement(
        'div',
        { className: `example-section ${isVisible ? '' : 'hidden'}` },
        React.createElement(
            'div',
            { className: 'example-header' },
            React.createElement('h2', null, 'Demo Data question ideas 🔥'),
            React.createElement(
                'button',
                { onClick: toggleVisibility, className: 'hide-button' },
                isVisible ? 'Hide' : 'Show', ' Examples'
            )
        ),
        isVisible && React.createElement(
            React.Fragment,
            null,
            React.createElement('p', null, 'Click on an example to try it out:'),
            React.createElement(
                'ul',
                null,
                examples.map((example, index) =>
                    React.createElement(
                        'li',
                        { 
                            key: index, 
                            onClick: () => handleExampleClick(example),
                            style: { cursor: 'pointer' } 
                        },
                        example
                    )
                )
            )
        )
    );
};
DataDialogue.renderExampleSection = () => {
    ReactDOM.render(React.createElement(DataDialogue.ExampleSection), document.getElementById('exampleSection'));
};


DataDialogue.showExampleSection = () => {
    const exampleSection = document.querySelector('.example-section');
    if (exampleSection) {
        exampleSection.classList.remove('hidden');
    }
};

DataDialogue.hideExampleSection = () => {
    const exampleSection = document.querySelector('.example-section');
    if (exampleSection) {
        exampleSection.classList.add('hidden');
    }
};
