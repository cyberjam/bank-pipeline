import json
import re
from tqdm import tqdm
from constants import BANK_INDICATOR_CONSTANT, GLOBAL_CONSTANT
from utils.save_json import save_json
from utils.create_soup import create_soup
from utils.fetch_page_source import fetch_page_source


def get_bank_code_info():
    with open(GLOBAL_CONSTANT['CODE_JSON_PATH'], encoding='UTF-8') as file:
        bank_infos = json.load(file)
        return {bank_info['gmgoCd']: bank_info['name'] for bank_info in bank_infos}


def get_payload(bank_code):
    payload = BANK_INDICATOR_CONSTANT['PAYLOAD']
    payload['gmgocd'] = bank_code
    return payload


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
        payload = get_payload(bank_code)
        html = fetch_page_source(method='POST',
                                 url=BANK_INDICATOR_CONSTANT['URL'],
                                 headers=BANK_INDICATOR_CONSTANT['HEADERS'],
                                 data=payload)
        soup = create_soup(html)
        raw_data = get_raw_data(soup)
        processed_raw_data = process_raw_data(raw_data)
        yield integrate_indicator(processed_raw_data, bank_code, bank_name)


def main():
    bank_indicator = list(get_indicator())
    save_json(GLOBAL_CONSTANT['INDICATOR_JSON_PATH'], bank_indicator)


if __name__ == '__main__':
    main()
