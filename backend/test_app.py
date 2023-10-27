from page import app
import unittest

class TestApp(unittest.TestCase):
    def test_app_runs_without_errors(self):
        # Create a test client
        client = app.test_client()

        # Send a GET request to the home page
        response = client.get('/')

        # Check if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()