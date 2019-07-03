""" test_get_result.py """

import requests

from commandict.get_result import parse


def test_parse():
    DAUM_DICT_HOST = "https://alldic.daum.net/"
    KEYWORD = 'test'
    LANG = 'eng'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    meanings = parse(response.text)
    assert meanings.startswith('\n1.시험\n')
