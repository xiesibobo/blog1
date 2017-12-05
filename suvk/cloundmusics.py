# -*- coding:utf8 -*-
import base64
import codecs
import json

import requests
from Crypto.Cipher import AES


# 返回搜索列表的params
def get_music_list(keyword):
    first_param = '{"hlpretag":"","hlposttag":"","id":"","s":"' + keyword + '","type":"1","offset":"0","total":"true","limit":"100","csrf_token":""}'
    return get_params(first_param)


# 返回每个歌曲的params
def get_music_url(id):
    first_param = '{ids: "[' + str(id) + ']", br: 128000, csrf_token: ""}'
    return get_params(first_param)


# 返回加密后的POST参数params
def get_params(first_param):
    iv = '0102030405060708'
    first_key = '0CoJUm6Qyw8W8jud'
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


# 返回加密后的POST参数encSecKey
def get_encSecKey():
    # encSecKey是固定的参数
    encSecKey = '257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c'
    return encSecKey


# AES加密算法
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


# 返回json数据
def get_json(url, params, encSecKey):
    data = {
        "params": params,
        "encSecKey": encSecKey
    }
    response = requests.post(url, data=data)
    return response.content

def get_music():
    search_url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    singer_name = raw_input('请输入歌手名:')
    if singer_name=='quit!':return True
    params = get_music_list(singer_name)
    encSecKey = get_encSecKey()
    json_text = get_json(search_url, params, encSecKey)
    json_dict = json.loads(json_text)
    for item in json_dict['result']['songs']:
        p = get_music_url(item['id'])
        music = get_json(url, p, encSecKey)
        songs = u'歌名：' + item['name'] + u'歌手：' + item['ar'][0]['name'] + '\n' + json.loads(music)['data'][0]['url']
        with codecs.open(singer_name + '.txt', 'a', encoding='utf-8') as f:
            f.write(songs + '\n')


if __name__ == "__main__":
    while True:
        if get_music():break
