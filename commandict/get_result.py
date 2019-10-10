#!/usr/bin/env python
""" get_result.py """

import click
import sys

import requests
from bs4 import BeautifulSoup


DAUM_DICT_HOST = "https://alldic.daum.net/"

# TODO: 키워드 입력받기
# TODO: 설정에서 언어 입력받고 설정 저장할 수 있게
LANG = 'eng'


def parse(html: str):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.findAll('meta',
                      attrs={'property': 'og:description'})[0].get('content')


@click.command()
@click.argument('keyword')
def main(keyword):
    click.echo('Searching...')
    url = f'{DAUM_DICT_HOST}search.do?q={keyword}&dic={LANG}'
    response = requests.get(url)
    meanings = parse(response.text)
    print(meanings)


if __name__ == "__main__":
    main()
