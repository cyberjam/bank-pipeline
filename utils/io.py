import json
import pandas as pd
import gspread
from constants import GOOGLE


def save_json(file_path, data):
    """ 결과물을 json으로 저장

    Args:
        file_path (string): 저장할 위치와 저장 파일 이름
        data (generator): 결과물
    """
    with open(file_path, 'w', encoding='UTF-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_json(file_path):
    with open(file_path, encoding='UTF-8') as file:
        return json.load(file)


def save_to_google_sheet(data):
    df = pd.DataFrame(data)
    gs = gspread.service_account(GOOGLE['KEY_FILE'])
    sheet = gs.open(GOOGLE['SHEET_NAME'])
    worksheet = sheet.worksheet(GOOGLE['WORKSHEET_NAME'])
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
