import json
import re
from tqdm import tqdm
import pandas as pd
import gspread
from constants import BANK_INDICATOR_CONSTANT, GLOBAL_CONSTANT
from utils import scraper


def load_bank_code_info():
    with open(GLOBAL_CONSTANT['CODE_JSON_PATH'], encoding='UTF-8') as file:
        bank_infos = json.load(file)
        return {bank_info['gmgoCd']: bank_info['name'] for bank_info in bank_infos}


def build_payload(bank_code):
    payload = BANK_INDICATOR_CONSTANT['PAYLOAD']
    payload['gmgocd'] = bank_code
    return payload


def extract_raw_data(soup):
    contentsdata = soup.select_one('#contentsdata')
    if contentsdata is None:
        return ''
    return contentsdata['value']


def parse_raw_data(raw_data):
    lines = re.split(r'\s{100,}', raw_data)
    parsed_data = {}

    for line in lines:
        address = line[:8].strip()
        content = line[8:].strip()

        if address == '0000':
            break

        parsed_data[address] = content.split('|')

    return parsed_data


def extract_indicator(processed_raw_data, address):
    return processed_raw_data.get(address, f'{" "*3}')[2]


def build_indicator_data(processed_raw_data, bank_code, bank_name):
    return {
        "지점명": bank_name,
        "지점코드": bank_code,
        "위험가중자산대비 자기자본비율": extract_indicator(processed_raw_data, '25000001'),
        "순고정이하 여신비율": extract_indicator(processed_raw_data, '25000005'),
        "유동성 비율": extract_indicator(processed_raw_data, '25000007'),
        "총자산 순이익률": extract_indicator(processed_raw_data, '25000009'),
        "경영실태 평가": extract_indicator(processed_raw_data, '31000001'),
    }


def fetch_bank_indicators():
    for bank_code, bank_name in tqdm(load_bank_code_info().items()):
        payload = build_payload(bank_code)
        html = scraper.fetch_page_source(method='POST',
                                         url=BANK_INDICATOR_CONSTANT['URL'],
                                         headers=BANK_INDICATOR_CONSTANT['HEADERS'],
                                         data=payload)
        soup = scraper.create_soup(html)
        raw_data = extract_raw_data(soup)
        parsed_raw_data = parse_raw_data(raw_data)
        yield build_indicator_data(parsed_raw_data, bank_code, bank_name)


def write_sheet(bank_indicator):
    df = pd.DataFrame(bank_indicator)
    gs = gspread.service_account('realjamdev_gcp_key.json')
    sheet = gs.open("BANK_DB")
    worksheet = sheet.worksheet("kfcc")
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


def main():
    bank_indicator = list(fetch_bank_indicators())
    write_sheet(bank_indicator)


if __name__ == '__main__':
    main()
