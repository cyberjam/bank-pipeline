from typing import Final, Dict

CODE_REGION: Final = ('서울', '인천', '경기', '강원', '충남', '충북', '대전', '경북',
                      '경남', '대구', '부산', '울산', '전북', '전남', '광주', '제주', '세종')
CODE_URL: Final = 'https://www.kfcc.co.kr/map/list.do'

CODE_HEADERS: Dict = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

CODE_JSON_PATH: Final = 'data/bank_code_info.json'


INDICATOR_URL: Final = 'https://kfcc.co.kr/gumgo/gum0301_view_new.do'

INDICATOR_HEADERS: Final = {
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

INDICATOR_PAYLOAD: Dict = {
    'procGbcd': '1',
    'pageNo': '',
    'gongsiGmgoid': '',
    'gmgocd': '',
    'hpageBrwsUm': '1',
    'gongsiDate': '',
    'strd_yymm': '202212',
    'gmgoNm': '',
    'gonsiYear': '2022',
    'gonsiMonth': '12'
}

INDICATOR_JSON_PATH = 'data/bank_indicator.json'


GLOBAL_CONSTANT = {"CODE_JSON_PATH": CODE_JSON_PATH,
                   "INDICATOR_JSON_PATH": INDICATOR_JSON_PATH}

BANK_CODE_CONSTANT = {"REGION": CODE_REGION,
                      "URL": CODE_URL,
                      "HEADERS": CODE_HEADERS}

BANK_INDICATOR_CONSTANT = {
    "URL": INDICATOR_URL,
    "HEADERS": INDICATOR_HEADERS,
    "PAYLOAD": INDICATOR_PAYLOAD
}
