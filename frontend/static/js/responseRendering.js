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
    const agentHeader = DataDialogue.createAgentHeader('SQL Agent', true, sqlResponse);
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

DataDialogue.createAgentHeader = (agentName, isSQLAgent, sqlResponse = null) => {
    const agentColor = isSQLAgent ? 'var(--sql-agent-color)' : 'var(--general-agent-color)';
    const buttons = isSQLAgent ? `
        <div class="agent-buttons">
            <button class="export-btn" onclick="DataDialogue.exportToCSV(this)" 
                    data-results='${JSON.stringify(sqlResponse?.results || [])}' 
                    data-columns='${JSON.stringify(sqlResponse?.column_names || [])}'>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" 
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Export CSV
            </button>
            <button class="copy-btn" onclick="DataDialogue.copyToClipboard(this)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" 
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                </svg>
                Copy SQL
            </button>
        </div>
    ` : '';
    
    return `
        <div class="agent-header">
            <span style="color: ${agentColor};">${agentName}</span>
            ${buttons}
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

DataDialogue.exportToCSV = (button) => {
    try {
        // Get data from button attributes
        const results = JSON.parse(button.getAttribute('data-results'));
        const columnNames = JSON.parse(button.getAttribute('data-columns'));
        
        if (!results || !columnNames) {
            console.error('No data available for export');
            return;
        }

        // Create CSV content
        const csvRows = [];
        
        // Add header row
        csvRows.push(columnNames.join(','));
        
        // Add data rows - handle both array and object formats
        results.forEach(row => {
            // Convert row to array if it's an object
            const rowArray = Array.isArray(row) ? row : columnNames.map(col => {
                const value = row[col];
                // Handle null/undefined values
                if (value === null || value === undefined) return '';
                // Handle special characters
                const valueStr = String(value);
                if (valueStr.includes(',') || valueStr.includes('"') || valueStr.includes('\n')) {
                    return `"${valueStr.replace(/"/g, '""')}"`;
                }
                return valueStr;
            });
            csvRows.push(rowArray.join(','));
        });

        const csvContent = csvRows.join('\n');

        // Create blob and download
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        
        // Format timestamp for filename
        const timestamp = new Date().toISOString()
            .replace(/[-:]/g, '')  // Remove dashes and colons
            .replace('T', '_')     // Replace T with underscore
            .slice(0, 15);         // Get only the date and hour parts
        
        link.setAttribute('href', url);
        link.setAttribute('download', `data_dialogue_${timestamp}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Show feedback
        const originalText = button.innerHTML;
        button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" 
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6L9 17l-5-5"/>
            </svg>
            Exported!
        `;
        setTimeout(() => {
            button.innerHTML = originalText;
        }, 2000);
    } catch (error) {
        console.error('Error exporting CSV:', error);
        button.textContent = 'Export failed';
        setTimeout(() => {
            button.textContent = 'Export CSV';
        }, 2000);
    }
};