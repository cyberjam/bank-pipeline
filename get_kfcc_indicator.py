import requests
from typing import Final, Dict
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


def get_bank_code():
    def preprecess_bank_infos(bank_infos):
        for bank_info in bank_infos:
            bank_code = bank_info['gmgoCd']
            bank_name = bank_info['name']
            yield bank_code, bank_name

    with open('bank_code_info.json', encoding='UTF-8') as file:
        bank_infos = json.load(file)
    return dict(preprecess_bank_infos(bank_infos))


def get_page_source():
    request_object = requests.post(URL, headers=headers, data=payload)
    return request_object.text


def get_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_data(soup):
    return soup.select_one('#contentsdata')['value']


def preprocess_data(raw_data):
    space = ' '*100
    type_last_index = 7
    splited_data = re.sub(f'{space}+', '\n', raw_data).split('\n')
    for line in splited_data:
        type_number = line[:type_last_index+1]
        content = line[type_last_index+1:]

        if type_number == '0000':
            break

        yield type_number, content


def get_indicator(preprocessed_data):
    data = dict(preprocessed_data)
    return data['25000001'].split('|')[2]


def main():
    print(get_bank_code())
    html = get_page_source()
    soup = get_soup(html)
    raw_data = get_data(soup)
    preprocessed_data = preprocess_data(raw_data)
    print(get_indicator(preprocessed_data))


if __name__ == '__main__':
    main()
