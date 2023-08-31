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

# import kakao

# 변수 선언
board_list = []
keyword ='아몬드+브리즈'

def find_keyword_and_get_list(keyword):

    params = {
    'mid': 'hotdeal',
    'category': '',
    'listStyle': 'webzine',
    'search_keyword': keyword,  # 검색어를 원하는 값으로 설정
    'search_target': 'title_content',  # 타겟을 원하는 값으로 설정
    }

    url = 'https://www.fmkorea.com/search.php'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        times = soup.select('.regdate') #글 작성시간 크롤링
        items = soup.find_all('a', re.compile('hotdeal_var8*')) 
        prices = soup.select('.hotdeal_info > span:nth-child(2) > a.strong')  # 가격 크롤링

        for idx, item in enumerate(items):
            
            if item['class'] == ['hotdeal_var8']:
                name = item.get_text(strip=True).replace('\t', '').rstrip('[')
                loc = name.rfind('[')
                name = name[:loc]
                parsed_url = urlparse(item['href'])
                query_params = parse_qs(parsed_url.query)
                href = query_params.get('document_srl', [''])[0]
                yn = 'y' if item.find_next_sibling('span', class_='STAR-BEST STAR-BEST-RT') else 'n'
                time = times[idx].text.replace('\t','')
                price = prices[idx].text
                url = item['href']

                item_dict = {'name': name, 'idx': href, 'highlight': yn, 'prices':price, 'time':time, 'url':url}
                board_list.append(item_dict)
            else:
                pass

    else:
        print('fm',response.status_code)

    return board_list

# while True:
#     f_get_list()  # 게시글 크롤링
#     access_token = kakao.f_reissue_token()  # 새로운 액세스 토큰을 발급 받음
#     sms_list = list(set(board_list) - set(p_board_list))  # 이전 리스트와 비교하여 다른 값만 문자 보낼 리스트로 저장
#     p_board_list = copy.deepcopy(board_list)  # 현재 게시글을 이전 게시글로 저장

#      authorization_kakao.f_send_msg(access_token, '뽐뿌 결과\n'  +'키워드 : '+keyword + '\n현재 시간 {} 최신글은 총 {}개입니다.'.format(datetime.now().strftime('%H:%M:%S'),len(sms_list)))

#     for i in range(0, len(sms_list), 1):
#         kakao.f_send_msg(access_token, sms_list[i])

#     board_list.clear()
#     sms_list.clear()
#     time.sleep(1800)  # 반복 주기