from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math
import csv
import io
import statistics
from scipy import stats

app = Flask(__name__)
CORS(app)


def parse_csv_file(file_storage):
    """
    Parse an uploaded CSV file and return a list of numeric values.
    Raises ValueError with a message if something is wrong.
    """
    if file_storage.filename == "":
        raise ValueError("No file selected.")

    # Read file content and decode to text
    content = file_storage.read().decode("utf-8", errors="ignore")
    if not content.strip():
        raise ValueError("The CSV file is empty.")

    f = io.StringIO(content)
    reader = csv.reader(f)

    values = []
    first_row = True

    for line_number, row in enumerate(reader, start=1):
        # Skip completely empty rows
        if not row or all(cell.strip() == "" for cell in row):
            continue

        # Treat first row as possible header
        if first_row:
            first_row = False
            # Check if row is purely non-numeric → then treat as header
            all_non_numeric = True
            for cell in row:
                cell = cell.strip()
                if cell == "":
                    continue
                try:
                    float(cell)
                    all_non_numeric = False
                    break
                except ValueError:
                    continue
            if all_non_numeric:
                # Header row → skip and continue with next line
                continue
            # Otherwise fall through and treat as data row

        # Process data row
        for cell in row:
            cell = cell.strip()
            if cell == "":
                continue
            try:
                values.append(float(cell))
            except ValueError:
                raise ValueError(
                    f"CSV contains non-numeric value '{cell}' in line {line_number}."
                )

    if len(values) < 2:
        raise ValueError("Not enough numeric values found in the CSV file.")

    return values


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """
    Endpoint to upload a CSV file and return parsed numeric data.
    Used to fill the descriptive statistics input automatically.
    """
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file part in the request."
        }), 400

    file = request.files["file"]

    try:
        values = parse_csv_file(file)
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Unexpected error while parsing CSV: {str(e)}"
        }), 500

    data_str = ", ".join(str(v) for v in values)

    return jsonify({
        "status": "success",
        "count": len(values),
        "data": data_str
    }), 200


@app.route('/api/descriptive-stats', methods=['POST'])
def descriptive_stats():
    try:
        data = request.json.get('data', '')
        numbers = [float(x.strip()) for x in data.split(',') if x.strip()]

        if not numbers:
            return jsonify({'error': 'Please enter valid numbers'}), 400

        # Calculate statistics
        n = len(numbers)
        total = sum(numbers)
        mean = statistics.mean(numbers)
        median = statistics.median(numbers)

        # Variance and standard deviation
        if n > 1:
            variance = statistics.variance(numbers)
            std_dev = statistics.stdev(numbers)
        else:
            variance = 0
            std_dev = 0

        minimum = min(numbers)
        maximum = max(numbers)
        data_range = maximum - minimum

        # Mode (if exists)
        try:
            mode = statistics.mode(numbers)
        except statistics.StatisticsError:
            mode = "No unique mode"

        result = {
            'count': n,
            'sum': round(total, 4),
            'mean': round(mean, 4),
            'median': round(median, 4),
            'mode': mode if isinstance(mode, str) else round(mode, 4),
            'variance': round(variance, 4),
            'stdDev': round(std_dev, 4),
            'min': round(minimum, 4),
            'max': round(maximum, 4),
            'range': round(data_range, 4)
        }

        return jsonify(result)

    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter numbers only.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/t-test', methods=['POST'])
