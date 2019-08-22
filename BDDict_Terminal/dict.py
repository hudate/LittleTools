import urllib.request

import requests
from lxml import etree


class ConsultWord(object):

    def __init__(self, words, url="https://fanyi.baidu.com/"):
        self.__url = url
        self.__words = words
        self.__token = self.__get_token()
        self.__from_type = self.__ajust_type()
        self.__to_type = self.__to_type()
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'origin': 'https://fanyi.baidu.com',
            'referer': 'https://fanyi.baidu.com/',
            'accept': 'text / html, application / xhtml + xml, application / xml;'
                        'q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;'
                        'v = b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN, zh; q = 0.9',
            'cache-control': 'max-age=0'
        }
        self.__transtype = 'translang'


    def __ajust_type(self):
        pass

    def __to_type(self):
        pass

    def __get_token(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'origin': 'https://fanyi.baidu.com',
            'referer': 'https://fanyi.baidu.com/'
        }
        res = requests.get(url=self.__url, headers=headers)
        et = etree.HTML(res.text)
        # 获取系统时间
        # token = str(et.xpath('//body//script/text()')).split("token: '")[1].split(": '")[1].split("',")[0]

        # 获取token
        token = str(et.xpath('//body//script/text()')).split("token: '")[1].split("',")[0]
        return token

    def __consult_word(self):
        data = {
            'from': self.__from_type,
            'to': self.__to_type,
            'query': self.__words,
            'transtype': self.__transtype,
            'simple_means_flag': 3,
            'sign': 1924543.23456,
            'token': self.__token
        }
        res = requests.post(url=self.__url, data=data, headers=self.__headers)
        return res.text
        # et = etree.HTML(res.text)
        # token_script = et.xpath('/body/script/text()')
        # # print(token_script)

    def parse_data(self):
        data = self.__consult_word()
        print(data)


    def look_up(self):
        result = self.parse_data()
        pass


if __name__ == '__main__':
    # unknow_words = input("请输入要查询的单词：")
    unknow_words = 'abs'
    consult = ConsultWord(unknow_words)
    consult.look_up()



