from src.base_api_client import BaseHarborApiClient


class ProjectApiClient(BaseHarborApiClient):
    def __init__(self, auth):
        super(BaseHarborApiClient, self).__init__()
        self.auth = auth

    async def get_projects(self, api_url, _page: int = 1):
        paginated_url = api_url.replace(f"page={_page-1}", f"page={str(_page)}")
        collated_response = await BaseHarborApiClient.harbor_get(self, paginated_url)

        if not collated_response:
            return collated_response
        elif collated_response.status_code == 200:
            if "Link" not in collated_response.headers:
                return collated_response.json()
            elif "Link" in collated_response.headers:
                _page += 1
                return collated_response.json() + await self.get_projects(paginated_url, _page)
