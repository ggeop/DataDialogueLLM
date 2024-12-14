DataDialogue.selectFile = async () => {
    try {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.csv';
        
        input.onchange = async (event) => {
            const file = event.target.files[0];
            if (file) {
                const formData = new FormData();
                formData.append('file', file);

                try {
                    const response = await fetch('http://localhost:8000/api/v1/files/upload', {
                        method: 'POST',
                        body: formData,
                    });

                    if (!response.ok) {
                        throw new Error('Upload failed');
                    }

                    const result = await response.json();
                    const display = document.getElementById('selectedPathDisplay');
                    if (display) {
                        display.textContent = `Selected file: ${result.filename}`;
                    }

                    // Store the filepath in a hidden input
                    const filepathInput = document.getElementById('filepath') || document.createElement('input');
                    filepathInput.type = 'hidden';
                    filepathInput.id = 'filepath';
                    filepathInput.value = result.filepath;
                    document.getElementById('filepathGroup').appendChild(filepathInput);

                } catch (error) {
                    DataDialogue.showMessage(`Error uploading file: ${error.message}`);
                }
            }
        };
        
        input.click();
    } catch (error) {
        DataDialogue.showMessage(`Error selecting file: ${error.message}`);
    }
};

DataDialogue.selectFolder = async () => {
    try {
        const input = document.createElement('input');
        input.type = 'file';
        input.webkitdirectory = true;
        input.multiple = true;
        
        input.onchange = async (event) => {
            const files = Array.from(event.target.files).filter(file => file.name.endsWith('.csv'));
            
            if (files.length > 0) {
                const formData = new FormData();
                formData.append('file', files[0]); // For now, just upload the first CSV file

                try {
                    const response = await fetch('http://localhost:8000/api/v1/files/upload', {
                        method: 'POST',
                        body: formData,
                    });

                    if (!response.ok) {
                        throw new Error('Upload failed');
                    }

                    const result = await response.json();
                    const display = document.getElementById('selectedPathDisplay');
                    if (display) {
                        display.textContent = `Selected folder file: ${result.filename}`;
                    }

                    // Store the filepath in a hidden input
                    const filepathInput = document.getElementById('filepath') || document.createElement('input');
                    filepathInput.type = 'hidden';
                    filepathInput.id = 'filepath';
                    filepathInput.value = result.filepath;
                    document.getElementById('filepathGroup').appendChild(filepathInput);

                } catch (error) {
                    DataDialogue.showMessage(`Error uploading file: ${error.message}`);
                }
            } else {
                DataDialogue.showMessage('No CSV files found in the selected folder');
            }
        };
        
        input.click();
    } catch (error) {
        DataDialogue.showMessage(`Error selecting folder: ${error.message}`);
    }
};

DataDialogue.updateSelectedPath = (path, type) => {
    const display = document.getElementById('selectedPathDisplay');
    const hidden = document.createElement('input');
    hidden.type = 'hidden';
    hidden.id = 'filepath';
    hidden.value = path;

    // Remove any existing hidden input
    const existingHidden = document.getElementById('filepath');
    if (existingHidden) {
        existingHidden.remove();
    }

    // Add the new hidden input
    display.parentNode.appendChild(hidden);

    // Update display text
    display.textContent = `Selected ${type}: ${path}`;
    display.title = path; // Add tooltip for long paths
};

DataDialogue.openFileDialog = async (options = {}) => {
    // If running in Electron
    if (window.electronAPI) {
        return window.electronAPI.showOpenDialog(options);
    } else {
        // Fallback for web browsers
        return new Promise((resolve, reject) => {
            const input = document.createElement('input');
            input.type = 'file';
            
            if (options.properties?.includes('openDirectory')) {
                input.webkitdirectory = true;
            }
            
            input.onchange = (event) => {
                const files = event.target.files;
                if (files && files.length > 0) {
                    // Handle the selected file(s)
                    DataDialogue.uploadFiles(files).then(result => {
                        resolve({ paths: [result.filepath] });
                    }).catch(reject);
                }
            };
            input.click();
        });
    }
};

DataDialogue.uploadFiles = async (files) => {
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    try {
        const response = await fetch('http://localhost:8000/api/v1/files/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        return await response.json();
    } catch (error) {
        DataDialogue.showMessage(`Error uploading files: ${error.message}`);
        throw error;
    }
};