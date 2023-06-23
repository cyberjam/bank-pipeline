from tqdm import tqdm
from constants import BANK_CODE_CONSTANT, GLOBAL_CONSTANT
from utils import scraper, write_json


def build_params(region_name):
    params = BANK_CODE_CONSTANT['PARAMS']
    params['r1'] = region_name
    return params


def extract_rows(soup):
    """table의 row들을 반환합니다.

    Args:
        soup (bs4.BeautifulSoup): html을 beutifulsoup으로 parsing 한 soup 객체
    Returns:
        bs4.element.ResultSet: table의 해당 row들
    """
    return soup.select("tr")


def extract_cells(row):
    """각 지점 cells들을 반환합니다.

    Args:
        row (bs4.element.ResultSet): table의 해당 row

    Returns:
        bs4.element.ResultSet: table의 해당 row에 속한 cell들
    """
    return row.select("td.no")


def extract_data(cell):
    """지점 정보를 넘겨줍니다.

    Args:
        cell (bs4.element.ResultSet): table의 해당 row에서 각 cell

    Yields:
        tuple: dictionary의 key와 value
    """
    for data in cell.select("span"):
        yield data['title'], data.get_text()


def fetch_bank_info():
    """모든 지역 지점 정보를 넘겨줍니다.

    Yields:
        dictionary: 각 지점 정보
    """
    for region_name in tqdm(BANK_CODE_CONSTANT['REGION']):
        params = build_params(region_name)
        html = scraper.fetch_page_source(method='GET',
                                         url=BANK_CODE_CONSTANT['URL'],
                                         headers=BANK_CODE_CONSTANT['HEADERS'],
                                         params=params)
        soup = scraper.create_soup(html)
        for row in extract_rows(soup):
            for cell in extract_cells(row):
                yield dict(extract_data(cell))


def main():
    """main 실행함수"""
    bank_info = list(fetch_bank_info())
    write_json(GLOBAL_CONSTANT['CODE_JSON_PATH'], bank_info)


if __name__ == '__main__':
    main()
