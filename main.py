import fmk
import ppom
import kakao
import time
import random
# from datetime import datetime

import logging
logging.basicConfig(filename='logs/example1.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info('START PROGRAM')


items = [
    '아몬드+브리즈', 
    '오메가',
    '루테인', 
    # '팸퍼스+에어', 
    # # '압타밀+프로푸트라', 
    # '햇반', 
    '톤프리', 
    # # '칫솔살균', 
    '아이허브', 
    # # '삼다수', 
    # 'master+3s',
    '네스+캡슐',
    '로보락',
    '제스프리',
    '로지텍',
    '토닉'
]

logging.info('Searching items: %s', items)

ppom_items_dict = dict()
fm_items_dict = dict()

r_token = kakao.f_auth()

for item in items:
    access_token = kakao.f_auth_refresh(r_token)
    org_ppom_list = ppom.find_keyword_and_get_list(item)
    time.sleep(random.randint(5,15))
    org_fm_list = fmk.find_keyword_and_get_list(item)

    # print(org_ppom_list[0])
    try: 
        kakao.f_send_msg(access_token, org_ppom_list[0], item)
    except IndexError:
        pass
    
    access_token = kakao.f_auth_refresh(r_token)

    try: 
        kakao.f_send_msg(access_token, org_fm_list[0], item)
    except IndexError:
        pass   

    ppom_items_dict[item] = org_ppom_list
    fm_items_dict[item] = org_fm_list
    org_ppom_list.clear()
    org_fm_list.clear()
    time.sleep(random.randint(5,15))
logging.info('Initial setting complete')
print('start')

# r_token = kakao.f_auth()

count = 0

while True:   
    access_token = kakao.f_auth_refresh(r_token)      

    for item in items:
        ppom_list = ppom.find_keyword_and_get_list(item)
        # ppom_list = [
        #             {'name': '[카카오톡]로보락다이애드 프로 (493,050원/무료)', 'idx': '48050188', 'highlight': 'n', 'prices': '493,050원', 'time': '13:20:32', 'url': '/new/bbs_view.php?id=ppomppu&no=480501&page=1&search_type=sub_memo&keyword=%B7%CE%BA%B8%B6%F4'},
        #             {'name': '[11번가]로보락S8 Pro Ultra (1,490,000/무료)', 'idx': '477534', 'highlight': 'y', 'prices': '1,490,000', 'time': '23-08-11', 'url': '/new/bbs_view.php?id=ppomppu&no=477534&page=1&search_type=sub_memo&keyword=%B7%CE%BA%B8%B6%F4'},
        #             {'name': '[카카오 선물하기]로보락S8 Pro Ultra  (1,590,000원 / 무료...', 'idx': '477045', 'highlight': 'n', 'prices': '1,590,000원 ', 'time': '23-08-08', 'url': '/new/bbs_view.php?id=ppomppu&no=477045&page=1&search_type=sub_memo&keyword=%B7%CE%BA%B8%B6%F4'}
        #             ]

        fm_list = fmk.find_keyword_and_get_list(item)

        ppom_idx_list = [i['idx'] for i in ppom_list]
        fm_idx_list = [i['idx'] for i in fm_list]

        org_ppom_idx_list = [i['idx'] for i in ppom_items_dict[item]]
        org_fm_idx_list = [i['idx'] for i in fm_items_dict[item]]

        if ppom_idx_list[0] == org_ppom_idx_list[0]:
            # 핫딜 알림 구현
            pass
        else:
            sms_idx_list = list(set(ppom_idx_list) - set(org_ppom_idx_list))

            for i in range(0, len(sms_idx_list)):
                for each in ppom_list:
                    if each['idx'] == sms_idx_list[i]:
                        access_token = kakao.f_auth_refresh(r_token) 
                        kakao.f_send_msg(access_token, each, item)
                        logging.info('send talk - ppomppu: %s', item)
                        print(each)
                    else:
                        pass

            ppom_items_dict[item] = ppom_list

        if fm_idx_list[0] == org_fm_idx_list[0]:
            # 핫딜 알림 구현
            pass
        else:
            sms_idx_list = list(set(fm_idx_list) - set(org_fm_idx_list))

            for i in range(0, len(sms_idx_list)):
                for each in fm_list:
                    if each['idx'] == sms_idx_list[i]:
                        access_token = kakao.f_auth_refresh(r_token) 
                        kakao.f_send_msg(access_token, each, item)
                        logging.info('send talk - ppomppu: %s', item)
                        print(each)
                    else:
                        pass

            fm_items_dict[item].update(fm_list)


        # sms_ppom_list = list(set(tuple(d.items()) for d in ppom_list) - set(tuple(d.items()) for d in ppom_items_dict[item]))
        # print(sms_ppom_list)
        # sms_ppom_list = [item for item in ppom_list if item not in ppom_items_dict[item]]
        # sms_ppom_list = []
        # for item in ppom_list:
        #     if item not in ppom_items_dict[item]:
        #         sms_ppom_list.append(item)

        # sms_fm_list = list(set(tuple(d.items()) for d in fm_list) - set(tuple(d.items()) for d in fm_items_dict[item]))
        # print(sms_fm_list)
        # sms_fm_list = [item for item in fm_list if item not in fm_items_dict[item]]
        # sms_fm_list = []
        # for item in ppom_list:
        #     if item not in fm_items_dict[item]:
        #         sms_fm_list.append(item)

        logging.info('compare history with current complete: %s', item)

        # if len(sms_ppom_list) == 0:
        #     # 핫딜로 올라가면 알림하는거 구현
        #     pass
        # else:
        #     for i in range(0, sms_ppom_list):
        #         logging.info('ppomppu: %s', item)
        #         kakao.f_send_msg(access_token, sms_ppom_list[i], item)
        #     org_ppom_list = ppom_list

        # if len(sms_fm_list) == 0:
        #     # 핫딜로 올라가면 알림하는거 구현
        #     pass
        # else:
        #     for i in range(0, sms_fm_list):
        #         logging.info('fm: %s', item)
        #         kakao.f_send_msg(access_token, sms_fm_list[i], item)
        #     org_fm_list = fm_list
        
        logging.info('each item search complete: %s', item)

        ppom_list.clear()
        fm_list.clear()
        time.sleep(random.randint(10,30))

    logging.info('total searching complete: %s', count)
    count+=1
    time.sleep(random.randint(550,650))





