// Tab switching functionality
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        
        // Remove active class from all tabs and buttons
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        document.getElementById(tabName).classList.add('active');
        
        // Clear previous results
        const resultDiv = document.getElementById(`${tabName}-result`);
        if (resultDiv) {
            resultDiv.innerHTML = '';
        }
    });
});

// Helper function to display results
function displayResult(elementId, data, isError = false) {
    const resultDiv = document.getElementById(elementId);
    resultDiv.className = isError ? 'result error' : 'result success';
    
    if (isError) {
        resultDiv.innerHTML = `<p><strong>❌ Error:</strong> ${data}</p>`;
        return;
    }
    
    resultDiv.innerHTML = data;
}

// Calculate Descriptive Statistics
async function calculateDescriptive() {
    const input = document.getElementById('descriptive-input').value;
    
    if (!input.trim()) {
        displayResult('descriptive-result', 'Please enter some numbers', true);
        return;
    }
    
    try {
        const response = await fetch('/api/descriptive-stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: input })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            displayResult('descriptive-result', result.error, true);
            return;
        }
        
        const html = `
            <h3>📊 Descriptive Statistics Results</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Count</div>
                    <div class="stat-value">${result.count}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Sum</div>
                    <div class="stat-value">${result.sum}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Mean</</div>
                    <div class="stat-value">${result.mean}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Median</div>
                    <div class="stat-value">${result.median}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Mode</div>
                    <div class="stat-value">${result.mode}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Variance</div>
                    <div class="stat-value">${result.variance}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Std Deviation</div>
                    <div class="stat-value">${result.stdDev}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Minimum</div>
                    <div class="stat-value">${result.min}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Maximum</div>
                    <div class="stat-value">${result.max}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Range</div>
                    <div class="stat-value">${result.range}</div>
                </div>
            </div>
        `;
        
        displayResult('descriptive-result', html);
    } catch (error) {
        displayResult('descriptive-result', 'Failed to connect to server', true);
    }
}

// Calculate T-Test
async function calculateTTest() {
    const input = document.getElementById('ttest-input').value;
    
    if (!input.trim()) {
        displayResult('ttest-result', 'Please enter sample data and population mean', true);
        return;
    }
    
    try {
        const response = await fetch('/api/t-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: input })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            displayResult('ttest-result', result.error, true);
            return;
        }
        
        const html = `
            <h3>🔬 One-Sample T-Test Results</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Sample Size</div>
                    <div class="stat-value">${result.sampleSize}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Sample Mean</div>
                    <div class="stat-value">${result.sampleMean}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Population Mean</div>
                    <div class="stat-value">${result.populationMean}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Sample Std Dev</div>
                    <div class="stat-value">${result.sampleStdDev}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Standard Error</div>
                    <div class="stat-value">${result.standardError}</div>
                </div>
                <div class="stat-card highlight">
                    <div class="stat-label">T-Statistic</div>
                    <div class="stat-value">${result.tStatistic}</div>
                </div>
                <div class="stat-card highlight">
                    <div class="stat-label">P-Value</div>
                    <div class="stat-value">${result.pValue}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Degrees of Freedom</div>
                    <div class="stat-value">${result.degreesOfFreedom}</div>
                </div>
                <div class="stat-card ${result.significance === 'Significant' ? 'significant' : 'not-significant'}">
                    <div class="stat-label">Result</div>
                    <div class="stat-value">${result.significance}</div>
                </div>
            </div>
            <div class="note">
                <strong>📝 Interpretation:</strong> ${result.interpretation}
            </div>
        `;
        
        displayResult('ttest-result', html);
    } catch (error) {
        displayResult('ttest-result', 'Failed to connect to server', true);
    }
}

