# Test Suite for Statistical Calculator

## Overview
Comprehensive unittest suite for the Statistical Calculator Flask application with 47 test cases covering all endpoints and edge cases.

## Test Coverage

### Endpoints Tested
- **GET /** - Index route
- **POST /api/descriptive-stats** - Descriptive statistics
- **POST /api/t-test** - One-sample t-test
- **POST /api/chi-square** - Chi-square goodness of fit test
- **POST /api/correlation** - Pearson correlation analysis

### Test Categories

#### Descriptive Statistics (10 tests)
- Valid data with multiple values
- Single value
- Data with mode
- No unique mode
- Negative numbers
- Decimal numbers
- Empty input
- Invalid (non-numeric) input
- Whitespace handling
- Large datasets (1000 values)

#### T-Test (7 tests)
- Valid data
- Significant difference
- Non-significant difference
- Insufficient data (< 2 points)
- Missing population mean
- Invalid sample data format
- Invalid population mean format

#### Chi-Square (9 tests)
- Valid data
- Equal observed and expected frequencies
- Normalization when sums don't match
- Mismatched array lengths
- Zero expected frequencies
- Negative expected frequencies
- Empty observed data
- Missing second line
- Invalid number format

#### Correlation (11 tests)
- Perfect positive correlation (r = 1.0)
- Perfect negative correlation (r = -1.0)
- No correlation (constant values)
- Moderate positive correlation
- Mismatched array lengths
- Insufficient data (< 2 points)
- Empty X values
- Empty Y values
- Missing second line
- Invalid X format
- Invalid Y format

#### Helper Functions (6 tests)
- `get_correlation_interpretation()` with various correlation strengths
- Very strong, strong, moderate, weak, very weak correlations
- Positive, negative, and zero correlations

#### Edge Cases (4 tests)
- Missing JSON data
- Large datasets (1000+ values)
- Very small decimal numbers (0.0001)
- Very large numbers (millions)

## Running the Tests

### Prerequisites
Install required packages:
```bash
pip install Flask flask-cors scipy numpy
```

### Run All Tests
```bash
# From project root directory
python -m unittest tests.test_app -v
```

### Run Specific Test Class
```bash
python -m unittest tests.test_app.TestStatCalculatorApp -v
```

### Run Individual Test
```bash
python -m unittest tests.test_app.TestStatCalculatorApp.test_descriptive_stats_valid_data -v
```

### Quick Run (less verbose)
```bash
python -m unittest tests.test_app
```

## Test Results
```
Ran 47 tests in 0.190s

OK
```

## Test Structure

Each test follows this pattern:
1. **Arrange**: Set up test data
2. **Act**: Make POST request to endpoint
3. **Assert**: Verify response status code and data

Example:
```python
def test_descriptive_stats_valid_data(self):
    """Test descriptive stats with valid data"""
    response = self.client.post('/api/descriptive-stats',
                               json={'data': '1, 2, 3, 4, 5'},
                               content_type='application/json')
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    
    self.assertEqual(data['count'], 5)
    self.assertEqual(data['mean'], 3)
    # ... more assertions
```

## Continuous Testing
Consider integrating with CI/CD:
- GitHub Actions
- GitLab CI
- Jenkins
- Travis CI

Example GitHub Actions workflow:
```yaml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt
      - run: python -m unittest tests.test_app -v
```

## Adding New Tests

When adding new functionality to `app.py`:
1. Add corresponding test cases in `test_app.py`
2. Test both happy path and error cases
3. Run the full test suite to ensure no regressions
4. Maintain > 90% code coverage

## Notes
- Tests use Flask's test client for endpoint testing
- All tests are isolated (setUp/tearDown for each test)
- Tests include both positive and negative scenarios
- Edge cases and boundary conditions are covered
