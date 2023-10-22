from typing import Any, Optional

import httpx
from pydantic import BaseModel, Field

from ..utils import retry, setup_logging

logger = setup_logging(__name__)


class APIClient(BaseModel):
    """
    A class representing an API client.

    Attributes:
    -----------
    headers : dict
        The headers to be used for the API requests.
    base_url : str
        The base URL for the API requests.
    """

    base_url: str = Field(..., description="The base URL for the API requests")
    headers: dict[str, str] = Field(
        ..., description="The headers to be used for the API requests"
    )

    @property
    def client(self):
        """
        Returns an HTTPX client object.

        Returns:
        --------
        httpx.AsyncClient
            An HTTPX client object.
        """
        return httpx.AsyncClient(base_url=self.base_url, headers=self.headers)

    @retry()
    async def get(self, endpoint: str, params: Optional[dict[str, Any]] = None):
        """
        Sends a GET request to the API.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.
        params : Optional[dict[str, Any]]
            The query parameters to be used for the request.

        Returns:
        --------
        dict
            The response from the API.
        """
        try:
            response = await self.client.get(endpoint, params=params)
            data = response.json()
            logger.info(f"GET {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"GET {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def post(self, endpoint: str, data: Optional[dict[str, Any]] = None):
        """
        Sends a POST request to the API.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.
        data : Optional[dict[str, Any]]
            The data to be sent with the request.

        Returns:
        --------
        dict
            The response from the API.
        """
        try:
            response = await self.client.post(endpoint, json=data)
            data = response.json()
            logger.info(f"POST {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"POST {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def put(self, endpoint: str, data: Optional[dict[str, Any]] = None):
        """
        Sends a PUT request to the API.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.
        data : Optional[dict[str, Any]]
            The data to be sent with the request.

        Returns:
        --------
        dict
            The response from the API.
        """
        try:
            response = await self.client.put(endpoint, json=data)
            data = response.json()
            logger.info(f"PUT {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"PUT {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def delete(self, endpoint: str):
        """
        Sends a DELETE request to the API.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.

        Returns:
        --------
        dict
            The response from the API.
        """
        try:
            response = await self.client.delete(endpoint)
            data = response.json()
            logger.info(f"DELETE {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"DELETE {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def patch(self, endpoint: str, data: Optional[dict[str, Any]] = None):
        """
        Sends a PATCH request to the API.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.
        data : Optional[dict[str, Any]]
            The data to be sent with the request.

        Returns:
        --------
        dict
            The response from the API.
        """
        try:
            response = await self.client.patch(endpoint, json=data)
            data = response.json()
            logger.info(f"PATCH {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"PATCH {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def head(self, endpoint: str):
        """
        Sends a HEAD request to the API.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.

        Returns:
        --------
        dict
            The response from the API.
        """
        try:
            response = await self.client.head(endpoint)
            data = response.json()
            logger.info(f"HEAD {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"HEAD {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def options(self, endpoint: str):
        """
        Sends an OPTIONS request to the API.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.

        Returns:
        --------
        dict
            The response from the API.
        """
        try:
            response = await self.client.options(endpoint)
            data = response.json()
            logger.info(f"OPTIONS {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"OPTIONS {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def trace(self, endpoint: str):
        """
        Sends a TRACE request to the API.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.

        Returns:
        --------
        dict
            The response from the API.
        """
        try:
            response = await self.client.trace(endpoint)
            data = response.json()
            logger.info(f"TRACE {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"TRACE {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def text(self, endpoint: str, params: Optional[dict[str, Any]] = None):
        """
        Sends a GET request to the API and returns the response as text.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.

        Returns:
        --------
        str
            The response from the API.
        """
        try:
            response = await self.client.get(endpoint, params=params)
            data = response.text
            logger.info(f"GET {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"GET {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    @retry()
    async def blob(self, endpoint: str, params: Optional[dict[str, Any]] = None):
        """
        Sends a GET request to the API and returns the response as bytes.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.

        Returns:
        --------
        bytes
            The response from the API.
        """
        try:
            response = await self.client.get(endpoint, params=params)
            data = response.content
            logger.info(f"GET {endpoint} {response.status_code} {data}")
            return data
        except Exception as e:
            logger.error(f"GET {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()

    async def stream(self, endpoint: str, params: Optional[dict[str, Any]] = None):
        """
        Sends a GET request to the API and returns the response as a stream.

        Parameters:
        -----------
        endpoint : str
            The endpoint to send the request to.

        Returns:
        --------
        httpx.AsyncIterator[bytes]
            The response from the API.
        """
        try:
            async with self.client.stream("GET", endpoint, params=params) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
        except Exception as e:
            logger.error(f"GET {endpoint} {e}")
            raise e
        finally:
            await self.client.aclose()
