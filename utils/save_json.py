import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def save_json(file_path, data):
    """ 결과물을 json으로 저장

    Args:
        file_path (string): 저장할 위치와 저장 파일 이름
        data (generator): 결과물
    """
    with open(file_path, 'w', encoding='UTF-8') as file:
        json.dump(list(data), file, ensure_ascii=False, indent=4)
