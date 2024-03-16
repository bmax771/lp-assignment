from src.base_api_client import BaseHarborApiClient


class RepositoryApiClient(BaseHarborApiClient):
    """
        Class for repository handling.

        Inherits from BaseHarborApiClient
    """

    def __init__(self, auth):
        self.auth = auth

    async def get_all_authorized_repos(self, api_url, _page: int = 1):
        """
            Gets list of repositories the user is authorized to see/read.

            Args:
                api_url (str): URL with query string for Repositories API call
                _page (int, optional): Page number to retrieve.

            Returns:
                collated_response (list): List of Repositories across all pages.
        """
        base_harbor_client = BaseHarborApiClient(auth=self.auth)
        response = await base_harbor_client.harbor_paginated_get(api_url=api_url, _page=_page)
        return response

    async def get_specific_project_repos(self, api_url, _page: int = 1):
        """
            Gets list of repositories for a given project

            Args:
                api_url (str): URL with query string for Repositories API call
                _page (int, optional): Page number to retrieve.

            Returns:
                collated_response (list): List of Repositories across all pages.
        """
        base_harbor_client = BaseHarborApiClient(auth=self.auth)
        response = await base_harbor_client.harbor_paginated_get(api_url=api_url, _page=_page)
        return response
