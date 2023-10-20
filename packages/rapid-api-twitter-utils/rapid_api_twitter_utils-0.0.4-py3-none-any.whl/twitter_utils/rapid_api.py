import requests
from decouple import config


def rapid_api_request(url: str, query: dict, *args, **kwargs) -> requests.Response:
    """
    Makes a request to the Twitter API.

    :param url: The URL of the API endpoint.
    :param query: The query parameters to pass to the API.
    :return: The response from the API.
    :rtype: requests.Response
    """

    RAPID_API_HEADERS = {
        "X-RapidAPI-Key": config("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "twitter135.p.rapidapi.com",
    }

    return requests.get(
        url=url,
        headers=RAPID_API_HEADERS,
        params=query,
        *args,
        **kwargs,
    )
