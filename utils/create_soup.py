from bs4 import BeautifulSoup


def create_soup(html):
    """html을 beautifulsoup로 parsing하여 객체로 반환합니다.

    Args:
        html (string): 페이지를 request하여 받은 page source code

    Returns:
        bs4.BeautifulSoup: html을 beutifulsoup으로 parsing 한 soup 객체
    """
    return BeautifulSoup(html, 'html.parser')
