from typing import Final, Dict
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

REGION: Final = ('서울', '인천', '경기', '강원', '충남', '충북', '대전', '경북',
                 '경남', '대구', '부산', '울산', '전북', '전남', '광주', '제주', '세종')
URL: Final = 'https://www.kfcc.co.kr/map/list.do'

headers: Dict = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


def get_page_source(region_name):
    """지역별 지점 목록을 나타내는 페이지 소스코드를 반환합니다.

    Args:
        region_name (string): 대한민국 광역, 자치, 도 단위 지역

    Returns:
        string: 해당 지역 지점 목록 html이 text로 반환
    """
    params = {'r1': region_name, 'r2': ''}
    response = requests.get(URL, params=params, headers=headers)
    return response.text


def get_soup(html):
    """html을 beautifulsoup로 parsing하여 객체로 반환합니다.

    Args:
        html (string): 전국 지점 목록 페이지를 request하여 받은 page source code

    Returns:
        bs4.BeautifulSoup: html을 beutifulsoup으로 parsing 한 soup 객체
    """
    return BeautifulSoup(html, 'html.parser')


def get_rows(soup):
    """table의 row들을 반환합니다.

    Args:
        soup (bs4.BeautifulSoup): html을 beutifulsoup으로 parsing 한 soup 객체
    Returns:
        bs4.element.ResultSet: table의 해당 row들
    """
    return soup.select("tr")


def get_cells(row):
    """각 지점 cells들을 반환합니다.

    Args:
        row (bs4.element.ResultSet): table의 해당 row

    Returns:
        bs4.element.ResultSet: table의 해당 row에 속한 cell들
    """
    return row.select("td.no")


def get_datas(cell):
    """지점 정보를 넘겨줍니다.

    Args:
        cell (bs4.element.ResultSet): table의 해당 row에서 각 cell

    Yields:
        tuple: dictionary의 key와 value
    """
    for data in cell.select("span"):
        yield data['title'], data.get_text()


def get_bank_info():
    """모든 지역 지점 정보를 넘겨줍니다.

    Yields:
        dictionary: 각 지점 정보
    """
    for region_name in tqdm(REGION):
        html = get_page_source(region_name)
        soup = get_soup(html)
        for row in get_rows(soup):
            for cell in get_cells(row):
                yield dict(get_datas(cell))


def save_json(file_path, data):
    """ 결과물을 json으로 저장

    Args:
        file_path (string): 저장할 위치와 저장 파일 이름
        data (generator): 결과물
    """
    with open(file_path, 'w', encoding='UTF-8') as file:
        json.dump(list(data), file, ensure_ascii=False, indent=4)


def main():
    """main 실행함수"""
    bank_info = get_bank_info()
    save_json('../data/bank_code_info.json', bank_info)


if __name__ == '__main__':
    main()
