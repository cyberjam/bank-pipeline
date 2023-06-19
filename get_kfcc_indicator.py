import json
import re
import requests
from bs4 import BeautifulSoup
from constants import INDICATOR_URL, INDICATOR_HEADERS, INDICATOR_PAYLOAD


def get_bank_code_info():
    with open('bank_code_info.json', encoding='UTF-8') as file:
        bank_infos = json.load(file)
        return {bank_info['gmgoCd']: bank_info['name'] for bank_info in bank_infos}


def get_page_source():
    INDICATOR_PAYLOAD['gmgocd'] = '0101'
    request_object = requests.post(
        INDICATOR_URL, headers=INDICATOR_HEADERS, data=INDICATOR_PAYLOAD)
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
    processed_raw_data = process_raw_data(raw_data)
    print(get_indicator(processed_raw_data))


if __name__ == '__main__':
    main()
