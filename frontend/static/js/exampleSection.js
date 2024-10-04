DataDialogue.ExampleSection = () => {
    const [isVisible, setIsVisible] = React.useState(true);
    const examples = [
        "What are the names and salaries of all employees in the Engineering department?",
        "I want the the average sales per month for the employees in the `Sales` and `HR` department per project",
        "What is the average salary across all departments?",
        "List all projects that start in 2024 along with their end dates.",
        "Who is the highest paid employee in the Marketing department?",
        "What is the capital of france?",
        "What is a department?",
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
            React.createElement('h2', null, 'Example Questions'),
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