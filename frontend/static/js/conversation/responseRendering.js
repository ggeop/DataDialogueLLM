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
    const agentHeader = DataDialogue.createAgentHeader('Contextual Agent', true, sqlResponse);
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
            ${DataDialogue.createVisualizationButton(sqlResponse)}
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
            <div class="results-section">
                <button class="remove-element" onclick="DataDialogue.removeElement(this)" title="Remove results">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" 
                         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </button>
                <p>Here are the results of the query:</p>
                ${DataDialogue.generateTableHTML(sqlResponse.results, sqlResponse.column_names)}
            </div>
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
        <div class="table-scroll-container">
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

DataDialogue.createVisualizationButton = (sqlResponse) => {
    if (!sqlResponse?.results?.length || !sqlResponse?.column_names?.length) {
        return '';
    }

    // Properly escape the JSON data for HTML attributes
    const escapedResults = JSON.stringify(sqlResponse.results).replace(/"/g, '&quot;');
    const escapedColumns = JSON.stringify(sqlResponse.column_names).replace(/"/g, '&quot;');

    return `
        <button class="plot-btn" onclick="DataDialogue.showVisualizationModal(this)" 
                data-results='${escapedResults}' 
                data-columns='${escapedColumns}'>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" 
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
            </svg>
            Plot Data
        </button>
    `;
};


DataDialogue.showVisualizationModal = (button) => {
    try {
        // Get and decode the data attributes
        const resultsStr = button.getAttribute('data-results').replace(/&quot;/g, '"');
        const columnsStr = button.getAttribute('data-columns').replace(/&quot;/g, '"');
        
        const results = JSON.parse(resultsStr);
        const columns = JSON.parse(columnsStr);

        // Create modal HTML with more user-friendly labels
        const modalHTML = `
            <div class="visualization-modal">
                <div class="visualization-modal-content">
                    <h3>Create Bar Chart</h3>
                    <div class="column-selectors">
                        <div class="select-group">
                            <label for="categorical-column">X-Axis (Categories):</label>
                            <select id="categorical-column">
                                ${columns.map(col => `<option value="${col}">${col}</option>`).join('')}
                            </select>
                        </div>
                        <div class="select-group">
                            <label for="numerical-column">Y-Axis (Values):</label>
                            <select id="numerical-column">
                                ${columns.map(col => `<option value="${col}">${col}</option>`).join('')}
                            </select>
                        </div>
                    </div>
                    <div class="visualization-actions">
                        <button class="cancel-btn" onclick="DataDialogue.closeVisualizationModal()">Cancel</button>
                        <button class="create-plot-btn" onclick="DataDialogue.createVisualization()">Create Plot</button>
                    </div>
                </div>
            </div>
        `;

        // Add modal to document
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Store the results data for later use
        DataDialogue.currentVisualizationData = results;
    } catch (error) {
        console.error('Error showing visualization modal:', error);
        alert('Error loading visualization data. Please try again.');
    }
};

DataDialogue.closeVisualizationModal = () => {
    const modal = document.querySelector('.visualization-modal');
    if (modal) {
        modal.remove();
    }
};

DataDialogue.createVisualization = () => {
    try {
        const xAxis = document.getElementById('categorical-column').value;
        const yAxis = document.getElementById('numerical-column').value;
        
        if (!DataDialogue.currentVisualizationData?.length) {
            throw new Error('No data available for visualization');
        }

        // Store current columns for reference
        DataDialogue.currentColumns = JSON.parse(
            document.querySelector('.plot-btn').getAttribute('data-columns')
        );

        const data = DataDialogue.processDataForVisualization(
            DataDialogue.currentVisualizationData,
            xAxis,
            yAxis
        );

        if (!data?.length) {
            throw new Error('No valid data after processing');
        }

        const container = document.createElement('div');
        container.className = 'visualization-container';
        
        // Add remove button container
        const headerDiv = document.createElement('div');
        headerDiv.className = 'visualization-header';
        headerDiv.innerHTML = `
            <button class="remove-element" onclick="DataDialogue.removeElement(this)" title="Remove visualization">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" 
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
            </button>
        `;
        container.appendChild(headerDiv);

        // Add chart container
        const chartContainer = document.createElement('div');
        chartContainer.className = 'chart-container';
        container.appendChild(chartContainer);

        const responseElement = document.querySelector('.app-response.sql-agent');
        responseElement.appendChild(container);

        ReactDOM.render(
            React.createElement(DataDialogue.BarChart, {
                data: data,
                categoricalColumn: xAxis,
                numericalColumn: yAxis
            }),
            chartContainer
        );

        DataDialogue.closeVisualizationModal();
    } catch (error) {
        console.error('Error in visualization creation:', error);
        DataDialogue.closeVisualizationModal();
        alert(`Error creating visualization: ${error.message}`);
    }
};

DataDialogue.processDataForVisualization = (results, xAxis, yAxis) => {
    console.log('Processing data:', { results, xAxis, yAxis });

    try {
        // Convert array results to array of objects if necessary
        const processedResults = results.map(row => {
            if (Array.isArray(row)) {
                // Get column indices
                const xIndex = DataDialogue.currentColumns.indexOf(xAxis);
                const yIndex = DataDialogue.currentColumns.indexOf(yAxis);
                
                if (xIndex === -1 || yIndex === -1) {
                    throw new Error('Column not found in data');
                }

                return {
                    [xAxis]: row[xIndex],
                    [yAxis]: row[yIndex]
                };
            }
            return row;
        });

        // Group by x-axis values and sum y-axis values
        const groupedData = processedResults.reduce((acc, row) => {
            const key = String(row[xAxis] ?? 'Unknown');
            const value = Number(row[yAxis]) || 0;
            
            if (!acc[key]) {
                acc[key] = { category: key, value: 0 };
            }
            acc[key].value += value;
            return acc;
        }, {});

        const chartData = Object.values(groupedData);
        console.log('Processed chart data:', chartData);

        return chartData;
    } catch (error) {
        console.error('Error processing data:', error);
        throw new Error('Failed to process data for visualization');
    }
};


DataDialogue.BarChart = function({ data, categoricalColumn, numericalColumn }) {
    console.log('BarChart props:', { data, categoricalColumn, numericalColumn });

    if (!window.Recharts) {
        console.error('Recharts library not loaded');
        return React.createElement('div', { className: 'error-message' },
            'Visualization library not loaded'
        );
    }

    const {
        BarChart: RechartsBarChart,
        Bar,
        XAxis,
        YAxis,
        CartesianGrid,
        Tooltip,
        ResponsiveContainer
    } = window.Recharts;

    if (!data?.length) {
        return React.createElement('div', { className: 'error-message' },
            'No data available for visualization'
        );
    }

    return React.createElement(ResponsiveContainer, { width: "100%", height: "100%" },
        React.createElement(RechartsBarChart, {
            data: data,
            margin: { top: 20, right: 30, left: 40, bottom: 60 }
        },
            React.createElement(CartesianGrid, { strokeDasharray: "3 3" }),
            React.createElement(XAxis, {
                dataKey: "category",
                angle: -45,
                textAnchor: "end",
                height: 60,
                interval: 0,
                label: {
                    value: categoricalColumn,
                    position: 'bottom',
                    offset: 40
                }
            }),
            React.createElement(YAxis, {
                label: {
                    value: numericalColumn,
                    angle: -90,
                    position: 'left',
                    offset: -10
                }
            }),
            React.createElement(Tooltip),
            React.createElement(Bar, {
                dataKey: "value",
                fill: "#4ecca3",
                name: numericalColumn
            })
        )
    );
};

DataDialogue.removeElement = (button) => {
    const container = button.closest('.results-section') || button.closest('.visualization-container');
    if (container) {
        if (container.classList.contains('visualization-container')) {
            const chartContainer = container.querySelector('.chart-container');
            if (chartContainer) {
                ReactDOM.unmountComponentAtNode(chartContainer);
            }
        }
        container.remove();
    }
};