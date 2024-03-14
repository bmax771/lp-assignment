import httpx
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


class BaseHarborApiClient:

    def __init__(self, auth: tuple, headers=None) -> None:
        self.auth = auth
        self.headers = headers

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(httpx.ConnectTimeout),
        retry_error_callback=lambda retry_state: "GET REQUEST FAILED",
    )
    async def harbor_get(self, api_url, params: dict = None, headers: dict = None) -> dict:
        response = {}
        client = httpx.AsyncClient()
        try:
            response = await client.get(api_url, params=params, auth=self.auth, headers=headers)
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Error in calling GET API: {e}")
            return {}
        finally:
            await client.aclose()
            return response

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(httpx.ConnectTimeout),
        retry_error_callback=lambda retry_state: "GET REQUEST FAILED",
    )
    async def harbor_delete(self, params: dict = None, headers: dict = None) -> dict:
        response = {}
        client = httpx.AsyncClient()
        try:
            response = await client.delete(self.api_url, params=params, auth=self.auth, headers=headers)
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Error in calling DELETE API: {e}")
            return {}
        finally:
            await client.aclose()
            return response

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(httpx.ConnectTimeout),
        retry_error_callback=lambda retry_state: "GET REQUEST FAILED",
    )
    async def harbor_delete(self, params: dict = None, headers: dict = None, data: dict = None) -> dict:
        response = {}
        client = httpx.AsyncClient()
        try:
            response = await client.post(self.api_url, params=params, auth=self.auth, headers=headers, data=data)
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Error in calling POST API: {e}")
            return {}
        finally:
            await client.aclose()
            return response
