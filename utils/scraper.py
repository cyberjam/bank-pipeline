import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.session = requests.Session()

    def fetch_page_source(self, method='', url='', params=None, headers=None, data=None):
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

        response = self.session.request(method,
                                        url,
                                        params=params,
                                        headers=headers,
                                        data=data)
        return response.text

    def create_soup(self, html):
        """html을 beautifulsoup로 parsing하여 객체로 반환합니다.

        Args:
            html (string): 페이지를 request하여 받은 page source code

        Returns:
            bs4.BeautifulSoup: html을 beutifulsoup으로 parsing 한 soup 객체
        """
        return BeautifulSoup(html, 'html.parser')
