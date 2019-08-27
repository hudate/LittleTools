#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hashlib
import json
import random
import time
import requests
import sys

class YDTrans(object):

    def __init__(self, content):
        self.__base_url = 'http://fanyi.youdao.com/'
        self.__lookup_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.__content = content
        self.__cookies = ''
        self.__time = ''
        self.__salt = self.__get_salt()
        self.__sign = self.__get_sign()
        self.__cookie = None    # cookie对象：第一次请求获取到的原始cookie
        self.__cookies = self.__get_cookie()    # 列表：从第一次请求获取到的原始cookie中解析出需要的cookie值
        self.__color()
        self.__parse()

    def __get_salt(self):
        self.__time = str(int(time.time() * 1000))
        return self.__time + str(random.randint(0, 10))

    def __get_sign(self):
        u = 'fanyideskweb'
        e = self.__content  # 需要被翻译的内容
        i = self.__salt
        j = 'n%A-rKaT5fb[Gy?;N5@Tj'
        sign_md5 = hashlib.md5((u + e + i + j).encode()).hexdigest()
        return sign_md5

    def __parse(self):
        smart_result = ''
        req_text = self.__get_data_page()
        req_json = json.loads(req_text)
        src = req_json['translateResult'][0][0]['src']
        tgt = req_json['translateResult'][0][0]['tgt']
        try:
            smart_result = [res.replace('\r\n', '\t') for res in req_json['smartResult']['entries'] if res != '']
        except:
            pass

        # 输出翻译信息
        print('\n%s: %s\n' % (src, tgt))

        # 输出其他的翻译信息
        if smart_result != '':
            print(self.__color_green_start, end='')
            print("####以下是来自有道字典的内容：####\n")
            [print('%s' % res) for res in smart_result]
            print('\n##################################\n')
            print(self.__color_end, end='')

    def __get_cookie(self):
        req = requests.get(self.__base_url)
        cookie = [cookie for cookie in req.cookies]
        self.__cookie = cookie
        cookie_list = []
        for i in range(len(cookie)):
            cookie_list.append(cookie[i].value)
        return cookie_list

    def __get_data_page(self):
        cookies = {
            '___rl__test__cookies=': self.__time,
            'OUTFOX_SEARCH_USER_ID': self.__cookies[0],
            'JSESSIONID': self.__cookies[1]
        }

        headers = {
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        }

        data = {
            'i': self.__content,
            'client': 'fanyideskweb',
            'salt': self.__salt,
            'sign': self.__sign,
            'version': '2.1',
            'keyfrom': 'fanyi.web',
        }
        res = requests.post(url=self.__lookup_url, headers=headers, data=data, cookies=cookies)
        return res.text

    def __color(self):
        if sys.platform[0] != "nt":
            self.__color_red_start = "\033[31m"
            self.__color_green_start = "\033[32m"
            self.__color_end = '\033[0m'


if __name__ == '__main__':
    content = sys.argv[1:]
    while 1:
        if len(content) != 0:
            if len(content) != 1:
                content = ' '.join(content)
            else:
                content = content[0]
            break
        else:
            content = input('请输入您要翻译的内容：')

    yd = YDTrans(content)

