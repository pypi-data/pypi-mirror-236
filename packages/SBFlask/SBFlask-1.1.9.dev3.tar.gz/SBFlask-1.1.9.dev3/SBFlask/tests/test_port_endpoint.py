import json
import unittest
from ..FlaskMain import app, set_frigg_responses  # Import your Flask app


class TestKodiakEndpointPort(unittest.TestCase):
    def setUp(self):
        set_frigg_responses(True)
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_get_port_endpoint_with_valid_ip(self):
        # Test the endpoint with a valid IP address
        ip_address = "192.168.1.247"
        response = self.app.get(f'/kodiak/port?ipaddress={ip_address}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Success', data)

    def test_get_port_endpoint_with_bad_format_ip(self):
        # Test the endpoint with a valid IP address
        ip_address = "192.168.1.247."
        response = self.app.get(f'/kodiak/port?ipaddress={ip_address}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Badly formatted IP address value")

    def test_get_port_endpoint_with_bad_no_ip(self):
        # Test the endpoint with a valid IP address
        ip_address = ""
        response = self.app.get(f'/kodiak/port?ipaddress={ip_address}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Badly formatted IP address value")

    def test_get_port_endpoint_with_bad_args(self):
        # Test the endpoint with a valid IP address
        ip_address = ""
        response = self.app.get(f'/kodiak/port?test={ip_address}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Request missing ipaddress argument")

    def test_get_port_endpoint_with_missing_ip(self):
        # Test the endpoint with a missing IP address
        response = self.app.get('/kodiak/port')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Request missing args")


if __name__ == '__main__':
    unittest.main()