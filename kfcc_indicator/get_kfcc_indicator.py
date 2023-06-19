import json
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from constants import INDICATOR_URL, INDICATOR_HEADERS, INDICATOR_PAYLOAD


def get_bank_code_info():
    with open('../data/bank_code_info.json', encoding='UTF-8') as file:
        bank_infos = json.load(file)
        return {bank_info['gmgoCd']: bank_info['name'] for bank_info in bank_infos}


def get_page_source(bank_code):
    INDICATOR_PAYLOAD['gmgocd'] = bank_code
    request_object = requests.post(
        INDICATOR_URL, headers=INDICATOR_HEADERS, data=INDICATOR_PAYLOAD)
    return request_object.text


def get_soup(html):
    return BeautifulSoup(html, 'html.parser')


def get_raw_data(soup):
    contentsdata = soup.select_one('#contentsdata')
    if contentsdata is None:
        return ''
    return contentsdata['value']


def process_raw_data(raw_data):
    lines = re.split(r'\s{100,}', raw_data)
    processed_data = {}

    for line in lines:
        address = line[:8].strip()
        content = line[8:].strip()

        if address == '0000':
            break

        processed_data[address] = content.split('|')

    return processed_data


def extract_indicator(processed_raw_data, address):
    return processed_raw_data.get(address, f'{" "*3}')[2]


def integrate_indicator(processed_raw_data, bank_code, bank_name):
    return {
        "지점명": bank_name,
        "지점코드": bank_code,
        "위험가중자산대비 자기자본비율": extract_indicator(processed_raw_data, '25000001'),
        "순고정이하 여신비율": extract_indicator(processed_raw_data, '25000005'),
        "유동성 비율": extract_indicator(processed_raw_data, '25000007'),
        "총자산 순이익률": extract_indicator(processed_raw_data, '25000009'),
        "경영실태 평가": extract_indicator(processed_raw_data, '31000001'),
    }


def get_indicator():
    for bank_code, bank_name in tqdm(get_bank_code_info().items()):
        html = get_page_source(bank_code)
        soup = get_soup(html)
        raw_data = get_raw_data(soup)
        processed_raw_data = process_raw_data(raw_data)
        yield integrate_indicator(processed_raw_data, bank_code, bank_name)


def save_json(file_path, data):
    """ 결과물을 json으로 저장

    Args:
        file_path (string): 저장할 위치와 저장 파일 이름
        data (generator): 결과물
    """
    with open(file_path, 'w', encoding='UTF-8') as file:
        json.dump(list(data), file, ensure_ascii=False, indent=4)


def main():
    bank_indicator = list(get_indicator())
    save_json('../data/bank_indicator.json', bank_indicator)


if __name__ == '__main__':
    main()
