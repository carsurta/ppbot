import os
import re
from urllib import parse
from datetime import datetime, timedelta
import requests

recent = datetime.now() - timedelta(minutes=15)
items = ['문화상품권']

bot_id = os.getenv('BOT_ID')
chat_id = os.getenv('CHAT_ID')
url_base = 'http://www.ppomppu.co.kr/zboard/'
list_url = 'zboard.php?id=ppomppu&page_num=20&search_type=sub_memo&keyword='
noti_url = f'https://api.telegram.org/bot{bot_id}/sendMessage'
notis = []
for item in items:
    target_url = url_base + list_url + parse.quote(item)
    response = requests.get(target_url).text
    times =  [datetime.strptime(t, '%y.%m.%d %H:%M:%S') for t in re.findall(r"(?<=<td nowrap class='eng list_vspace' colspan=2  title=\").*?(?=\" >)", response)]
    if times:
        is_recent = [t > recent for t in times]
        try:
            links = re.findall(r"(?<=<a href=\")view.php\?id=ppomppu&.*?(?=\")", response)
            rs = is_recent.index(False)
            if rs:
                notis += reversed([url_base + links[i] for i in range(rs)])
        except:
            notis += reversed([url_base + l for l in links])
    else:
        notis += ['시간 파싱 오류 발생']
    if notis:
        for n in notis:
            noti_params = {
                'chat_id': chat_id,
                'text': n
            }
            requests.get(noti_url, noti_params)