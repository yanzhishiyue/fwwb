'''
@file : text.py
@Author: Yak
@Date  : 2021/4/2 21:57
@Contact : 1683077301@qq.com
@Software: PyCharm
'''
import requests
import urllib.request
import urllib
import json

# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id ='xP7yt40qeTvOZ9crgj4lDe9g'
client_secret ='FRwPpId2CVfWQHZBnOF6gP9M59juhWjZ'

# 获取token
def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')  # 需要的参数
    response = urllib.request.urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key


def txt_correction(content):
    if content == '':
        return ''
    token = get_token()
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/ecnet'
    params = dict()
    params['text'] = content
    params = json.dumps(params).encode('utf-8')  # 将params转换成json，并使用‘utf-8’编码
    access_token = token
    url = url + "?access_token=" + access_token
    request = urllib.request.Request(url=url, data=params)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        import time
        time.sleep(0.3)
        content = content.decode('GB2312')
        data = json.loads(content)
        print(data)
        item = data['item']
        word = item['correct_query']
        return  word
        # print(item['correct_query'])



# txt_correction('你有没有见刀.')
# txt_correction('为什么你拿么慢!')
# txt_correction('我学Java')