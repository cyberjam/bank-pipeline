import requests


def fetch_page_source(url='', method='', params=None, headers=None, data=None):
    """페이지 소스코드를 반환합니다.
    Args:
        url (string): _description_
        method (string): _description_
        params (dictionary, optional): _description_. Defaults to None.
        headers (dictionary, optional): _description_. Defaults to None.
        data (dictionary, optional): _description_. Defaults to None.

    Returns:
        string: _description_
    """

    response = requests.request(method,
                                url,
                                params=params,
                                headers=headers,
                                data=data)
    return response.text
