""" get_result.py """

import requests
from bs4 import BeautifulSoup


DAUM_DICT_HOST = "https://alldic.daum.net/"

# TODO: 키워드 입력받기
# TODO: 설정에서 언어 입력받고 설정 저장할 수 있게
KEYWORD = 'test'
LANG = 'eng'


def parse(html: str):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.findAll('ul', attrs={'class': 'list_search'})[0].text


if __name__ == "__main__":
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    meanings = parse(response.text)
    print(meanings)
