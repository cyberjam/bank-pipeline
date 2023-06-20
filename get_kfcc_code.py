import requests
from tqdm import tqdm
from constants import BANK_CODE_CONSTANT, GLOBAL_CONSTANT
from utils.save_json import save_json
from utils.create_soup import create_soup


def get_page_source(region_name):
    """지역별 지점 목록을 나타내는 페이지 소스코드를 반환합니다.

    Args:
        region_name (string): 대한민국 광역, 자치, 도 단위 지역

    Returns:
        string: 해당 지역 지점 목록 html이 text로 반환
    """
    params = {'r1': region_name, 'r2': ''}
    response = requests.get(
        BANK_CODE_CONSTANT['URL'], params=params, headers=BANK_CODE_CONSTANT['HEADERS'])
    return response.text


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
    for region_name in tqdm(BANK_CODE_CONSTANT['REGION']):
        html = get_page_source(region_name)
        soup = create_soup(html)
        for row in get_rows(soup):
            for cell in get_cells(row):
                yield dict(get_datas(cell))


def main():
    """main 실행함수"""
    bank_info = list(get_bank_info())
    save_json(GLOBAL_CONSTANT['CODE_JSON_PATH'], bank_info)


if __name__ == '__main__':
    main()
