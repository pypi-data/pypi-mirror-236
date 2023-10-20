from dataclasses import dataclass
from typing import Dict, Iterator

import requests

from .serializers import IrusReportItem


@dataclass
class IrusClient:
    """Single entry point to the IRUS API."""

    base_url: str
    requestor_id: str
    platform: int
    api_key: str | None = None
    metric_type: str = 'Unique_Item_Requests'

    def __post_init__(self):
        self.base_parameters = dict(
            requestor_id=self.requestor_id,
            platform=self.platform,
            metric_type=self.metric_type,
            attributes_to_show='Country'
        )
        if self.api_key is not None:
            self.base_parameters.update(api_key=self.api_key)

    def fetch_report_json(
            self,
            report_path: str,
            begin_date: str,
            end_date: str
    ) -> Dict:
        """Make a get request to the IRUS-UK API and return the JSON response.

        Args:
            report_path (str): API endpoint to query.
            begin_date (str): Usage start date in the form of yyyy-mm.
            end_date (str): Usage end date in the form of yyyy-mm.

        Returns:
            dict: JSON representation of the report.
        """
        parameters = self.base_parameters.copy()
        parameters.update(begin_date=begin_date, end_date=end_date)
        url = f'{self.base_url}/{report_path.strip("/")}'
        response = requests.get(url, params=parameters)

        if response.status_code != 200:
            response.raise_for_status()

        return response.json()


def has_required_settings(**kwargs) -> bool:
    """Helper function to check if the required kwargs are available to pass
     to the fetch_processed_report() function.
     """
    required_settings = {
        'base_url',#
        'report_path',
        'platform',#
        'requestor_id',#
        'begin_date',
        'end_date'
    }
    kwargs.pop('api_key', None)

    return set(kwargs.keys()) == required_settings


def fetch_processed_report(
        base_url: str,
        requestor_id: str,
        platform: int,
        report_path: str,
        begin_date: str,
        end_date: str,
        api_key: str | None = None,
) -> Iterator[IrusReportItem]:
    """Make a get request to the IRUS-UK API and return a processed report.

    Only works for the 'Unique_Item_Requests' metric type.

    Args:
        base_url (str): IRUS API base URL to use.
        platform (int): IRUS identifier of the repository.
        requestor_id (str): UUID showing who is making the request.
        report_path (str): API endpoint to query.
        begin_date (str): Usage start date in the form of yyyy-mm.
        end_date (str): Usage end date in the form of yyyy-mm.
        api_key (str): UUID Key to Confirm identity of requestor (OAPEN-only).

    Yields:
        IrusReportItem: Serialized IRUS-UK report items.
    """
    client = IrusClient(
        base_url=base_url,
        platform=platform,
        requestor_id=requestor_id,
        api_key=api_key,
    )
    response = client.fetch_report_json(report_path, begin_date, end_date)

    for item in filter(lambda x: 'DOI' in x, response['Report_Items']):
        yield IrusReportItem(**item)
