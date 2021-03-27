import os
import re
import json
from urllib import parse
import requests

items = ['문화상품권', '공유기']
bot_id = os.getenv('BOT_ID')
chat_id = os.getenv('CHAT_ID')
gist_url = f'https://api.github.com/gists/{os.getenv("GIST_ID")}'
recent_link = requests.get(gist_url).json()['files']['recent_link']['content']
url_base = 'http://www.ppomppu.co.kr/zboard/'
list_url = 'zboard.php?id=ppomppu&page_num=20&search_type=sub_memo&keyword='
noti_url = f'https://api.telegram.org/bot{bot_id}/sendMessage'
notis = []
for item in items:
    target_url = url_base + list_url + parse.quote(item)
    response = requests.get(target_url).text
    links = re.findall(r"(?<=<a href=\")view.php\?id=ppomppu&.*?(?=\")", response)
    if links:
        try:
            rs = links.index(recent_link)
            if rs:
                notis += reversed([url_base + links[i] for i in range(rs)])
        except:
            notis += reversed([url_base + l for l in links])
    else:
        notis += [f'{item} 게시글 링크 파싱 오류 발생']
    if notis:
        if links:
            gist_headers = {
                'Accept':'application/vnd.github.v3+json',
                'Authorization':f'token {os.getenv("GIST_TOKEN")}'
            }
            gist_data = {
                'description':'update recent link',
                'files':{
                    'recent_link': {
                        'content': links[0]
                    }
                }
            }
            requests.patch(gist_url, headers=gist_headers, data=json.dumps(gist_data))
        for n in notis:
            noti_params = {
                'chat_id': chat_id,
                'text': n
            }
            requests.get(noti_url, noti_params)
