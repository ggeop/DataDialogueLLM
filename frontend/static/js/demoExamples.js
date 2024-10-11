DataDialogue.ExampleSection = () => {
    const [isVisible, setIsVisible] = React.useState(true);
    const examples = [
        "Give me the most popular DVD titles",
        "Give me the top 3 customers the last 3 months",
        "Give me the top 5 stores per year",
    ];

    const handleExampleClick = (example) => {
        document.getElementById('queryInput').value = example;
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
                        { key: index, onClick: () => handleExampleClick(example) },
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
