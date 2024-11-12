DataDialogue.displayResponse = (data) => {
    const responseHTML = data.is_sql_response 
        ? DataDialogue.createSQLResponse(data.response)
        : DataDialogue.createGeneralResponse(data.response);

    DataDialogue.addMessageToConversation(
        `app-response ${data.is_sql_response ? 'sql-agent' : 'general-agent'}`, 
        responseHTML
    );
};

DataDialogue.createSQLResponse = (sqlResponse) => {
    const agentHeader = DataDialogue.createAgentHeader('SQL Agent', true);
    const sqlQuery = DataDialogue.createSQLQuerySection(sqlResponse.sql);
    const results = DataDialogue.createResultsSection(sqlResponse);

    return `
        ${agentHeader}
        ${sqlQuery}
        ${results}
    `;
};

DataDialogue.createGeneralResponse = (response) => {
    const agentHeader = DataDialogue.createAgentHeader('General Agent', false);
    return `
        ${agentHeader}
        <p>${response.response}</p>
    `;
};

DataDialogue.createAgentHeader = (agentName, isSQLAgent) => {
    const agentColor = isSQLAgent ? 'var(--sql-agent-color)' : 'var(--general-agent-color)';
    const copyButton = isSQLAgent 
        ? '<button class="copy-btn" onclick="DataDialogue.copyToClipboard(this)">Copy SQL</button>' 
        : '';
    return `
        <div class="agent-header">
            <span style="color: ${agentColor};">${agentName}</span>
            ${copyButton}
        </div>
    `;
};

DataDialogue.createSQLQuerySection = (sql) => {
    return `<pre class="sql-code"><code>${DataDialogue.highlightSQL(sql)}</code></pre>`;
};

DataDialogue.createResultsSection = (sqlResponse) => {
    if (sqlResponse.error) {
        return `
            <div class="error-message">
                <strong>Error:</strong>
                <pre>${sqlResponse.error}</pre>
            </div>
        `;
    } else if (sqlResponse.results && sqlResponse.column_names) {
        return `
            <p>Here are the results of the query:</p>
            ${DataDialogue.generateTableHTML(sqlResponse.results, sqlResponse.column_names)}
        `;
    } else {
        return '<p>The query was generated but no results were returned.</p>';
    }
};

DataDialogue.generateTableHTML = (results, columnNames) => {
    if (!Array.isArray(results) || results.length === 0 || !Array.isArray(columnNames) || columnNames.length === 0) {
        return '<p>No results to display.</p>';
    }

    // Generate header row using column_names
    const headerRow = columnNames.map(header => `<th>${header}</th>`).join('');

    // Generate data rows - assuming results is an array of arrays
    const dataRows = results.map(row => {
        // Ensure row is treated as an array
        const rowArray = Array.isArray(row) ? row : Object.values(row);
        return `<tr>${rowArray.map(cell => `<td>${cell ?? ''}</td>`).join('')}</tr>`;
    }).join('');

    return `
        <div class="table-container">
            <table class="result-table">
                <thead><tr>${headerRow}</tr></thead>
                <tbody>${dataRows}</tbody>
            </table>
        </div>
    `;
};

DataDialogue.highlightSQL = (sql) => {
    const keywords = [
        'SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'GROUP BY', 'ORDER BY', 
        'HAVING', 'LIMIT', 'OFFSET', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 
        'ALTER', 'DROP', 'TABLE', 'INDEX', 'VIEW', 'TRIGGER', 'PROCEDURE', 
        'FUNCTION', 'AND', 'OR', 'NOT', 'IN', 'BETWEEN', 'LIKE', 'IS NULL', 
        'IS NOT NULL', 'ASC', 'DESC'
    ];
    const regex = new RegExp(`\\b(${keywords.join('|')})\\b`, 'gi');
    return sql.replace(regex, match => `<span class="sql-keyword">${match}</span>`);
};

DataDialogue.copyToClipboard = (button) => {
    const sqlCode = button.closest('.app-response').querySelector('.sql-code').textContent;
    navigator.clipboard.writeText(sqlCode).then(() => {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
};