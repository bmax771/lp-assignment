from src.base_api_client import BaseHarborApiClient
import json

class ProjectApiClient(BaseHarborApiClient):
    """
        Class for projects handling.

        Inherits from BaseHarborApiClient
    """

    def __init__(self, auth):
        self.auth = auth

    async def get_projects(self, api_url, _page: int = 1):
        """
            Gets list of projects.

            Args:
                api_url (str): URL with query string for Artifacts API call
                _page (int, optional): Page number to retrieve.

            Returns:
                collated_response (list): List of Projects across all pages.
        """
        base_harbor_client = BaseHarborApiClient(auth=self.auth)
        response = await base_harbor_client.harbor_paginated_get(api_url=api_url, _page=_page)
        return json.dumps(response, indent=4)
