from src.base_api_client import BaseHarborApiClient
from datetime import datetime
import json
import re


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
        return json.dumps(response, indent=4)

    async def delete_artifact(self, api_url, _page: int = 1, days_threshold_for_deletion: int = 30):
        collated_delete_response = []
        list_of_artifacts = await self.get_artifacts(api_url)
        if "digest" in list_of_artifacts:
            json_of_artifacts = json.loads(list_of_artifacts)
            base_harbor_client = BaseHarborApiClient(auth=self.auth)
            for artifact in json_of_artifacts:
                digest_of_artifact = artifact["digest"]
                if artifact["tags"]:
                    for tag in artifact["tags"]:
                        if ((datetime.now().date() - (datetime.fromisoformat(tag["push_time"])).date()).days
                                >= days_threshold_for_deletion):
                            collated_delete_response.append(f"Deleting tag: {tag["name"]}")
                            delete_api_url = (f"{re.sub(r"\?.*", "", api_url)}/"
                                              f"{str(digest_of_artifact).replace(":", "%3A")}"
                                              f"/tags/{tag["name"]}")
                            response = await base_harbor_client.harbor_delete(api_url=delete_api_url)
                            collated_delete_response.append(response)
                        else:
                            collated_delete_response.append(f"No tags found that are older than "
                                                            f"{days_threshold_for_deletion} days")
                else:
                    collated_delete_response.append(
                        f"No tags found for artifact with digest: {str(digest_of_artifact)}.")
        else:
            collated_delete_response.append(
                f"No artifact found to process older than {days_threshold_for_deletion} days.")
        return collated_delete_response
