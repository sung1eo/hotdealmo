import requests
import json
import time

#code url  https://kauth.kakao.com/oauth/authorize?client_id=자신의 rest key값&redirect_uri=https://example.com/oauth&response_type=code
#code url  https://kauth.kakao.com/oauth/authorize?client_id=aecc5deb422efc7a2b2a44d01edbde76&redirect_uri=https://example.com/oauth&response_type=code
#추가 동의 https://kauth.kakao.com/oauth/authorize?client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}&response_type=code&scope=account_email,gender
#추가 동의 https://kauth.kakao.com/oauth/authorize?client_id=aecc5deb422efc7a2b2a44d01edbde76&redirect_uri=https://example.com/oauth&response_type=code&scope=friends
auth_url = 'https://kauth.kakao.com/oauth/token' 
check_auth_url = 'https://kapi.kakao.com/v1/user/access_token_info' 
rest_api_key = 'aecc5deb422efc7a2b2a44d01edbde76'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'eTofgn2vMR77D7O701Lb8RaCSz8ir_4VXXHwm-O59-rtpokg1Om2YvrCNkWi1TL8XRYQ9QoqJVAAAAGKST1X9A'
message_url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'  # 나에게 보내기 (https://developers.kakao.com/docs/latest/ko/message/rest-api#default-template-msg-me)
custom_message_url = 'https://kapi.kakao.com/v2/api/talk/memo/send' # 나에게 보내기 (https://developers.kakao.com/docs/latest/ko/message/rest-api#custom-template-msg-me)
check_url = 'https://kapi.kakao.com/v1/api/talk/friends'



def f_auth():
    header = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'} 
    data = {
        'grant_type': 'authorization_code',
        'client_id': rest_api_key,
        'redirect_uri': redirect_uri,
        'code': authorize_code,
    }
    url = auth_url
    response = requests.post(url, headers=header, data=data)
    tokens = response.json()

    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    r_token = ts["refresh_token"]
    return r_token

# def check_auth(token):
#     header = {'Authorization': 'Bearer ' + token}    
#     url = check_auth_url
#     response = requests.post(url, headers=header)
#     tokens = response.json()
#     with open("check_auth.json", "w") as fp:
#         json.dump(tokens, fp)   

def f_auth_refresh(r_token):
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    data = {
        "grant_type": "refresh_token",
        "client_id": rest_api_key,
        "refresh_token": r_token
    }
    response = requests.post(auth_url, data=data)
    tokens = response.json()

    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)
    with open("kakao_code.json", "r") as fp:
        ts = json.load(fp)
    token = ts["access_token"]
    return token


def f_send_talk(token, text):
    header = {'Authorization': 'Bearer ' + token}
    url = message_url
    post = {
        'object_type': 'text',
        'text': text,
        'link': {
            'web_url': 'https://developers.kakao.com',
            'mobile_web_url': 'https://developers.kakao.com'
        },
        'button_title': '키워드'
    }
    data = {'template_object': json.dumps(post)}
    return requests.post(url, headers=header, data=data)

def f_send_msg(token, item_msg, item):
    header = {'Authorization': 'Bearer ' + token}
    url = message_url

    if 'ppomppu' in item_msg['url']:
        post = { 
            'object_type': 'text',
            'text': '[[뽐뿌]]\n검색어명:'+item+'\n게시글명:'+item_msg['name']+'\n가격:'+item_msg['prices']+'\nhighlight여부:'+item_msg['highlight']+'\n날짜:'+item_msg['time'],
            'link': {
                'web_url': 'https://m.ppomppu.co.kr/'+item_msg['url'],
                'mobile_web_url': 'https://m.ppomppu.co.kr/'+item_msg['url']
            },
            'button_title': '확인'
        }
        # post = {
        #     'object_type': 'commerce',
        #     'content': {
        #         # 'title': '[[뽐뿌]] 게시글명:'+item_msg['name']+'\n'+'가격:'+item_msg['prices']+'\n'+'highlight여부:'+item_msg['highlight'],
        #         'title': '[[뽐뿌]] 검색어:'+item,
        #         'description':item_msg['name'],
        #         'link':{
        #             'web_url': 'https://m.ppomppu.co.kr/'+item_msg['url'],
        #             'mobile_web_url': 'https://m.ppomppu.co.kr/'+item_msg['url']
        #         }
        #     },
        #     'commerce': {
        #         'regular_price': item_msg['prices']
        #     },
        #     'buttons':{
        #         'title':'바로가기',
        #         'link':{
        #             'web_url': 'https://m.ppomppu.co.kr/'+item_msg['url'],
        #             'mobile_web_url': 'https://m.ppomppu.co.kr/'+item_msg['url']
        #         }
        #     }
        # }
    else:
        post = {
            'object_type': 'text',
            'text': '[[펨코]]\n검색어명:'+item+'\n게시글명:'+item_msg['name']+'\n'+'가격:'+item_msg['prices']+'\n'+'highlight여부:'+item_msg['highlight']+'\n날짜:'+item_msg['time'],
            'link': {
                'web_url': 'https://fmkorea.com/'+item_msg['url'],
                'mobile_web_url': 'https://fmkorea.com/'+item_msg['url']
            },
            'button_title': '확인'
        }
    # post = {
    #     'object_type': 'text',
    #     'text': '게시글명:'+item['name']+'\n'+'가격:'+item['prices']+'highlight여부:'+item['highlight'],
    #     'link': {
    #         'web_url': 'https://developers.kakao.com',
    #         'mobile_web_url': 'https://developers.kakao.com'
    #     },
    #     'button_title': '키워드'
    # }
    data = {'template_object': json.dumps(post)}

    response = requests.post(url, headers=header, data=data)
    # print(response)
    return response

# def check_friends(token):
#     header = {'Authorization': 'Bearer ' + token}
#     url = check_url
#     return requests.get(url, headers=header) 

# item = {'name': '[티몬] 광천김아몬드김자반 40g x 10봉 외 다양 (4,840원/무료)', 'idx': '472822', 'highlight': 'n', 'prices': '4,840원', 'time': '23-07-12', 'url': '/new/bbs_view.php?id=ppomppu&no=472822&page=1&search_type=sub_memo&keyword=%BE%C6%B8%F3%B5%E5'}
# r_token = f_auth()

# while True:
#     access_token = f_auth_refresh(r_token)  
#     # f_send_talk(access_token, '카카오톡 테스트입니다 3')
#     f_send_msg(access_token, item)
#     # print(check_friends(access_token).json())
#     time.sleep(1800)