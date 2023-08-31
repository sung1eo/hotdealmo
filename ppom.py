#ppom.py

import requests
import os
import json
import time
import copy
import re
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# 변수 선언

board_list = []
keyword ='아몬드+브리즈'
pattern = r'\((.*?)\/'


# 사이트 리스트 가져오는 함수
def find_keyword_and_get_list(keyword):

    # 사이트에 파라미터로 넘길 조건들, 키워드 추가시 +뒤에 키워드 추가
    params = {
    'search_type': 'sub_memo',
    'keyword': keyword
    }

    url = 'https://m.ppomppu.co.kr/new/bbs_list.php?id=ppomppu&category='

    response = requests.get(url, params=params)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        idxs = soup.select('#wrap > div.ct > div.bbs > ul > li > a')
        times = soup.select('#wrap > div.ct > div.bbs > ul > li > a > div.thmb_N2 > ul > li.exp > time')
        items = soup.select('#wrap > div.ct > div.bbs > ul > li > a > div.thmb_N2 > ul > li.title > span.cont')
        links = soup.select('a.list_b_01n')
        for idx, item in enumerate(items):
            # 종료가 아닌 item만 찾는다
            if 'text-decoration:line-through' not in item:
                name = item.get_text(strip=True)
                parsed_url = urlparse(idxs[idx]['href'])
                query_params = parse_qs(parsed_url.query)
                href = query_params.get('no', [''])[0]
                time = times[idx].text
                soup_item = BeautifulSoup(str(item), 'html.parser')             
                yn = 'y' if soup_item.find(class_='newhot') else 'n'
                price = item.text.strip()
                start_index = price.rfind('(') + 1
                end_index = price.rfind('/')
                price = price[start_index:end_index]
                url = links[idx]['href']
                item_dict = {'name': name, 'idx': href, 'highlight': yn, 'prices':price, 'time':time, 'url':url}
                board_list.append(item_dict)
            else:
                pass
    else:
        print('ppom',response.status_code)

    return board_list

# print(find_keyword_and_get_list('아몬드'))