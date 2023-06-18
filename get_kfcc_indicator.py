from typing import Final, Dict
import requests
from bs4 import BeautifulSoup
import json
import re

URL: Final = 'https://kfcc.co.kr/gumgo/gum0301_view_new.do'

headers: Dict = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '161',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '',
    'DNT': '1',
    'Host': 'kfcc.co.kr',
    'Origin': 'https://kfcc.co.kr',
    'Referer': 'https://kfcc.co.kr/gumgo/regulardisclosure.do',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}

payload: Dict = {
    'procGbcd': '1',
    'pageNo': '',
    'gongsiGmgoid': '',
    'gmgocd': '0101',
    'hpageBrwsUm': '1',
    'gongsiDate': '',
    'strd_yymm': '202212',
    'gmgoNm': '',
    'gonsiYear': '2022',
    'gonsiMonth': '12'
}


def get_bank_code_info():
    with open('bank_code_info.json', encoding='UTF-8') as file:
        bank_infos = json.load(file)
        return {bank_info['gmgoCd']: bank_info['name'] for bank_info in bank_infos}


def get_page_source():
    request_object = requests.post(URL, headers=headers, data=payload)
    return request_object.text


def get_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_raw_data(soup):
    return soup.select_one('#contentsdata')['value']


def process_raw_data(raw_data):
    lines = re.split(r'\s{100,}', raw_data)
    processed_data = {}

    for line in lines:
        address = line[:8].strip()
        content = line[8:].strip()

        if address == '0000':
            break

        processed_data[address] = content

    return processed_data


def get_indicator(processed_raw_data):
    def extract_indicator(processed_raw_data, address):
        return processed_raw_data.get(address, '').split('|')[2]

    return {
        "위험가중자산대비 자기자본비율": extract_indicator(processed_raw_data, '25000001'),
        "순고정이하 여신비율": extract_indicator(processed_raw_data, '25000005'),
        "유동성 비율": extract_indicator(processed_raw_data, '25000007'),
        "총자산 순이익률": extract_indicator(processed_raw_data, '25000009'),
        "경영실태 평가": extract_indicator(processed_raw_data, '31000001'),
    }


def main():
    # print(get_bank_code_info())
    html = get_page_source()
    soup = get_soup(html)
    raw_data = get_raw_data(soup)
    with open('t.txt', 'w', encoding='UTF-8') as file:
        json.dump(raw_data, file, ensure_ascii=False, indent=4)
    processed_raw_data = process_raw_data(raw_data)
    print(get_indicator(processed_raw_data))


if __name__ == '__main__':
    main()
