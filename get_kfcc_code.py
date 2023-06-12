from typing import Final, Dict
import requests

REGION: Final = ('서울', '인천', '경기', '강원', '충남', '충북', '대전', '경북',
                 '경남', '대구', '부산', '울산', '전북', '전남', '광주', '제주', '세종')
URL: Final = 'https://www.kfcc.co.kr/map/list.do'

headers: Dict = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


def main():
    """main 실행함수"""
    for region_name in REGION:
        params = {'r1': region_name, 'r2': ''}
        request_object = requests.get(URL, params=params, headers=headers)
        print(request_object.text)


if __name__ == '__main__':
    main()
