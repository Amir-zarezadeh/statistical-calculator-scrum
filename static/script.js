// Tab switching
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');

        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

        button.classList.add('active');
        document.getElementById(tabName).classList.add('active');

        const resultDiv = document.getElementById(`${tabName}-result`);
        if (resultDiv) {
            resultDiv.innerHTML = '';
            resultDiv.className = 'result';
        }
    });
});

// Helper: display result or error
function displayResult(elementId, data, isError = false) {
    const resultDiv = document.getElementById(elementId);
    resultDiv.className = isError ? 'result error' : 'result success';

    if (isError) {
        resultDiv.innerHTML = `<p><strong>❌ Error:</strong> ${data}</p>`;
        return;
    }

    resultDiv.innerHTML = data;
}

// Helper: parse numeric input string to array of numbers
function parseNumericInput(input) {
    return input
        .split(',')
        .map(x => x.trim())
        .filter(x => x !== '')
        .map(x => Number(x))
        .filter(x => !Number.isNaN(x));
}

let descriptiveChart = null;

// Render histogram chart for descriptive stats
function renderDescriptiveChart(numbers, stats) {
    if (!Array.isArray(numbers) || numbers.length === 0) return;
    const canvas = document.getElementById('descriptive-chart');
    if (!canvas || typeof Chart === 'undefined') return;

    const min = Math.min(...numbers);
    const max = Math.max(...numbers);

    let binCount = 6;
    if (numbers.length < binCount) binCount = numbers.length;

    const range = max - min || 1;
    const binSize = range / binCount;

    const bins = new Array(binCount).fill(0);
    const labels = [];

    for (let i = 0; i < binCount; i++) {
        const start = min + i * binSize;
        const end = i === binCount - 1 ? max : min + (i + 1) * binSize;
        labels.push(`${start.toFixed(1)}–${end.toFixed(1)}`);
    }

    numbers.forEach(value => {
        let index = Math.floor((value - min) / binSize);
        if (index >= binCount) index = binCount - 1;
        if (index < 0) index = 0;
        bins[index]++;
    });

    if (descriptiveChart) {
        descriptiveChart.destroy();
    }

    const ctx = canvas.getContext('2d');
    descriptiveChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Frequency',
                data: bins,
                backgroundColor: 'rgba(123, 92, 255, 0.6)',
                borderColor: 'rgba(123, 92, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Frequency (Count)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Value Range'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true
                },
                title: {
                    display: true,
                    text: `Frequency Distribution (Mean=${stats.mean}, Median=${stats.median}, StdDev=${stats.stdDev})`
                }
            }
        }
    });
}

// Calculate Descriptive Statistics
async function calculateDescriptive() {
    const input = document.getElementById('descriptive-input').value;

    if (!input.trim()) {
        displayResult('descriptive-result', 'Please enter some numbers', true);
        return;
    }

    const numbers = parseNumericInput(input);
    if (!numbers.length) {
        displayResult('descriptive-result', 'Please enter valid numeric values', true);
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
            displayResult('descriptive-result', result.error || 'Server error', true);
            return;
        }

        const html = `
            <div class="descriptive-header">
                <span class="descriptive-header-icon">📊</span>
                <span class="descriptive-header-title">Descriptive Statistics Results</span>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">COUNT</div>
                    <div class="stat-value">${result.count}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">SUM</div>
                    <div class="stat-value">${result.sum}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">MEAN</div>
                    <div class="stat-value">${result.mean}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">MEDIAN</div>
                    <div class="stat-value">${result.median}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">MODE</div>
                    <div class="stat-value">${result.mode}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">VARIANCE</div>
                    <div class="stat-value">${result.variance}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">STD DEVIATION</div>
                    <div class="stat-value">${result.stdDev}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">MINIMUM</div>
                    <div class="stat-value">${result.min}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">MAXIMUM</div>
                    <div class="stat-value">${result.max}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">RANGE</div>
                    <div class="stat-value">${result.range}</div>
                </div>
            </div>

            <div class="chart-section">
                <div class="chart-title">Frequency Distribution</div>
                <div style="height: 280px;">
                    <canvas id="descriptive-chart"></canvas>
                </div>
            </div>

            <div class="chart-explanation">
                <h3>📖 Understanding the Chart</h3>
                <p><strong>Frequency Distribution Histogram:</strong> Each bar shows how many values fall within a range. Taller bars = more values in that range.</p>
                <p><strong>Shape:</strong> Look for patterns – bell-shaped (normal), skewed (one-sided), or multimodal (multiple peaks).</p>
                <p><strong>Mean vs Median:</strong> If similar, data is symmetric. If different, data may be skewed.</p>
                <p><strong>Spread:</strong> Wide distribution = high variability; narrow distribution = low variability.</p>
            </div>
        `;

        displayResult('descriptive-result', html);
        renderDescriptiveChart(numbers, result);

    } catch (error) {
        console.error(error);
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
                <div class="stat-card">
                    <div class="stat-label">T-Statistic</div>
                    <div class="stat-value">${result.tStatistic}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">P-Value</div>
                    <div class="stat-value">${result.pValue}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Degrees of Freedom</div>
                    <div class="stat-value">${result.degreesOfFreedom}</div>
                </div>
                <div class="stat-card">
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
                <div class="stat-card">
                    <div class="stat-label">Chi-Square Statistic</div>
                    <div class="stat-value">${result.chiSquareStatistic}</div>
                </div>
                <div class="stat-card">
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
                <div class="stat-card">
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
                <div class="stat-card">
                    <div class="stat-label">Correlation Coefficient (r)</div>
                    <div class="stat-value">${result.correlationCoefficient}</div>
                </div>
                <div class="stat-card">
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
                <div class="stat-card">
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

// CSV upload
async function uploadCsv() {
    const fileInput = document.getElementById('csv-input');
    const messageDiv = document.getElementById('csv-message');
    const textarea = document.getElementById('descriptive-input');

    if (!fileInput.files || !fileInput.files[0]) {
        messageDiv.textContent = 'Please choose a CSV file first.';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/api/upload-csv', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok || data.status === 'error') {
            messageDiv.textContent = data.message || 'Failed to upload CSV.';
            return;
        }

        textarea.value = data.data || '';
        messageDiv.textContent = `CSV uploaded successfully. ${data.count} values detected.`;

    } catch (error) {
        console.error(error);
        messageDiv.textContent = 'Failed to upload CSV.';
    }
}

// Ctrl+Enter shortcut
document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            const tabId = textarea.closest('.tab-content').id;

            switch (tabId) {
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

// Button click animation
document.querySelectorAll('.btn-calculate').forEach(button => {
    button.addEventListener('click', function () {
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
        }, 100);
    });
});

console.log('📊 Statistical Calculator loaded successfully!');
