from src.base_api_client import BaseHarborApiClient


class ArtifactApiClient(BaseHarborApiClient):
    """
        Class for artifacts handling.

        Inherits from BaseHarborApiClient
    """

    def __init__(self, auth):
        self.auth = auth

    async def get_artifacts(self, api_url, _page: int = 1):
        """
            Gets list of artifacts from the registry for a given project and repository

            Args:
                api_url (str): URL with query string for Artifacts API call
                _page (int, optional): Page number to retrieve.

            Returns:
                collated_response (list): List of Artifacts across all pages.
        """
        base_harbor_client = BaseHarborApiClient(auth=self.auth)
        response = await base_harbor_client.harbor_paginated_get(api_url=api_url, _page=_page)
        return response

    async def delete_artifact(self, api_url, _page: int = 1):
        list_of_artifacts = await self.get_artifacts(api_url)
