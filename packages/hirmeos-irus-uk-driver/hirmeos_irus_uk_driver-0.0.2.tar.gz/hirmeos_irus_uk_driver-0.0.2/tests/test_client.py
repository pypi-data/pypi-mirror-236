from unittest import TestCase
from unittest.mock import patch, Mock
from src.irus_uk_driver.client import (
    IrusClient,
    has_required_settings,
)


class MockIrusReportItem:
    """Mock the IrusReportItem object from the serializer."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TestClient(TestCase):
    def setUp(self) -> None:
        self.init_class = IrusClient(
            base_url="https://irus.test.uk/api/v3/oapen",
            platform=215,
            requestor_id="test_requestor_id",
            api_key="test_api_key",
        )

    @patch("requests.get")
    def test_fetch_report_json_success_request(self, mock_get: Mock) -> None:
        """Test a successful response"""
        # Set up a mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "mocked_data"}
        mock_get.return_value = mock_response

        # Call the method to be tested
        result = self.init_class.fetch_report_json(
            "test/path", begin_date="start_date", end_date="end_date"
        )

        self.assertEqual(result, {"result": "mocked_data"})

    @patch("requests.get")
    def test_fetch_report_json_unsuccessful_request(self, mock_get: Mock) -> None:
        """Check the unsuccessful response raises for status"""
        # Set up a mock response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"result": "mocked_data"}
        mock_get.return_value = mock_response

        self.init_class.fetch_report_json(
            "test/path", begin_date="start_date", end_date="end_date"
        )
        # Assert that response.raise_for_status() was called
        mock_response.raise_for_status.assert_called_once()

    def test_has_required_settings_successful_and_fail(self) -> None:
        """Test both cases where it pass (correct settings) and then
        it fails with the wrong settings."""
        settings = {
            "base_url": "https://test-irus/v3/irus",
            "report_path": "reports/irus_ir",
            "platform": 123,
            "requestor_id": "",
            "begin_date": "2023-01-31",
            "end_date": "2023-02-31",
            "api_key": 12345,
        }
        self.assertEqual(has_required_settings(**settings), True)

        settings["WRONG_KEY"] = "TEST-WRONG"
        self.assertEqual(has_required_settings(**settings), False)
