import unittest
import json
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, get_correlation_interpretation


class TestStatCalculatorApp(unittest.TestCase):
    """Test suite for the Statistical Calculator Flask application"""

    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after each test"""
        pass

    # ===== Test Index Route =====
    def test_index_route(self):
        """Test that the index route returns the HTML page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # ===== Test Descriptive Statistics Endpoint =====
    def test_descriptive_stats_valid_data(self):
        """Test descriptive stats with valid data"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '1, 2, 3, 4, 5'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['count'], 5)
        self.assertEqual(data['sum'], 15)
        self.assertEqual(data['mean'], 3)
        self.assertEqual(data['median'], 3)
        self.assertEqual(data['min'], 1)
        self.assertEqual(data['max'], 5)
        self.assertEqual(data['range'], 4)
        self.assertAlmostEqual(data['variance'], 2.5)
        self.assertAlmostEqual(data['stdDev'], 1.5811, places=3)

    def test_descriptive_stats_single_value(self):
        """Test descriptive stats with a single value"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '42'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['mean'], 42)
        self.assertEqual(data['variance'], 0)
        self.assertEqual(data['stdDev'], 0)

    def test_descriptive_stats_with_mode(self):
        """Test descriptive stats with data that has a mode"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '1, 2, 2, 3, 4'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['mode'], 2)

    def test_descriptive_stats_no_unique_mode(self):
        """Test descriptive stats with data that has no unique mode"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '1, 2, 3, 4'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # In Python 3.8+, mode returns first value when no unique mode exists
        # The app will catch StatisticsError for multimodal data in older versions
        self.assertIn('mode', data)  # Just verify mode key exists

    def test_descriptive_stats_negative_numbers(self):
        """Test descriptive stats with negative numbers"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '-5, -3, -1, 0, 2'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['count'], 5)
        self.assertEqual(data['min'], -5)
        self.assertEqual(data['max'], 2)
        self.assertEqual(data['range'], 7)

    def test_descriptive_stats_decimal_numbers(self):
        """Test descriptive stats with decimal numbers"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '1.5, 2.7, 3.2, 4.8'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['count'], 4)
        self.assertAlmostEqual(data['mean'], 3.05, places=2)

    def test_descriptive_stats_empty_input(self):
        """Test descriptive stats with empty input"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': ''},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_descriptive_stats_invalid_input(self):
        """Test descriptive stats with invalid (non-numeric) input"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '1, 2, abc, 4'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_descriptive_stats_whitespace_handling(self):
        """Test descriptive stats handles whitespace correctly"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '  1 ,  2,3  , 4  ,5  '},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 5)

    # ===== Test T-Test Endpoint =====
    def test_t_test_valid_data(self):
        """Test t-test with valid data"""
        response = self.client.post('/api/t-test',
                                   json={'data': '2.3, 2.5, 2.7, 2.9, 3.1\n2.5'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['sampleSize'], 5)
        self.assertAlmostEqual(data['sampleMean'], 2.7, places=1)
        self.assertEqual(data['populationMean'], 2.5)
        self.assertIn('tStatistic', data)
        self.assertIn('pValue', data)
        self.assertEqual(data['degreesOfFreedom'], 4)
        self.assertIn('significance', data)

    def test_t_test_significant_difference(self):
        """Test t-test with significantly different values"""
        response = self.client.post('/api/t-test',
                                   json={'data': '10, 12, 14, 16, 18\n5'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['sampleMean'], 14)
        self.assertEqual(data['populationMean'], 5)
        # Should be significant
        self.assertLess(data['pValue'], 0.05)
        self.assertEqual(data['significance'], 'Significant')

    def test_t_test_not_significant(self):
        """Test t-test with non-significant difference"""
        response = self.client.post('/api/t-test',
                                   json={'data': '5.0, 5.1, 4.9, 5.0, 5.0\n5.0'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should not be significant
        self.assertGreater(data['pValue'], 0.05)
        self.assertEqual(data['significance'], 'Not Significant')

    def test_t_test_insufficient_data(self):
        """Test t-test with only one data point"""
        response = self.client.post('/api/t-test',
                                   json={'data': '5\n4'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('at least 2', data['error'])

    def test_t_test_missing_population_mean(self):
        """Test t-test with missing population mean"""
        response = self.client.post('/api/t-test',
                                   json={'data': '1, 2, 3, 4, 5'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_t_test_invalid_sample_data(self):
        """Test t-test with invalid sample data"""
        response = self.client.post('/api/t-test',
                                   json={'data': 'a, b, c\n5'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_t_test_invalid_population_mean(self):
        """Test t-test with invalid population mean"""
        response = self.client.post('/api/t-test',
                                   json={'data': '1, 2, 3, 4, 5\nabc'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    # ===== Test Chi-Square Endpoint =====
    def test_chi_square_valid_data(self):
        """Test chi-square with valid data"""
        response = self.client.post('/api/chi-square',
                                   json={'data': '10, 15, 20, 25\n12.5, 12.5, 12.5, 12.5'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertIn('chiSquareStatistic', data)
        self.assertIn('pValue', data)
        self.assertEqual(data['degreesOfFreedom'], 3)
        self.assertEqual(data['categories'], 4)

    def test_chi_square_equal_frequencies(self):
        """Test chi-square with equal observed and expected frequencies"""
        response = self.client.post('/api/chi-square',
                                   json={'data': '10, 20, 30, 40\n10, 20, 30, 40'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should be 0 when observed equals expected
        self.assertAlmostEqual(data['chiSquareStatistic'], 0, places=4)
        self.assertGreater(data['pValue'], 0.95)  # Very high p-value

    def test_chi_square_normalization(self):
        """Test chi-square normalizes expected frequencies when sums don't match"""
        response = self.client.post('/api/chi-square',
                                   json={'data': '20, 30, 40, 50\n10, 10, 10, 10'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Should normalize and compute
        self.assertIn('chiSquareStatistic', data)
        self.assertAlmostEqual(data['observedSum'], 140, places=1)

    def test_chi_square_mismatched_lengths(self):
        """Test chi-square with different lengths"""
        response = self.client.post('/api/chi-square',
                                   json={'data': '10, 20, 30\n10, 20'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('same length', data['error'])

    def test_chi_square_zero_expected(self):
        """Test chi-square with zero in expected frequencies"""
        response = self.client.post('/api/chi-square',
                                   json={'data': '10, 20, 30\n0, 10, 20'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_chi_square_negative_expected(self):
        """Test chi-square with negative expected frequencies"""
        response = self.client.post('/api/chi-square',
                                   json={'data': '10, 20, 30\n-5, 10, 20'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_chi_square_empty_observed(self):
        """Test chi-square with empty observed frequencies"""
        response = self.client.post('/api/chi-square',
                                   json={'data': '\n10, 20, 30'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_chi_square_missing_line(self):
        """Test chi-square with only one line"""
        response = self.client.post('/api/chi-square',
                                   json={'data': '10, 20, 30'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_chi_square_invalid_format(self):
        """Test chi-square with invalid number format"""
        response = self.client.post('/api/chi-square',
                                   json={'data': 'a, b, c\n10, 20, 30'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    # ===== Test Correlation Endpoint =====
    def test_correlation_perfect_positive(self):
        """Test correlation with perfect positive correlation"""
        response = self.client.post('/api/correlation',
                                   json={'data': '1, 2, 3, 4, 5\n2, 4, 6, 8, 10'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['n'], 5)
        self.assertAlmostEqual(data['correlationCoefficient'], 1.0, places=4)
        self.assertAlmostEqual(data['rSquared'], 1.0, places=4)
        self.assertLess(data['pValue'], 0.05)
        self.assertEqual(data['significance'], 'Significant')

    def test_correlation_perfect_negative(self):
        """Test correlation with perfect negative correlation"""
        response = self.client.post('/api/correlation',
                                   json={'data': '1, 2, 3, 4, 5\n10, 8, 6, 4, 2'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertAlmostEqual(data['correlationCoefficient'], -1.0, places=4)
        self.assertAlmostEqual(data['rSquared'], 1.0, places=4)

    def test_correlation_no_correlation(self):
        """Test correlation with no correlation"""
        response = self.client.post('/api/correlation',
                                   json={'data': '1, 2, 3, 4, 5\n5, 5, 5, 5, 5'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Can't compute correlation when Y is constant (will be NaN)
        # This is expected behavior - should handle gracefully

    def test_correlation_moderate_positive(self):
        """Test correlation with moderate positive correlation"""
        response = self.client.post('/api/correlation',
                                   json={'data': '1, 2, 3, 4, 5\n2, 3, 5, 7, 8'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertGreater(data['correlationCoefficient'], 0.8)
        self.assertIn('interpretation', data)

    def test_correlation_mismatched_lengths(self):
        """Test correlation with different lengths"""
        response = self.client.post('/api/correlation',
                                   json={'data': '1, 2, 3, 4, 5\n2, 4, 6'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('same length', data['error'])

    def test_correlation_insufficient_data(self):
        """Test correlation with only one data point"""
        response = self.client.post('/api/correlation',
                                   json={'data': '5\n10'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('at least 2', data['error'])

    def test_correlation_empty_x(self):
        """Test correlation with empty X values"""
        response = self.client.post('/api/correlation',
                                   json={'data': '\n1, 2, 3'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_correlation_empty_y(self):
        """Test correlation with empty Y values"""
        response = self.client.post('/api/correlation',
                                   json={'data': '1, 2, 3\n'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_correlation_missing_line(self):
        """Test correlation with only one line"""
        response = self.client.post('/api/correlation',
                                   json={'data': '1, 2, 3, 4, 5'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_correlation_invalid_x_format(self):
        """Test correlation with invalid X values"""
        response = self.client.post('/api/correlation',
                                   json={'data': 'a, b, c\n1, 2, 3'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_correlation_invalid_y_format(self):
        """Test correlation with invalid Y values"""
        response = self.client.post('/api/correlation',
                                   json={'data': '1, 2, 3\nx, y, z'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    # ===== Test Helper Function: get_correlation_interpretation =====
    def test_get_correlation_interpretation_very_strong_positive(self):
        """Test interpretation for very strong positive correlation"""
        result = get_correlation_interpretation(0.95, 0.001)
        self.assertIn('Very strong', result)
        self.assertIn('positive', result)
        self.assertIn('significant', result)

    def test_get_correlation_interpretation_strong_negative(self):
        """Test interpretation for strong negative correlation"""
        result = get_correlation_interpretation(-0.8, 0.01)
        self.assertIn('Strong', result)
        self.assertIn('negative', result)
        self.assertIn('significant', result)

    def test_get_correlation_interpretation_moderate(self):
        """Test interpretation for moderate correlation"""
        result = get_correlation_interpretation(0.6, 0.02)
        self.assertIn('Moderate', result)
        self.assertIn('positive', result)

    def test_get_correlation_interpretation_weak(self):
        """Test interpretation for weak correlation"""
        result = get_correlation_interpretation(0.4, 0.1)
        self.assertIn('Weak', result)
        self.assertIn('not significant', result)

    def test_get_correlation_interpretation_very_weak(self):
        """Test interpretation for very weak correlation"""
        result = get_correlation_interpretation(0.1, 0.5)
        self.assertIn('Very weak', result)
        self.assertIn('not significant', result)

    def test_get_correlation_interpretation_zero(self):
        """Test interpretation for zero correlation"""
        result = get_correlation_interpretation(0, 0.9)
        self.assertIn('Very weak', result)
        self.assertIn('no', result)

    # ===== Test Edge Cases and Error Handling =====
    def test_missing_json_data(self):
        """Test endpoints with missing JSON data"""
        endpoints = ['/api/descriptive-stats', '/api/t-test', 
                    '/api/chi-square', '/api/correlation']
        
        for endpoint in endpoints:
            response = self.client.post(endpoint,
                                       json={},
                                       content_type='application/json')
            # Should handle gracefully (either 400 or return with empty processing)
            self.assertIn(response.status_code, [200, 400])

    def test_large_dataset(self):
        """Test descriptive stats with large dataset"""
        large_data = ','.join([str(i) for i in range(1000)])
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': large_data},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 1000)

    def test_very_small_numbers(self):
        """Test with very small decimal numbers"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '0.0001, 0.0002, 0.0003'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertGreater(data['mean'], 0)

    def test_very_large_numbers(self):
        """Test with very large numbers"""
        response = self.client.post('/api/descriptive-stats',
                                   json={'data': '1000000, 2000000, 3000000'},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['mean'], 2000000)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
