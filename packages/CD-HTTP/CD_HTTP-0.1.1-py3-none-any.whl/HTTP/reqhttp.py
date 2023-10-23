import requests

class HTTP:
    """
    A simple HTTP client class to handle various HTTP requests using the `requests` library.
    For a detailed list of available keyword arguments, refer to:
    https://docs.python-requests.org/en/latest/api/#requests.request
    """

    def __init__(self):
        """Initialize a new HTTP client session."""
        self.session = requests.Session()

    def get(self, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Send a GET request to the specified URL.

        :param url: The URL to request.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments supported by `requests.get()`.
        :return: Response object.
        """
        return self._request("GET", url, user_agent, proxy, proxy_username, proxy_password, **kwargs)

    def post(self, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Send a POST request to the specified URL.

        :param url: The URL to request.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments supported by `requests.post()`.
        :return: Response object.
        """
        return self._request("POST", url, user_agent, proxy, proxy_username, proxy_password, **kwargs)

    def put(self, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Send a PUT request to the specified URL.

        :param url: The URL to request.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments supported by `requests.put()`.
        :return: Response object.
        """
        return self._request("PUT", url, user_agent, proxy, proxy_username, proxy_password, **kwargs)

    def patch(self, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Send a PATCH request to the specified URL.

        :param url: The URL to request.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments supported by `requests.patch()`.
        :return: Response object.
        """
        return self._request("PATCH", url, user_agent, proxy, proxy_username, proxy_password, **kwargs)

    def delete(self, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Send a DELETE request to the specified URL.

        :param url: The URL to request.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments supported by `requests.delete()`.
        :return: Response object.
        """
        return self._request("DELETE", url, user_agent, proxy, proxy_username, proxy_password, **kwargs)

    def head(self, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Send a HEAD request to the specified URL.

        :param url: The URL to request.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments supported by `requests.head()`.
        :return: Response object.
        """
        return self._request("HEAD", url, user_agent, proxy, proxy_username, proxy_password, **kwargs)

    def options(self, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Send an OPTIONS request to the specified URL.

        :param url: The URL to request.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments supported by `requests.options()`.
        :return: Response object.
        """
        return self._request("OPTIONS", url, user_agent, proxy, proxy_username, proxy_password, **kwargs)


    def _request(self, method, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Internal method to handle HTTP requests.

        :param method: The HTTP method (e.g., "GET", "POST").
        :param url: The URL to request.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments.
        :return: Response object.
        """
        DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        HEADERS = {
            "User-Agent": user_agent if user_agent else DEFAULT_USER_AGENT
        }

        # Merge with additional headers if provided
        if 'headers' in kwargs:
            HEADERS.update(kwargs['headers'])
            del kwargs['headers']

        if proxy and proxy_username and proxy_password:
            PROXIES = {
                "http": f"http://{proxy_username}:{proxy_password}@{proxy}",
                "https": f"https://{proxy_username}:{proxy_password}@{proxy}"
            }
        elif proxy:
            PROXIES = {
                "http": proxy,
                "https": proxy
            }
        else:
            PROXIES = None

        try:
            response = self.session.request(method, url, headers=HEADERS, proxies=PROXIES, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as err:
            print(f"Error making {method} request to {url}: {err}")
            return None
        except Exception as err:
            print(f"Unexpected error: {err}")
            return None

    def download_file(self, file_name_path, url, user_agent=None, proxy=None, proxy_username=None, proxy_password=None, **kwargs):
        """
        Download a file from the specified URL.

        :param file_name_path: Path to save the downloaded file.
        :param url: The URL of the file to download.
        :param user_agent: Optional user agent string. Defaults to a popular browser's user agent.
        :param proxy: Optional proxy URL.
        :param proxy_username: Optional proxy authentication username.
        :param proxy_password: Optional proxy authentication password.
        :param kwargs: Other optional keyword arguments supported by `requests.get()`.
        """
        response = self.get(url, user_agent=user_agent, proxy=proxy, proxy_username=proxy_username, proxy_password=proxy_password, stream=True, **kwargs)
        if response:
            with open(file_name_path, 'wb') as handle:
                for block in response.iter_content(1024):
                    handle.write(block)

    def start_session(self):
        """Start a new persistent session."""
        self.session = requests.Session()

    def close_session(self):
        """Close the current session."""
        self.session.close()