def t_test():
    try:
        data = request.json.get('data', '')

        # Split by newlines and filter empty lines
        lines = [line.strip() for line in data.strip().split('\n') if line.strip()]

        if len(lines) < 2:
            return jsonify({
                'error': 'Enter sample data (line 1) and population mean (line 2). Make sure to press Enter between lines.'
            }), 400

        # Parse sample data
        try:
            sample = [float(x.strip()) for x in lines[0].split(',') if x.strip()]
        except ValueError as e:
            return jsonify({'error': f'Invalid sample data format: {str(e)}'}), 400

        # Parse population mean
        try:
            population_mean = float(lines[1].strip())
        except ValueError:
            return jsonify({'error': 'Population mean must be a single number'}), 400

        if not sample:
            return jsonify({'error': 'Sample data cannot be empty'}), 400

        if len(sample) < 2:
            return jsonify({'error': 'Need at least 2 data points for t-test'}), 400

        # Calculate t-test using scipy
        t_statistic, p_value = stats.ttest_1samp(sample, population_mean)

        n = len(sample)
        sample_mean = statistics.mean(sample)
        sample_std = statistics.stdev(sample)
        std_error = sample_std / math.sqrt(n)
        df = n - 1

        # Determine significance
        significance = "Significant" if p_value < 0.05 else "Not Significant"

        result = {
            'sampleSize': n,
            'sampleMean': round(sample_mean, 4),
            'populationMean': round(population_mean, 4),
            'sampleStdDev': round(sample_std, 4),
            'standardError': round(std_error, 4),
            'tStatistic': round(t_statistic, 4),
            'pValue': round(p_value, 6),
            'degreesOfFreedom': df,
            'significance': significance,
            'interpretation': f'At α=0.05: {significance} (p={round(p_value, 4)})'
        }

        return jsonify(result)

    except ValueError as e:
        return jsonify({'error': f'Invalid input format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/api/chi-square', methods=['POST'])
def chi_square():
    try:
        data = request.json.get('data', '')

        # Debug: Print received data
        print(f"Received data: {repr(data)}")

        # Split by newlines and filter empty lines
        lines = [line.strip() for line in data.strip().split('\n') if line.strip()]

        print(f"Number of lines: {len(lines)}")
        print(f"Lines: {lines}")

        if len(lines) < 2:
            return jsonify({
                'error': 'Enter observed (line 1) and expected (line 2) frequencies. Make sure to press Enter between lines.'
            }), 400

        # Parse observed frequencies
        try:
            observed = [float(x.strip()) for x in lines[0].split(',') if x.strip()]
        except (ValueError, IndexError) as e:
            return jsonify({'error': f'Invalid observed frequencies format: {str(e)}'}), 400

        # Parse expected frequencies
        try:
            expected = [float(x.strip()) for x in lines[1].split(',') if x.strip()]
        except (ValueError, IndexError) as e:
            return jsonify({'error': f'Invalid expected frequencies format: {str(e)}'}), 400

        print(f"Observed: {observed}")
        print(f"Expected: {expected}")

        if not observed:
            return jsonify({'error': 'Observed frequencies cannot be empty'}), 400

        if not expected:
            return jsonify({'error': 'Expected frequencies cannot be empty'}), 400

        if len(observed) != len(expected):
            return jsonify({
                'error': f'Observed ({len(observed)}) and expected ({len(expected)}) must have same length'
            }), 400

        if any(e <= 0 for e in expected):
            return jsonify({'error': 'Expected frequencies must be positive values'}), 400

        # Check if sums are approximately equal
        sum_obs = sum(observed)
        sum_exp = sum(expected)
        print(f"Sum observed: {sum_obs}, Sum expected: {sum_exp}")

        # If sums don't match, normalize expected frequencies
        if abs(sum_obs - sum_exp) > 1e-6:
            print("Sums don't match. Normalizing expected frequencies...")
            expected = [(e * sum_obs / sum_exp) for e in expected]
            print(f"Normalized expected: {expected}")

        # Calculate chi-square manually
        chi_square_stat = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
        df = len(observed) - 1

        # Calculate p-value using chi-square distribution
        p_value = 1 - stats.chi2.cdf(chi_square_stat, df)

        # Determine significance
        significance = "Significant" if p_value < 0.05 else "Not Significant"

        result = {
            'chiSquareStatistic': round(chi_square_stat, 4),
            'pValue': round(p_value, 6),
            'degreesOfFreedom': df,
            'categories': len(observed),
            'significance': significance,
            'observedSum': round(sum_obs, 2),
            'expectedSum': round(sum(expected), 2),
            'interpretation': f'At α=0.05: {significance} (p={round(p_value, 4)})'
        }

        return jsonify(result)

    except ValueError as e:
        return jsonify({'error': f'Invalid input format: {str(e)}'}), 400
    except ZeroDivisionError:
        return jsonify({'error': 'Expected frequencies cannot be zero'}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/api/correlation', methods=['POST'])
def correlation():
    try:
        data = request.json.get('data', '')

        # Split by newlines and filter empty lines
        lines = [line.strip() for line in data.strip().split('\n') if line.strip()]

        if len(lines) < 2:
            return jsonify({
                'error': 'Enter X values (line 1) and Y values (line 2). Make sure to press Enter between lines.'
            }), 400

        # Parse X values
        try:
            x_values = [float(x.strip()) for x in lines[0].split(',') if x.strip()]
        except ValueError as e:
            return jsonify({'error': f'Invalid X values format: {str(e)}'}), 400

        # Parse Y values
        try:
            y_values = [float(y.strip()) for y in lines[1].split(',') if y.strip()]
        except ValueError as e:
            return jsonify({'error': f'Invalid Y values format: {str(e)}'}), 400

        if not x_values:
            return jsonify({'error': 'X values cannot be empty'}), 400

        if not y_values:
            return jsonify({'error': 'Y values cannot be empty'}), 400

        if len(x_values) != len(y_values):
            return jsonify({
                'error': f'X ({len(x_values)}) and Y ({len(y_values)}) must have same length'
            }), 400

        if len(x_values) < 2:
            return jsonify({'error': 'Need at least 2 data points for correlation'}), 400

        # Calculate Pearson correlation using scipy
        correlation_coef, p_value = stats.pearsonr(x_values, y_values)

        # Coefficient of determination
        r_squared = correlation_coef ** 2

        n = len(x_values)
        mean_x = statistics.mean(x_values)
        mean_y = statistics.mean(y_values)

        # Determine significance
        significance = "Significant" if p_value < 0.05 else "Not Significant"

        result = {
            'n': n,
            'correlationCoefficient': round(correlation_coef, 4),
            'pValue': round(p_value, 6),
            'rSquared': round(r_squared, 4),
            'meanX': round(mean_x, 4),
            'meanY': round(mean_y, 4),
            'significance': significance,
            'interpretation': get_correlation_interpretation(correlation_coef, p_value)
        }

        return jsonify(result)

    except ValueError as e:
        return jsonify({'error': f'Invalid input format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


def get_correlation_interpretation(r, p_value):
    r_abs = abs(r)
    if r_abs >= 0.9:
        strength = "Very strong"
    elif r_abs >= 0.7:
        strength = "Strong"
    elif r_abs >= 0.5:
        strength = "Moderate"
    elif r_abs >= 0.3:
        strength = "Weak"
    else:
        strength = "Very weak"

    direction = "positive" if r > 0 else "negative" if r < 0 else "no"
    sig_text = "significant" if p_value < 0.05 else "not significant"

    return f"{strength} {direction} correlation ({sig_text} at α=0.05, p={round(p_value, 4)})"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
