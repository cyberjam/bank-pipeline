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
    request_object = requests.get(URL, params=params, headers=headers)
    return request_object.text


def get_bank_info():
    """모든 지역 지점 정보를 반환합니다.

    Returns:
        list of dictionary: 전국 각 지점 정보를 dictionary로 list에 담아 반환
    """
    return [
        {data['title']: data.get_text() for data in cell.select("span")}
        for region_name in tqdm(REGION)
        for row in BeautifulSoup(get_page_source(region_name), 'html.parser').select("tr")
        for cell in row.select("td.no")
    ]


def main():
    """main 실행함수"""
    with open('bank_code_info.json', 'w', encoding='UTF-8') as file:
        json.dump(get_bank_info(), file, indent=4)


if __name__ == '__main__':
    main()
