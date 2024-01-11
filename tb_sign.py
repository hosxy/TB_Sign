#!/usr/bin/env python3

import re,requests,sys,time
from bs4 import BeautifulSoup


def get_tieba_list(s:requests.Session) -> list:

    bar_list = []
    url = "https://tieba.baidu.com/f/like/mylike?&pn="
    res = s.get(url + "1")

    soup = BeautifulSoup(res.text,'html.parser')

    for i in soup.find_all('a',href=re.compile(r'f\?kw')):
        bar_list.append(i.string)

    for i in soup.find_all('a',href=re.compile('mylike')):
        if i.string.isdigit():
            res = s.get(url + i.string)
            soup = BeautifulSoup(res.text,'html.parser')
            for i in soup.find_all('a',href=re.compile(r'f\?kw')):
                bar_list.append(i.string)

    return bar_list


def tieba_sign(s:requests.Session,tieba_list:list) -> None:
    url = "https://tieba.baidu.com/sign/add"
    
    for name in tieba_list:
        parameters = {"ie":"utf8","kw":name}
        res = s.post(url,params=parameters)
        print(name+ ": " + res.json().get("error"))
        time.sleep(2)


headers = {
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "http://tieba.baidu.com",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://tieba.baidu.com/i/i/forum?&pn=1",
    "Host": "tieba.baidu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
}


s = requests.session()
s.headers.update(headers)

for i in sys.argv:
    if i == sys.argv[0]:
        continue

    ck = i.split(":")
    cookies = {"BDUSS": ck[0], "STOKEN": ck[1]}
    s.cookies.clear_session_cookies()
    s.cookies.update(cookies)

    TB_list = get_tieba_list(s)
    tieba_sign(s,TB_list)
