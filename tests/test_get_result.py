""" test_get_result.py """

import requests

from click.testing import CliRunner
from commandict.get_result import main, parse, parse_detail


DAUM_DICT_HOST = "https://dic.daum.net/"
LANG = 'eng'


# TODO: test with more words
def test_parse_no_polysemy():

    KEYWORD = 'buy'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    meanings, wordid = parse(response.text)
    assert meanings.startswith('1.사다')
    assert wordid == 'ekw000024208'


def test_parse_with_polysemy():

    KEYWORD = 'test'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    meanings, wordid = parse(response.text)
    assert meanings.startswith('1.시험')
    assert wordid == 'ekw000167718'


def test_parse_no_result():
    KEYWORD = 'cthulhu'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    result, wordid = parse(response.text)
    assert result == 'No results found.'
    assert wordid == ''


def test_parse_detail():
    # TODO: test with more words
    KEYWORD = 'buy'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    meanings, wordid = parse(response.text)
    detailed_url = f'https://dic.daum.net/word/view.do?wordid={wordid}'
    detailed_text = requests.get(detailed_url).text
    result = parse_detail(detailed_text, wordid, 'synonym')
    synonym = '''purchase: 구매하다, 구입하다, 매수하다, 사다, 인수하다
pay for: 대가를 지불하다, 돈을 내다, 내다, 부담하다, 계산하다
procure: 조달하다, 입수, 구하다, 도입, 얻다'''
    assert result == synonym
    result = parse_detail(detailed_text, wordid, 'antonym')
    antonym = 'sell: 팔다, 판매하다, 매각하다, 매도하다, 매매'
    assert result == antonym


def test_parse_detail_no_antonym():
    KEYWORD = 'test'
    url = f'{DAUM_DICT_HOST}/search.do?q={KEYWORD}&dic={LANG}'
    response = requests.get(url)
    meanings, wordid = parse(response.text)
    detailed_url = f'https://dic.daum.net/word/view.do?wordid={wordid}'
    detailed_text = requests.get(detailed_url).text
    result = parse_detail(detailed_text, wordid, 'synonym')
    synonym = '''work: 일하다, 연구, 작업, 작품, 작동하다
study: 연구, 조사, 공부, 검토하다, 관찰하다
ask: 묻다, 요청하다, 질문하다, 부탁하다, 말씀하다
game: 게임, 경기, 시합
research: 연구, 조사, 탐구, 탐사'''
    assert result == synonym
    result = parse_detail(detailed_text, wordid, 'antonym')
    antonym = 'No results found.'
    assert result == antonym


def test_main_no_result():
    KEYWORD = 'cthulhu'

    runner = CliRunner()
    result = runner.invoke(main, KEYWORD)
    assert result.exit_code == 0
    assert 'Searching...' in result.output
    assert 'No results found.' in result.output


def test_main_undefined_command():
    KEYWORD = 'command'
    runner = CliRunner()
    result = runner.invoke(main,
                           args=KEYWORD,
                           input='\n'.join(['undefined_command', 'q']))
    assert result.exit_code == 0
    assert "Sorry, I don't understand." in result.output
