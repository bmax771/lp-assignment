import httpx
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import time


class BaseHarborApiClient:
    """
        Class for REST API functions.

        Main parent class.
    """

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
        """
            GET API for executing get REST API call on Harbor client

            Args:
                api_url: URL to execute API on. Note that URL will contain queries as well.
                params (dict, optional): parameters for API request
                headers (dict, optional): headers for API request

            Returns:
                response (class): Response of API
        """
        response = {}
        try:
            async with httpx.AsyncClient() as client:
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
        retry_error_callback=lambda retry_state: "PAGINATED GET REQUEST FAILED",
    )
    async def harbor_paginated_get(self, api_url, _page=1) -> dict:
        """
            Paginated GET API for executing get REST API call on Harbor client

            Args:
                api_url: URL to execute API on. Note that URL will contain queries as well.
                _page (int, optional): Internal parameter. Page number to read.

            Returns:
                collated_response (dict): Response of API after reading all pages.
        """
        paginated_url = api_url.replace(f"page={_page - 1}", f"page={str(_page)}")

        collated_response = await self.harbor_get(api_url=paginated_url)

        if not collated_response:
            return collated_response
        elif collated_response.status_code == 200:
            if "Link" not in collated_response.headers:
                return collated_response.json()
            elif "Link" in collated_response.headers:
                _page += 1
                return collated_response.json() + await self.harbor_paginated_get(paginated_url,
                                                                                  _page)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type(httpx.ConnectTimeout),
        retry_error_callback=lambda retry_state: "DELETE REQUEST FAILED",
    )
    async def harbor_delete(self, api_url, params: dict = None, headers: dict = None) -> dict:
        """
            DELETE API for executing delete REST API call on Harbor client

            Args:
                api_url: URL to execute API on. Note that URL will contain queries as well.
                params (dict, optional): parameters for API request
                headers (dict, optional): headers for API request

            Returns:
                response (class): Response of API
        """
        response = {}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(api_url, params=params, auth=self.auth, headers=headers)
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
        retry_error_callback=lambda retry_state: "POST REQUEST FAILED",
    )
    async def harbor_post(self, api_url, params: dict = None, headers: dict = None, data: dict = None) -> dict:
        """
            POST API for executing post REST API call on Harbor client

            Args:
                api_url (string): URL to execute API on. Note that URL will contain queries as well.
                params (dict, optional): parameters for API request
                headers (dict, optional): headers for API request
                data (dict, optional): Data for POST API request.

            Returns:
                response (class): Response of API
        """
        response = {}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(api_url, params=params, auth=self.auth, headers=headers, data=data)
                response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Error in calling POST API: {e}")
            return {}
        finally:
            await client.aclose()
            return response