// Calculate Chi-Square
async function calculateChiSquare() {
    const input = document.getElementById('chisquare-input').value;
    
    if (!input.trim()) {
        displayResult('chisquare-result', 'Please enter observed and expected frequencies', true);
        return;
    }
    
    try {
        const response = await fetch('/api/chi-square', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: input })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            displayResult('chisquare-result', result.error, true);
            return;
        }
        
        const html = `
            <h3>📊 Chi-Square Test Results</h3>
            <div class="stats-grid">
                <div class="stat-card highlight">
                    <div class="stat-label">Chi-Square Statistic</div>
                    <div class="stat-value">${result.chiSquareStatistic}</div>
                </div>
                <div class="stat-card highlight">
                    <div class="stat-label">P-Value</div>
                    <div class="stat-value">${result.pValue}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Degrees of Freedom</div>
                    <div class="stat-value">${result.degreesOfFreedom}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Categories</div>
                    <div class="stat-value">${result.categories}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Observed Sum</div>
                    <div class="stat-value">${result.observedSum}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Expected Sum</div>
                    <div class="stat-value">${result.expectedSum}</div>
                </div>
                <div class="stat-card ${result.significance === 'Significant' ? 'significant' : 'not-significant'}">
                    <div class="stat-label">Result</div>
                    <div class="stat-value">${result.significance}</div>
                </div>
            </div>
            <div class="note">
                <strong>📝 Interpretation:</strong> ${result.interpretation}
            </div>
        `;
        
        displayResult('chisquare-result', html);
    } catch (error) {
        displayResult('chisquare-result', 'Failed to connect to server', true);
    }
}

// Calculate Correlation
async function calculateCorrelation() {
    const input = document.getElementById('correlation-input').value;
    
    if (!input.trim()) {
        displayResult('correlation-result', 'Please enter X and Y values', true);
        return;
    }
    
    try {
        const response = await fetch('/api/correlation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: input })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            displayResult('correlation-result', result.error, true);
            return;
        }
        
        const html = `
            <h3>📉 Correlation Analysis Results</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Sample Size (n)</div>
                    <div class="stat-value">${result.n}</div>
                </div>
                <div class="stat-card highlight">
                    <div class="stat-label">Correlation Coefficient (r)</div>
                    <div class="stat-value">${result.correlationCoefficient}</div>
                </div>
                <div class="stat-card highlight">
                    <div class="stat-label">P-Value</div>
                    <div class="stat-value">${result.pValue}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">R-Squared (r²)</div>
                    <div class="stat-value">${result.rSquared}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Mean X</div>
                    <div class="stat-value">${result.meanX}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Mean Y</div>
                    <div class="stat-value">${result.meanY}</div>
                </div>
                <div class="stat-card ${result.significance === 'Significant' ? 'significant' : 'not-significant'}">
                    <div class="stat-label">Result</div>
                    <div class="stat-value">${result.significance}</div>
                </div>
            </div>
            <div class="note">
                <strong>📝 Interpretation:</strong> ${result.interpretation}
            </div>
        `;
        
        displayResult('correlation-result', html);
    } catch (error) {
        displayResult('correlation-result', 'Failed to connect to server', true);
    }
}

// ✅ NEW: Upload CSV and fill descriptive input
function uploadCsv() {
    const fileInput = document.getElementById("csv-input");
    const messageDiv = document.getElementById("csv-message");
    const descriptiveInput = document.getElementById("descriptive-input");

    // clear previous message
    messageDiv.textContent = "";

    // check file selected
    if (!fileInput.files || fileInput.files.length === 0) {
        messageDiv.textContent = "Please select a CSV file first.";
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    fetch("/api/upload-csv", {
        method: "POST",
        body: formData
    })
        .then(response =>
            response.json().then(data => ({
                status: response.status,
                body: data
            }))
        )
        .then(result => {
            if (result.status === 200 && result.body.status === "success") {
                // put numeric values into the descriptive textarea
                descriptiveInput.value = result.body.data;
                messageDiv.textContent = `CSV uploaded successfully. ${result.body.count} values detected.`;
            } else {
                messageDiv.textContent =
                    result.body.message || "An error occurred while uploading the CSV file.";
            }
        })
        .catch(error => {
            console.error(error);
            messageDiv.textContent =
                "An unexpected error occurred while uploading the CSV file.";
        });
}

// Add Enter key support for textareas
document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            const tabId = textarea.closest('.tab-content').id;
            
            switch(tabId) {
                case 'descriptive':
                    calculateDescriptive();
                    break;
                case 'ttest':
                    calculateTTest();
                    break;
                case 'chisquare':
                    calculateChiSquare();
                    break;
                case 'correlation':
                    calculateCorrelation();
                    break;
            }
        }
    });
});

// Add visual feedback on button click
document.querySelectorAll('.btn-calculate').forEach(button => {
    button.addEventListener('click', function() {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
        }, 100);
    });
});

console.log('📊 Statistical Calculator loaded successfully!');
